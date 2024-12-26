from setuptools import setup, find_packages

setup(
    name="gpu_wait",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nvidia-ml-py3",    # For NVIDIA GPU monitoring
        "psutil",           # For system resource monitoring
        "click"             # For CLI interface
    ],
    entry_points={
        "console_scripts": [
            "gpu-wait=gpu_wait.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to run commands when GPU resources are available",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gpu-wait",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)