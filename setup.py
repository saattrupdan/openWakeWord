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
            # ai-edge-litert publishes wheels for each platform supported by
            # LiteRT, including Windows.  Do not exclude a supported platform
            # with a package-level marker.
            "ai-edge-litert>=2.0.2,<3",
        ],
        "speex": [
            # speexdsp-ns only publishes Linux CPython 3.12 wheels.
            (
                "speexdsp-ns>=0.1.2,<1; "
                "platform_system == 'Linux' and "
                "platform_python_implementation == 'CPython' and "
                "python_version == '3.12'"
            ),
        ],
        "test": [
            "pytest>=8,<9",
            "pytest-cov>=5,<7",
            "mock>=5.1,<6",
            "types-requests",
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
