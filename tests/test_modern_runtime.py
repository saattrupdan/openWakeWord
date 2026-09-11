from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

import openwakeword
from openwakeword import model as model_module
from openwakeword import utils


def test_default_model_assets_are_onnx():
    assert all(path.endswith(".onnx") for path in openwakeword.get_pretrained_model_paths())
    assert openwakeword.MODELS["hey_jarvis"]["model_path"].endswith(
        "hey_jarvis_v0.1.onnx"
    )


def test_download_models_selects_one_framework_and_repairs_partial_assets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    downloaded: list[str] = []

    def fake_download(url: str, target_directory: str, file_size: int | None = None) -> None:
        del file_size
        downloaded.append(url)
        (Path(target_directory) / url.rsplit("/", maxsplit=1)[-1]).touch()

    monkeypatch.setattr(utils, "download_file", fake_download)
    existing = tmp_path / "embedding_model.onnx"
    existing.write_bytes(b"already downloaded")

    utils.download_models(model_names=["hey_jarvis"], target_directory=str(tmp_path))

    names = {url.rsplit("/", maxsplit=1)[-1] for url in downloaded}
    assert "embedding_model.onnx" not in names
    assert names == {
        "melspectrogram.onnx",
        "silero_vad.onnx",
        "hey_jarvis_v0.1.onnx",
    }
    assert all(not name.endswith(".tflite") for name in names)


def test_download_models_can_select_litert_assets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    downloaded: list[str] = []

    def fake_download(url: str, target_directory: str, file_size: int | None = None) -> None:
        del file_size
        downloaded.append(url.rsplit("/", maxsplit=1)[-1])
        (Path(target_directory) / downloaded[-1]).touch()

    monkeypatch.setattr(utils, "download_file", fake_download)
    utils.download_models(
        model_names=["hey_jarvis"],
        target_directory=str(tmp_path),
        inference_framework="tflite",
    )

    assert set(downloaded) == {
        "embedding_model.tflite",
        "melspectrogram.tflite",
        "silero_vad.onnx",
        "hey_jarvis_v0.1.tflite",
    }


def test_litert_backend_has_a_helpful_optional_dependency_error(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setitem(__import__("sys").modules, "ai_edge_litert", None)
    with pytest.raises(ValueError, match=r"openwakeword\[tflite\]"):
        openwakeword.Model(wakeword_models=["hey_jarvis"], inference_framework="tflite")


def test_speex_reports_unsupported_environment(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(model_module.platform, "system", lambda: "Windows")

    with pytest.raises(ImportError, match="only supported on Linux with CPython 3.12"):
        model_module._create_speex_noise_suppression()


def test_hey_jarvis_onnx_prediction_contract(monkeypatch: pytest.MonkeyPatch):
    class FakeSession:
        def __init__(self, model_path: str, **kwargs: object) -> None:
            self.model_path = model_path

        def get_inputs(self) -> list[SimpleNamespace]:
            return [SimpleNamespace(shape=[None, 16], name="features")]

        def get_outputs(self) -> list[SimpleNamespace]:
            return [SimpleNamespace(shape=[None, 1])]

        def run(self, outputs: object, inputs: dict[str, np.ndarray]) -> list[np.ndarray]:
            del outputs, inputs
            return [np.asarray([[[0.8]]], dtype=np.float32)]

    fake_onnxruntime = SimpleNamespace(
        SessionOptions=lambda: SimpleNamespace(
            inter_op_num_threads=1, intra_op_num_threads=1
        ),
        InferenceSession=FakeSession,
    )
    monkeypatch.setitem(__import__("sys").modules, "onnxruntime", fake_onnxruntime)

    class FakeFeatures:
        def __init__(self, **kwargs: object) -> None:
            del kwargs

        def __call__(self, audio: np.ndarray) -> int:
            del audio
            return 1280

        def get_features(self, size: int, start_ndx: int = -1) -> np.ndarray:
            del start_ndx
            return np.zeros((1, size, 96), dtype=np.float32)

        def reset(self) -> None:
            pass

    monkeypatch.setattr(model_module, "AudioFeatures", FakeFeatures)
    model = openwakeword.Model(wakeword_models=["hey_jarvis"])

    prediction = model.predict(np.zeros(1280, dtype=np.int16))

    assert list(prediction) == ["hey_jarvis"]
    assert model.models["hey_jarvis"].model_path.endswith("hey_jarvis_v0.1.onnx")
