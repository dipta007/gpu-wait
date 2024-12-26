# GPU Wait

A Python package that monitors GPU resources and executes commands when the GPU becomes available.

## Installation

```bash
pip install gpu-wait
```

## Usage

### Command Line Interface

```bash
# Run a command when any GPU is available
gpu-wait "python train.py"

# Wait for specific GPU
gpu-wait -d 0 "python train.py"

# Customize memory threshold and polling interval
gpu-wait -t 0.8 -i 5 "python train.py"

# Enable verbose logging
gpu-wait -v "python train.py"
```

### Python API

```python
from gpu_wait import GPUMonitor, CommandRunner

# Create monitor with custom threshold
monitor = GPUMonitor(memory_threshold=0.8)

# Create command runner
runner = CommandRunner(monitor)

# Run command when GPU is available
runner.run_when_available("python train.py")
```

## Features

- Monitor single or multiple GPUs
- Customizable memory threshold and polling interval
- Command line interface
- Python API
- Logging support

## Requirements

- Python 3.6+
- NVIDIA GPU
- nvidia-ml-py
- psutil
- click

## License

MIT License