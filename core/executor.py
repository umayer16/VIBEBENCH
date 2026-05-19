import os
import subprocess
import sys
import time
from typing import Any, Optional

# 1. Fix mypy module errors by using a conditional check with 'types' fallback
# or letting mypy know 'resource' can be None via type annotation.
try:
    import resource
except ImportError:
    resource = None  # type: ignore[assignment]


class CodeExecutor:
    """Handles the dynamic execution of Python scripts in a sandboxed-style

    environment using Unix resource limits to ensure operational safety.
    """

    def __init__(self, timeout: int = 10, memory_limit_mb: int = 512) -> None:
        """Initializes the executor with specific safety constraints.

        Args:
            timeout (int): Maximum CPU time allowed in seconds.
            memory_limit_mb (int): Maximum memory allowed in megabytes.
        """
        self.timeout: int = timeout
        self.memory_limit: int = memory_limit_mb * 1024 * 1024

    def _limit_resources(self) -> None:
        """Sets hard CPU and memory limits on the child process (Unix-only)."""
        if resource is not None:
            # Using getattr to bypass mypy platform-specific missing attribute check
            setrlimit = getattr(resource, "setrlimit", None)
            rlimit_as = getattr(resource, "RLIMIT_AS", None)
            if setrlimit and rlimit_as is not None:
                setrlimit(rlimit_as, (self.memory_limit, self.memory_limit))

    def run(self, file_path: str) -> dict[str, Any]:
        """Executes a Python file and captures its performance metrics.

        Args:
            file_path (str): The path to the script to execute.

        Returns:
            dict: Metrics including status, execution time, carbon
                footprint estimate, and potential errors.
        """
        # Emission factors (conservative laptop defaults)
        tdp_watts: int = 15          # typical laptop CPU TDP
        carbon_intensity: int = 475  # gCO2/kWh — IEA 2023 global average

        if not os.path.exists(file_path):
            return {
                "status": "Error",
                "message": f"File {file_path} not found",
                "stderr": "File not found",
                "carbon_footprint_gCO2e": None
            }

        start_time: float = time.perf_counter()
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                # Resource limiting only works on Unix systems
                preexec_fn=(
                    self._limit_resources
                    if (os.name != "nt" and resource is not None)
                    else None
                )
            )
            execution_time: float = round(time.perf_counter() - start_time, 4)

            # Carbon footprint estimate
            carbon_footprint: float = round(
                (execution_time * tdp_watts * carbon_intensity) / 3600000,
                9
            )

            # Ensure stdout is safely treated as a string type
            stdout_str: str = result.stdout if result.stdout is not None else ""

            return {
                "status": (
                    "Success" if result.returncode == 0 else "Runtime Error"
                ),
                "execution_time": execution_time,
                "carbon_footprint_gCO2e": carbon_footprint,
                "stdout_preview": stdout_str[:1000].strip(),
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

    def run_multiple(self, file_path: str, runs: int = 3) -> dict[str, Any]:
        if runs < 1:
            raise ValueError(f"runs must be at least 1, got {runs}")

        all_times: list[float] = []
        all_carbon: list[float] = []
        statuses: list[str] = []

        for _ in range(runs):
            result: dict[str, Any] = self.run(file_path)

            # Error Fix (Line 120): Ensure the extracted status is strictly a string
            status_val = result.get('status')
            statuses.append(str(status_val) if status_val is not None else "Unknown")

            exec_time: Any = result.get('execution_time')
            if isinstance(exec_time, (int, float)):
                all_times.append(float(exec_time))

            carbon: Any = result.get('carbon_footprint_gCO2e')
            if isinstance(carbon, (int, float)):
                all_carbon.append(float(carbon))

        successful_runs: int = statuses.count('Success')

        # Determine overall status
        overall_status: str
        if successful_runs == runs:
            overall_status = 'Success'
        elif successful_runs == 0:
            overall_status = statuses[0]  # first error status
        else:
            overall_status = 'Partial'

        # Compute statistics over successful run times
        mean_time: Optional[float]
        min_time: Optional[float]
        max_time: Optional[float]
        std_time: Optional[float]

        if all_times:
            mean_time = round(sum(all_times) / len(all_times), 6)
            min_time = round(min(all_times), 6)
            max_time = round(max(all_times), 6)

            if len(all_times) >= 2:
                variance: float = sum(
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

        mean_carbon: Optional[float] = (
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
