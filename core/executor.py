import subprocess
import time
import os
import sys

try:
    import resource
except ImportError:
    resource = None


class CodeExecutor:
    """
    Handles the dynamic execution of Python
    scripts in a sandboxed-style environment
    using Unix resource limits to ensure
    operational safety.
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
        """Sets hard CPU and memory limits
        on the child process (Unix-only)."""
        if resource:
            resource.setrlimit(
                resource.RLIMIT_AS, (self.memory_limit, self.memory_limit)
            )

    def run(self, file_path):
        """
        Executes a Python file and captures its performance metrics.

        Args:
            file_path (str): The path to the script to execute.

        Returns:
            dict: Metrics including status, execution time, carbon
                footprint estimate, and potential errors.

                carbon_footprint_gCO2e is computed as:
                      execution_time_sec * TDP_WATTS * CARBON_INTENSITY
                    / 3_600_000
                where TDP_WATTS=15 (typical laptop CPU) and
                CARBON_INTENSITY=475 gCO2/kWh (IEA 2023 global average).
        """
        # Emission factors (conservative laptop defaults)
        TDP_WATTS = 15          # typical laptop CPU TDP
        CARBON_INTENSITY = 475  # gCO2/kWh — IEA 2023 global average

        if not os.path.exists(file_path):
            return {
                "status": "Error",
                "message": f"File {file_path} not found",
                "stderr": "File not found",
                "carbon_footprint_gCO2e": None
            }

        start_time = time.perf_counter()
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                # Resource limiting only works on Unix systems
                preexec_fn = (
                    self._limit_resources
                    if (os.name != "nt" and resource)
                    else None
                )
            )
            execution_time = round(time.perf_counter() - start_time, 4)

            # Carbon footprint estimate
            # Formula: time(s) * power(W) * carbon_intensity(gCO2/kWh) / 3,600,000
            carbon_footprint = round(
                (execution_time * TDP_WATTS * CARBON_INTENSITY) / 3600000,
                9
            )

            return {
                "status": "Success" if result.returncode == 0 else "Runtime Error",
                "execution_time": execution_time,
                "carbon_footprint_gCO2e": carbon_footprint,
                "stdout_preview": (result.stdout or "")[:1000].strip(),
                "stderr": (result.stderr or "").strip(),
                "stdout": result.stdout
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "Timeout",
                "message": f"Exceeded {self.timeout}s",
                "stderr": "Execution timed out",
                "execution_time": float(self.timeout),
                "carbon_footprint_gCO2e": None
            }
        except Exception as e:
            return {
                "status": "Exception",
                "message": str(e),
                "stderr": str(e),
                "execution_time": round(time.perf_counter() - start_time, 4),
                "carbon_footprint_gCO2e": None
            }

    def run_multiple(self, file_path, runs=3):
        if runs < 1:
            raise ValueError(f"runs must be at least 1, got {runs}")

        all_times = []
        all_carbon = []
        statuses = []

        for _ in range(runs):
            result = self.run(file_path)
            statuses.append(result.get('status'))

            exec_time = result.get('execution_time')
            if isinstance(exec_time, (int, float)):
                all_times.append(exec_time)

            carbon = result.get('carbon_footprint_gCO2e')
            if isinstance(carbon, (int, float)):
                all_carbon.append(carbon)

        successful_runs = statuses.count('Success')

        # Determine overall status
        if successful_runs == runs:
            overall_status = 'Success'
        elif successful_runs == 0:
            overall_status = statuses[0]  # first error status
        else:
            overall_status = 'Partial'

        # Compute statistics over successful run times
        if all_times:
            mean_time = round(sum(all_times) / len(all_times), 6)
            min_time = round(min(all_times), 6)
            max_time = round(max(all_times), 6)

            if len(all_times) >= 2:
                variance = sum(
                    (t - mean_time) ** 2 for t in all_times
                ) / (len(all_times) - 1)
                std_time = round(variance ** 0.5, 6)
            else:
                std_time = None
        else:
            mean_time = None
            min_time = None
            max_time = None
            std_time = None

        mean_carbon = (
            round(sum(all_carbon) / len(all_carbon), 9)
            if all_carbon else None
        )

        return {
            'status': overall_status,
            'execution_time': mean_time,
            'execution_time_std': std_time,
            'execution_time_min': min_time,
            'execution_time_max': max_time,
            'successful_runs': successful_runs,
            'total_runs': runs,
            'carbon_footprint_gCO2e': mean_carbon,
        }


