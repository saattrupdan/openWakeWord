from pathlib import Path

import setuptools


long_description = Path("README.md").read_text(encoding="utf-8")


setuptools.setup(
    name="openwakeword",
    version="0.6.0",
    install_requires=[
        "numpy>=1.26,<3",
        "onnxruntime>=1.18,<2",
        "tqdm>=4,<5",
        "scipy>=1.11,<2",
        "scikit-learn>=1.4,<2",
        "requests>=2,<3",
    ],
    extras_require={
        "tflite": [
            "ai-edge-litert>=2.0.2,<3; platform_system == 'Linux' or platform_system == 'Darwin'",
        ],
        "speex": [
            "speexdsp-ns>=0.1.2,<1; platform_system == 'Linux'",
        ],
        "test": [
            "pytest>=8,<9",
            "pytest-cov>=5,<7",
            "mock>=5.1,<6",
            "types-requests",
        ],
        # Training uses an older TensorFlow/ONNX conversion stack.  Keep it
        # opt-in and prevent its legacy pins from affecting runtime installs.
        "full": [
            "mutagen>=1.46,<2; python_version < '3.12'",
            "torch>=1.13.1,<3; python_version < '3.12'",
            "torchaudio>=0.13.1,<1; python_version < '3.12'",
            "torchinfo>=1.8,<2; python_version < '3.12'",
            "torchmetrics>=0.11.4,<1; python_version < '3.12'",
            "speechbrain>=0.5.14,<1; python_version < '3.12'",
            "audiomentations>=0.30,<1; python_version < '3.12'",
            "torch-audiomentations>=0.11,<1; python_version < '3.12'",
            "acoustics>=0.2.6,<1; python_version < '3.12'",
            "pyyaml>=6,<7; python_version < '3.12'",
            "tensorflow-cpu==2.8.1; python_version < '3.12'",
            "tensorflow-probability==0.16.0; python_version < '3.12'",
            "protobuf>=3.20,<4; python_version < '3.12'",
            "onnx-tf==1.10.0; python_version < '3.12'",
            "onnx==1.14.0; python_version < '3.12'",
            "pronouncing>=0.2,<1; python_version < '3.12'",
            "datasets>=2.14.4,<3; python_version < '3.12'",
            "deep-phonemizer==0.0.19; python_version < '3.12'",
        ],
    },
    author="David Scripka",
    author_email="david.scripka@gmail.com",
    description=(
        "An open-source audio wake word (or phrase) detection framework "
        "with a focus on performance and simplicity"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/openwakeword",
    project_urls={
        "Bug Tracker": "https://pypi.org/project/openwakeword/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.12",
)
