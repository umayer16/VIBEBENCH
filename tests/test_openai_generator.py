"""
Tests for core/openai_generator.py

Note: These tests mock the OpenAI API client to avoid requiring
a real API key in CI. The tests verify the generator's file I/O,
task loading, and code-cleaning logic independently of the API.
"""

import os
import json
from openai import OpenAI, api_key
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_tasks_file(tmp_path):
    """Creates a minimal tasks JSON file for testing."""
    tasks = [
        {
            "id": "TASK-001",
            "category": "Data Structures",
            "difficulty": "Easy",
            "prompt": "Write a Python function to reverse a linked list."
        },
        {
            "id": "TASK-002",
            "category": "Algorithms",
            "difficulty": "Medium",
            "prompt": "Implement binary search."
        }
    ]
    path = str(tmp_path / "test_prompts.json")
    with open(path, 'w') as f:
        json.dump(tasks, f)
    return path


@pytest.fixture
def output_dir(tmp_path):
    """Returns a temporary output directory."""
    d = str(tmp_path / "datasets")
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Tests for load_tasks()
# ---------------------------------------------------------------------------

class TestLoadTasks:

    def test_loads_valid_file(self, sample_tasks_file):
        from core.openai_generator import load_tasks
        tasks = load_tasks(sample_tasks_file)
        assert isinstance(tasks, list)
        assert len(tasks) == 2

    def test_raises_on_missing_file(self):
        from core.openai_generator import load_tasks
        with pytest.raises(FileNotFoundError):
            load_tasks("nonexistent_tasks.json")

    def test_returns_correct_task_ids(self, sample_tasks_file):
        from core.openai_generator import load_tasks
        tasks = load_tasks(sample_tasks_file)
        ids = [t['id'] for t in tasks]
        assert "TASK-001" in ids
        assert "TASK-002" in ids


# ---------------------------------------------------------------------------
# Tests for save_generated_code()
# ---------------------------------------------------------------------------

class TestSaveGeneratedCode:

    def test_creates_output_file(self, output_dir):
        from core.openai_generator import save_generated_code
        code = "def add(a, b):\n    return a + b\n"
        path = save_generated_code(
            code, "gpt-4o", "TASK-001", output_dir
        )
        assert os.path.exists(path)

    def test_file_contains_correct_code(self, output_dir):
        from core.openai_generator import save_generated_code
        code = "def hello():\n    print('hello')\n"
        path = save_generated_code(
            code, "gpt-4o", "TASK-001", output_dir
        )
        with open(path) as f:
            content = f.read()
        assert content == code

    def test_model_name_sanitised_in_path(self, output_dir):
        from core.openai_generator import save_generated_code
        path = save_generated_code(
            "pass", "gpt-4o-mini", "TASK-001", output_dir
        )
        # Hyphens and dots should be replaced with underscores
        assert "gpt_4o_mini" in path

    def test_creates_model_subdirectory(self, output_dir):
        from core.openai_generator import save_generated_code
        save_generated_code("pass", "gpt-4o", "TASK-001", output_dir)
        model_dir = os.path.join(output_dir, "gpt_4o")
        assert os.path.isdir(model_dir)


# ---------------------------------------------------------------------------
# Tests for generate_code_openai() — mocked
# ---------------------------------------------------------------------------

class TestGenerateCodeOpenAI:

    def generate_code_openai(self, prompt, model_name="gpt-4o"):
        if OpenAI is None:
            raise ImportError(
                "openai is not installed. "
                "Run: pip install openai"
            )

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY environment variable is not set. "
                "Get a key at https://platform.openai.com/api-keys"
            )
        client = OpenAI(api_key=api_key)

    def test_raises_without_api_key(self):
        from core.openai_generator import generate_code_openai
        with patch.dict(os.environ, {}, clear=True):
            # Remove OPENAI_API_KEY if present
            env = {
                k: v for k, v in os.environ.items()
                if k != 'OPENAI_API_KEY'
            }
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(EnvironmentError):
                    generate_code_openai("Write a function")

    def test_strips_markdown_fences(self):
        from core.openai_generator import generate_code_openai

        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "```python\ndef add(a, b):\n    return a + b\n```"
        )

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        # Inject mock client directly — no patching needed
        result = generate_code_openai(
            "Write add function",
            _client=mock_client
        )

        assert "```" not in result
        assert "def add" in result



    def test_returns_clean_code(self):
        from core.openai_generator import generate_code_openai

        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "def fibonacci(n):\n    return n if n <= 1 else "
            "fibonacci(n-1) + fibonacci(n-2)\n"
        )

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        result = generate_code_openai(
            "Write fibonacci",
            _client=mock_client
        )

        assert "def fibonacci" in result
