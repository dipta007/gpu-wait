import pynvml
import time
from typing import Optional, Callable


class GPUMonitor:
    def __init__(self, memory_threshold: float = 0.9, polling_interval: float = 1.0):
        """
        Initialize GPU monitor.

        Args:
            memory_threshold (float): Memory usage threshold (0.0 to 1.0)
            polling_interval (float): Time between checks in seconds
        """
        self.memory_threshold = memory_threshold
        self.polling_interval = polling_interval
        pynvml.nvmlInit()
        self.device_count = pynvml.nvmlDeviceGetCount()

    def is_gpu_available(self, device_id: Optional[int] = None) -> bool:
        """
        Check if GPU is available (memory usage below threshold).

        Args:
            device_id (int, optional): Specific GPU to check. If None, checks all GPUs.

        Returns:
            bool: True if GPU is available, False otherwise
        """
        if device_id is not None:
            return self._check_single_gpu(device_id)

        return any(self._check_single_gpu(i) for i in range(self.device_count))

    def _check_single_gpu(self, device_id: int) -> bool:
        handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        usage = info.used / info.total
        free = 1.0 - usage
        return free >= self.memory_threshold

    def wait_for_gpu(
        self, device_id: Optional[int] = None, callback: Optional[Callable] = None
    ):
        """
        Wait until GPU becomes available.

        Args:
            device_id (int, optional): Specific GPU to wait for
            callback (callable, optional): Function to call while waiting
        """
        while not self.is_gpu_available(device_id):
            if callback:
                callback()
            time.sleep(self.polling_interval)

    def __del__(self):
        try:
            pynvml.nvmlShutdown()
        except:
            pass
