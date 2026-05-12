import json
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.reporter import VibeReporter


# --- Fixtures ---

SAMPLE_DATA = [
    {
        "model": "chatgpt",
        "category": "AI Synthesis",
        "file": "TASK-001_chatgpt.py",
        "complexity": 1.8,
        "docstring_coverage": 0.0,
        "bad_practices_count": 0,
        "execution_time_sec": 0.06,
        "vibebench_score": 0.18,
        "status": "Success",
        "timestamp": "2026-05-05T10:00:00"
    },
    {
        "model": "chatgpt",
        "category": "AI Synthesis",
        "file": "TASK-002_chatgpt.py",
        "complexity": 7.0,
        "docstring_coverage": 100.0,
        "bad_practices_count": 0,
        "execution_time_sec": 0.39,
        "vibebench_score": 0.72,
        "status": "Success",
        "timestamp": "2026-05-05T10:00:01"
    },
    {
        "model": "gemini",
        "category": "AI Synthesis",
        "file": "TASK-001_gemini.py",
        "complexity": 2.0,
        "docstring_coverage": 75.0,
        "bad_practices_count": 0,
        "execution_time_sec": 0.05,
        "vibebench_score": 0.21,
        "status": "Success",
        "timestamp": "2026-05-05T10:00:02"
    },
    {
        "model": "grok",
        "category": "AI Synthesis",
        "file": "TASK-001_grok.py",
        "complexity": 2.2,
        "docstring_coverage": 60.0,
        "bad_practices_count": 0,
        "execution_time_sec": 0.10,
        "vibebench_score": None,
        "status": "Runtime Error",
        "timestamp": "2026-05-05T10:00:03"
    },
]


@pytest.fixture
def json_report_file(tmp_path):
    """Creates a temporary JSON report file for testing."""
    report_path = tmp_path / "test_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_DATA, f)
    return str(report_path)


@pytest.fixture
def reporter(json_report_file):
    """Creates a VibeReporter instance from the test JSON file."""
    return VibeReporter(json_report_file)


# --- Initialisation Tests ---

class TestVibeReporterInit:

    def test_loads_valid_json_file(self, json_report_file):
        reporter = VibeReporter(json_report_file)
        assert len(reporter.data) == 4

    def test_raises_on_missing_file(self, tmp_path):
        missing = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            VibeReporter(missing)

    def test_data_contains_expected_models(self, reporter):
        models = {entry['model'] for entry in reporter.data}
        assert 'chatgpt' in models
        assert 'gemini' in models
        assert 'grok' in models


# --- Markdown Generation Tests ---

class TestGenerateMarkdown:

    def test_generates_markdown_file(self, reporter, tmp_path):
        output_path = str(tmp_path / "leaderboard.md")
        reporter.generate_markdown(output_file=output_path)
        assert os.path.exists(output_path)

    def test_markdown_contains_model_names(self, reporter, tmp_path):
        output_path = str(tmp_path / "leaderboard.md")
        reporter.generate_markdown(output_file=output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "CHATGPT" in content
        assert "GEMINI" in content
        assert "GROK" in content

    def test_markdown_contains_table_headers(self, reporter, tmp_path):
        output_path = str(tmp_path / "leaderboard.md")
        reporter.generate_markdown(output_file=output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "Avg Complexity" in content
        assert "Avg Exec Time" in content
        assert "Doc Coverage" in content

    def test_markdown_contains_status_values(self, reporter, tmp_path):
        output_path = str(tmp_path / "leaderboard.md")
        reporter.generate_markdown(output_file=output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "Success" in content
        assert "Runtime Error" in content

    def test_empty_data_does_not_crash(self, tmp_path):
        empty_file = tmp_path / "empty.json"
        with open(empty_file, 'w') as f:
            json.dump([], f)
        reporter = VibeReporter(str(empty_file))
        output_path = str(tmp_path / "leaderboard.md")
        # Should not raise, just print warning
        reporter.generate_markdown(output_file=output_path)

    def test_handles_none_numeric_fields(self, reporter, tmp_path):
        """vibebench_score can be None — reporter should handle it."""
        output_path = str(tmp_path / "leaderboard.md")
        # Should not raise even though grok entry has vibebench_score=None
        reporter.generate_markdown(output_file=output_path)
        assert os.path.exists(output_path)

class TestStatisticalTesting:
    def test_compare_models_returns_dict(self, reporter):
        results = reporter.compare_models_statistically(
            metric='execution_time_sec'
        )
        assert isinstance(results, dict)
    
    def test_compare_models_has_model_pairs(self, reporter):
        results = reporter.compare_models_statistically(
            metric='execution_time_sec'
        )
        # Should have at least one model pair
        total_pairs = sum(len(v) for v in results.values())
        assert total_pairs > 0
    
    def test_significance_result_has_required_keys(self, reporter):
        results = reporter.compare_models_statistically(
            metric='execution_time_sec'
        )
        for model_a, comparisons in results.items():
            for model_b, res in comparisons.items():
                if res.get('p_value') is not None:
                    assert 'u_statistic' in res
                    assert 'p_value' in res
                    assert 'significant' in res
                    assert isinstance(res['significant'], bool)
    def test_p_value_between_0_and_1(self, reporter):
        results = reporter.compare_models_statistically(
            metric='complexity'
        )
        for model_a, comparisons in results.items():
            for model_b, res in comparisons.items():
                if res.get('p_value') is not None:
                    assert 0.0 <= res['p_value'] <= 1.0
    def test_generates_significance_report_file(
        self, reporter, tmp_path
    ):
        output_path = str(
            tmp_path / "significance_report.md"
        )
        reporter.generate_significance_report(
            output_file=output_path
        )
        assert os.path.exists(output_path)
    
    def test_significance_report_contains_headers(
        self, reporter, tmp_path
    ):
        output_path = str(
            tmp_path / "significance_report.md"
        )
        reporter.generate_significance_report(
            output_file=output_path
        )
        with open(output_path, 'r') as f:
            content = f.read()
        assert "Execution Time" in content
        assert "Cyclomatic Complexity" in content
        assert "p-value" in content
