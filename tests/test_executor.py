import os
import sys
# from unittest import result
import pytest
from core.executor import CodeExecutor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def executor():
    """Creates a CodeExecutor with a 5-second timeout."""
    return CodeExecutor(timeout=5)


# --- File Not Found Tests ---

class TestExecutorFileNotFound:

    def test_returns_error_for_missing_file(self, executor):
        result = executor.run("nonexistent_file_xyz.py")
        assert result["status"] == "Error"

    def test_error_message_mentions_not_found(self, executor):
        result = executor.run("nonexistent_file_xyz.py")
        assert "not found" in result.get("message", "").lower()


# --- Successful Execution Tests ---

class TestExecutorSuccess:

    def test_simple_print_succeeds(self, executor, tmp_path):
        script = tmp_path / "hello.py"
        script.write_text('print("hello world")\n')
        result = executor.run(str(script))
        assert result["status"] == "Success"

    def test_returns_execution_time(self, executor, tmp_path):
        script = tmp_path / "simple.py"
        script.write_text('x = 1 + 1\n')
        result = executor.run(str(script))
        assert isinstance(result.get("execution_time"), float)
        assert result["execution_time"] > 0

    def test_execution_time_is_reasonable(self, executor, tmp_path):
        script = tmp_path / "fast.py"
        script.write_text('pass\n')
        result = executor.run(str(script))
        # A simple pass statement should run in under 3 seconds
        assert result.get("execution_time", 999) < 3.0

    def test_stdout_preview_captured(self, executor, tmp_path):
        script = tmp_path / "output.py"
        script.write_text('print("VibeBench test output")\n')
        result = executor.run(str(script))
        assert result["status"] == "Success"
        assert "VibeBench test output" in result.get("stdout_preview", "")

    def test_carbon_footprint_present_on_success(self, tmp_path):
        """Successful runs should include a carbon_footprint_gCO2e field."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run(str(script))
        assert 'carbon_footprint_gCO2e' in result
        assert isinstance(result['carbon_footprint_gCO2e'], float)

    def test_carbon_footprint_is_positive(self, tmp_path):
        """Carbon footprint should always be a positive number."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run(str(script))
        assert result['carbon_footprint_gCO2e'] > 0

    def test_carbon_footprint_none_on_timeout(self, tmp_path):
        """Timed-out runs should have carbon_footprint_gCO2e = None."""
        script = tmp_path / "infinite.py"
        script.write_text("while True: pass\n")
        executor = CodeExecutor(timeout=1)
        result = executor.run(str(script))
        assert result['status'] == 'Timeout'
        assert result['carbon_footprint_gCO2e'] is None

    def test_carbon_footprint_scales_with_time(self, tmp_path):
        """A faster script should produce a smaller carbon footprint."""
        fast_script = tmp_path / "fast.py"
        fast_script.write_text("x = 1 + 1\n")

        slow_script = tmp_path / "slow.py"
        slow_script.write_text(
            "import time\ntime.sleep(0.1)\n"
        )

        executor = CodeExecutor(timeout=5)
        fast_result = executor.run(str(fast_script))
        slow_result = executor.run(str(slow_script))

        if (fast_result['carbon_footprint_gCO2e'] is not None
                and slow_result['carbon_footprint_gCO2e'] is not None):
            assert (
                fast_result['carbon_footprint_gCO2e']
                < slow_result['carbon_footprint_gCO2e']
            )


# --- Runtime Error Tests ---

class TestExecutorRuntimeError:

    def test_syntax_error_returns_runtime_error(self, executor, tmp_path):
        script = tmp_path / "broken.py"
        script.write_text('def broken(:\n    pass\n')
        result = executor.run(str(script))
        assert result["status"] == "Runtime Error"

    def test_exception_returns_runtime_error(self, executor, tmp_path):
        script = tmp_path / "raises.py"
        script.write_text('raise ValueError("intentional error")\n')
        result = executor.run(str(script))
        assert result["status"] == "Runtime Error"

    def test_division_by_zero_returns_runtime_error(self, executor, tmp_path):
        script = tmp_path / "divzero.py"
        script.write_text('x = 1 / 0\n')
        result = executor.run(str(script))
        assert result["status"] == "Runtime Error"


# --- Timeout Tests ---

class TestExecutorTimeout:

    def test_infinite_loop_times_out(self, tmp_path):
        # Use a very short timeout so the test does not hang
        fast_executor = CodeExecutor(timeout=2)
        script = tmp_path / "infinite.py"
        script.write_text('while True:\n    pass\n')
        result = fast_executor.run(str(script))
        assert result["status"] == "Timeout"


class TestRunMultiple:

    def test_returns_correct_keys(self, tmp_path):
        """run_multiple should return all expected keys."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=2)
        expected_keys = {
            'status', 'execution_time', 'execution_time_std',
            'execution_time_min', 'execution_time_max',
            'successful_runs', 'total_runs', 'carbon_footprint_gCO2e'
        }
        assert expected_keys.issubset(result.keys())

    def test_successful_runs_count(self, tmp_path):
        """successful_runs should equal runs for a healthy script."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=3)
        assert result['successful_runs'] == 3
        assert result['total_runs'] == 3

    def test_status_success_all_pass(self, tmp_path):
        """Status should be Success when all runs succeed."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=2)
        assert result['status'] == 'Success'

    def test_mean_time_is_float(self, tmp_path):
        """Mean execution time should be a float."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=2)
        assert isinstance(result['execution_time'], float)

    def test_std_none_for_single_run(self, tmp_path):
        """Std dev should be None when only one run is requested."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=1)
        assert result['execution_time_std'] is None

    def test_std_float_for_multiple_runs(self, tmp_path):
        """Std dev should be a float when runs >= 2."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=3)
        assert isinstance(result['execution_time_std'], float)

    def test_min_lte_mean_lte_max(self, tmp_path):
        """Min <= mean <= max must always hold."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        result = executor.run_multiple(str(script), runs=3)
        assert result['execution_time_min'] <= result['execution_time']
        assert result['execution_time'] <= result['execution_time_max']

    def test_invalid_runs_raises(self, tmp_path):
        """run_multiple should raise ValueError for runs < 1."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        with pytest.raises(ValueError):
            executor.run_multiple(str(script), runs=0)

    def test_single_run_backward_compatible(self, tmp_path):
        """runs=1 should produce same structure as run()."""
        script = tmp_path / "hello.py"
        script.write_text("print('hello')\n")
        executor = CodeExecutor(timeout=5)
        single = executor.run(str(script))
        multi = executor.run_multiple(str(script), runs=1)
        assert single['status'] == multi['status']
        assert isinstance(multi['execution_time'], float)
