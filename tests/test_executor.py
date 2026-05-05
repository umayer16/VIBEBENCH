import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.executor import CodeExecutor


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