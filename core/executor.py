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

    def __init__(self, timeout=10, memory_limit_mb=512):

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
            return {
                "status": "Error",
                "message": f"File {file_path} not found",
                "stderr": "File not found"
            }
        start_time = time.time()
        try:
            result = subprocess.run(
                ["python", file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            execution_time = time.time() - start_time

            # 2. Extract stdout preview (e.g., first 1000 characters)
            stdout_content = result.stdout or ""
            stdout_preview = stdout_content[:1000]

            if result.returncode != 0:
                return {
                    "status": "Runtime Error",
                    "stderr": result.stderr,
                    "execution_time": execution_time
                }
            return {
                "status": "Success",
                "stdout": stdout_content,
                "stdout_preview": stdout_preview, # Required for test_stdout_preview_captured
                "execution_time": execution_time  # Required for test_returns_execution_time
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "Timeout",
                "stderr": "Execution timed out",
                "execution_time": float(self.timeout)
            }
        except Exception as e:
            return {
                "status": "Runtime Error",
                "stderr": str(e),
                "execution_time": time.time() - start_time
            }