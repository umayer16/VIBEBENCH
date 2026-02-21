import subprocess
import time
import resource
import sys
import os

class CodeExecutor:
    def __init__(self, timeout=5, memory_limit_mb=512):
        self.timeout = timeout
        self.memory_limit = memory_limit_mb * 1024 * 1024  # Convert to bytes

    def _limit_resources(self):
        """Sets hard limits on the process to prevent system crashes."""
        # Limit CPU time
        resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
        # Limit Memory (Address Space)
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))

    def run(self, file_path):
        """
        Executes the file and returns performance metrics.
        """
        if not os.path.exists(file_path):
            return {"status": "Error", "message": "File not found"}

        start_time = time.perf_counter()
        
        try:
            # We use preexec_fn to apply resource limits ONLY to the child process
            # Note: resource limits via preexec_fn work on Linux/macOS. 
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                preexec_fn=self._limit_resources if os.name != 'nt' else None
            )
            
            end_time = time.perf_counter()
            
            return {
                "status": "Success" if result.returncode == 0 else "Runtime Error",
                "execution_time": round(end_time - start_time, 4),
                "stdout_preview": result.stdout[:100].strip(),
                "stderr": result.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {"status": "Timeout", "message": f"Exceeded {self.timeout}s"}
        except Exception as e:
            return {"status": "Exception", "message": str(e)}

# --- Quick Test ---
if __name__ == "__main__":
    # Create a dummy test file
    test_file = "temp_test.py"
    with open(test_file, "w") as f:
        f.write("print(sum(range(1_000_000)))")

    executor = CodeExecutor()
    print(f"--- Running Test: {test_file} ---")
    metrics = executor.run(test_file)
    print(metrics)
    
    # Cleanup
    if os.path.exists(test_file): os.remove(test_file)