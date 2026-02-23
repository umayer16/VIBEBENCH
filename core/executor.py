import subprocess
import time
import sys
import os

# Conditional import for Unix-only 'resource' module
try:
    import resource
except ImportError:
    resource = None

class CodeExecutor:
    def __init__(self, timeout=5, memory_limit_mb=512):
        self.timeout = timeout
        self.memory_limit = memory_limit_mb * 1024 * 1024  # Convert to bytes

    def _limit_resources(self):
        """Sets hard limits on the process (Unix only)."""
        if resource:
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))

    def run(self, file_path):
        if not os.path.exists(file_path):
            return {"status": "Error", "message": "File not found"}

        start_time = time.perf_counter()
        try:
            # preexec_fn is NOT supported on Windows
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