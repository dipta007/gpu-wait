import subprocess
import logging
from typing import List, Optional
from .gpu_monitor import GPUMonitor


class CommandRunner:
    def __init__(self, gpu_monitor: Optional[GPUMonitor] = None):
        """
        Initialize command runner.

        Args:
            gpu_monitor (GPUMonitor, optional): GPU monitor instance
        """
        self.gpu_monitor = gpu_monitor or GPUMonitor()
        self.logger = logging.getLogger(__name__)

    def run_when_available(
        self, command: str, device_id: Optional[int] = None, shell: bool = True
    ):
        """
        Run command when GPU becomes available.

        Args:
            command (str): Command to run
            device_id (int, optional): Specific GPU to wait for
            shell (bool): Whether to run command in shell
        """

        def status_callback():
            self.logger.info("Waiting for GPU to become available...")

        self.gpu_monitor.wait_for_gpu(device_id, status_callback)

        try:
            self.logger.info(f"Running command: {command}")
            # Don't capture output when using shell=True to allow redirections to work
            result = subprocess.run(
                command, shell=shell, check=True, text=True, stdout=None, stderr=None
            )
            self.logger.info("Command completed successfully")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}")
            raise
