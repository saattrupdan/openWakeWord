import os

from openwakeword.model import Model
from openwakeword.vad import VAD
from openwakeword.custom_verifier_model import train_custom_verifier

__all__ = ["Model", "VAD", "train_custom_verifier"]

_RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "models")
_RELEASE_URL = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1"

# ONNX is the portable runtime supported by the base installation.  The tflite
# paths remain available through get_pretrained_model_paths(..., "tflite").
FEATURE_MODELS = {
    "embedding": {
        "model_path": os.path.join(_RESOURCES, "embedding_model.onnx"),
        "download_url": f"{_RELEASE_URL}/embedding_model.onnx",
    },
    "melspectrogram": {
        "model_path": os.path.join(_RESOURCES, "melspectrogram.onnx"),
        "download_url": f"{_RELEASE_URL}/melspectrogram.onnx",
    },
}

VAD_MODELS = {
    "silero_vad": {
        "model_path": os.path.join(_RESOURCES, "silero_vad.onnx"),
        "download_url": f"{_RELEASE_URL}/silero_vad.onnx",
    }
}

MODELS = {
    name: {
        "model_path": os.path.join(_RESOURCES, f"{name}_v0.1.onnx"),
        "download_url": f"{_RELEASE_URL}/{name}_v0.1.onnx",
    }
    for name in ("alexa", "hey_mycroft", "hey_jarvis", "hey_rhasspy", "timer", "weather")
}

model_class_mappings = {
    "timer": {
        "1": "1_minute_timer",
        "2": "5_minute_timer",
        "3": "10_minute_timer",
        "4": "20_minute_timer",
        "5": "30_minute_timer",
        "6": "1_hour_timer"
    }
}


def get_pretrained_model_paths(inference_framework="onnx"):
    """Return paths for all bundled wakeword models.

    Args:
        inference_framework (str): Either ``"onnx"`` (the default) or
            ``"tflite"``.

    Returns:
        list[str]: Paths to the models for the selected runtime.

    Raises:
        ValueError: If the requested inference framework is unsupported.
    """
    if inference_framework not in {"onnx", "tflite"}:
        raise ValueError(
            f"Unsupported inference framework: {inference_framework!r}. "
            "Choose 'onnx' or 'tflite'."
        )

    if inference_framework == "onnx":
        return [model["model_path"] for model in MODELS.values()]

    return [model["model_path"].replace(".onnx", ".tflite") for model in MODELS.values()]
