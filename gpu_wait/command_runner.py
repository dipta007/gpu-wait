import os
import signal
import sys
import subprocess
import logging
from typing import List, Optional, Any
from .gpu_monitor import GPUMonitor

import signal
import sys
from typing import Optional, Callable, Any

class SignalHandler:
    def __init__(self):
        self.process = None
        self.original_sigint = signal.getsignal(signal.SIGINT)
        self.original_sigtstp = signal.getsignal(signal.SIGTSTP)
        
    def __enter__(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTSTP, self.handle_signal)
        return self
        
    def __exit__(self, type: Any, value: Any, traceback: Any):
        signal.signal(signal.SIGINT, self.original_sigint)
        signal.signal(signal.SIGTSTP, self.original_sigtstp)
    
    def set_process(self, process):
        self.process = process
        
    def handle_signal(self, signum, frame):
        if self.process:
            print(f"\nReceived signal {signum}, terminating process...")
            self.process.terminate()
            self.process.wait()  # Wait for process to terminate
        sys.exit(signum)

class CommandRunner:
    def __init__(self, gpu_monitor: Optional[GPUMonitor] = None):
        """
        Initialize command runner.
        
        Args:
            gpu_monitor (GPUMonitor, optional): GPU monitor instance
        """
        self.gpu_monitor = gpu_monitor or GPUMonitor()
        self.logger = logging.getLogger(__name__)
        self.signal_handler = SignalHandler()
    
    def run_when_available(self, command: str, device_id: Optional[int] = None,
                          shell: bool = True):
        """
        Run command when GPU becomes available.
        
        Args:
            command (str): Command to run
            device_id (int, optional): Specific GPU to wait for
            shell (bool): Whether to run command in shell
        """
        def status_callback():
            self.logger.info("Waiting for GPU to become available...")
        
        with self.signal_handler:
            self.gpu_monitor.wait_for_gpu(device_id, status_callback)
            
            try:
                self.logger.info(f"Running command: {command}")
                # Start process without waiting
                process = subprocess.Popen(command, shell=shell, 
                                        text=True,
                                        stdout=None, stderr=None,
                                        preexec_fn=os.setsid)  # Create new process group
                
                # Register process with signal handler
                self.signal_handler.set_process(process)
                
                # Wait for completion
                return_code = process.wait()
                if return_code != 0:
                    raise subprocess.CalledProcessError(return_code, command)
                    
                self.logger.info("Command completed successfully")
                return process
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Command failed with exit code {e.returncode}")
                raise
