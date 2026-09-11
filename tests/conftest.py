from pathlib import Path

import pytest

import openwakeword
from openwakeword import utils


@pytest.fixture(scope="session", autouse=True)
def pretrained_model_assets() -> None:
    """Download and validate every ONNX asset required by the test suite.

    Keeping this in one session fixture means a clean checkout never relies on
    whichever model happened to be downloaded by an earlier test module.
    """
    utils.download_models()
    required_assets = [
        *openwakeword.FEATURE_MODELS.values(),
        *openwakeword.VAD_MODELS.values(),
        *openwakeword.MODELS.values(),
    ]
    missing_assets = [
        Path(asset["model_path"])
        for asset in required_assets
        if not (
            Path(asset["model_path"]).is_file()
            and Path(asset["model_path"]).stat().st_size > 0
        )
    ]
    if missing_assets:
        missing = ", ".join(str(path) for path in missing_assets)
        pytest.fail(f"Model download did not provide required assets: {missing}")
