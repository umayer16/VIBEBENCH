import subprocess
import time
import sys
import os

try:
    import resource
except ImportError:
    resource = None

class CodeExecutor:
    """
    Handles the dynamic execution of Python scripts in a sandboxed-style environment
    using Unix resource limits to ensure operational safety.
    """

    def __init__(self, timeout=5, memory_limit_mb=512):
        """
        Initializes the executor with specific safety constraints.

        Args:
            timeout (int): Maximum CPU time allowed in seconds.
            memory_limit_mb (int): Maximum memory allowed in megabytes.
        """
        self.timeout = timeout
        self.memory_limit = memory_limit_mb * 1024 * 1024 

    def _limit_resources(self):
        """Sets hard CPU and memory limits on the child process (Unix-only)."""
        if resource:
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))

    def run(self, file_path):
        """
        Executes a Python file and captures its performance metrics.

        Args:
            file_path (str): The path to the script to execute.

        Returns:
            dict: Metrics including status, execution time, and potential errors.
        """
        if not os.path.exists(file_path):
            return {"status": "Error", "message": "File not found"}

        start_time = time.perf_counter()
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                preexec_fn=self._limit_resources if (os.name != 'nt' and resource) else None
            )
            return {
                "status": "Success" if result.returncode == 0 else "Runtime Error",
                "execution_time": round(time.perf_counter() - start_time, 4),
                "stdout_preview": result.stdout[:100].strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {"status": "Timeout", "message": f"Exceeded {self.timeout}s"}
        except Exception as e:
            return {"status": "Exception", "message": str(e)}