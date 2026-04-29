import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.analyzer import CodeAnalyzer


# --- Test fixtures ---

SIMPLE_CODE = """
def add(a, b):
    \"\"\"Adds two numbers.\"\"\"
    return a + b

def subtract(a, b):
    return a - b
"""

FULLY_DOCUMENTED_CODE = """
def foo():
    \"\"\"Does foo.\"\"\"
    pass

class Bar:
    \"\"\"A bar class.\"\"\"
    pass
"""

UNDOCUMENTED_CODE = """
def foo():
    pass

def bar():
    pass
"""

CODE_WITH_CREDENTIALS = """
api_key = "abcdef1234567890"
"""

CODE_WITH_TODO = """
def process():
    # TODO: insert logic here
    pass
"""

CODE_WITH_GHOST_COMMENT = """
def process():
    #
    pass
"""

CODE_WITH_DUPLICATE_IMPORTS = """
import os
import os
"""

CODE_WITH_DUPLICATE_FROM_IMPORTS = """
from os import path
from os import path
"""

SYNTAX_ERROR_CODE = """
def broken(:
    pass
"""

SCRIPT_NO_FUNCTIONS = """
x = 1 + 2
print(x)
"""


# --- Halstead Metrics Tests ---

class TestHalsteadMetrics:

    def test_returns_dict_with_expected_keys(self):
        analyzer = CodeAnalyzer(SIMPLE_CODE)
        result = analyzer.calculate_halstead_metrics()
        assert isinstance(result, dict)
        assert "vocabulary" in result
        assert "volume" in result

    def test_syntax_error_returns_error_string(self):
        analyzer = CodeAnalyzer(SYNTAX_ERROR_CODE)
        result = analyzer.calculate_halstead_metrics()
        assert result == "Syntax Error"

    def test_volume_is_positive(self):
        analyzer = CodeAnalyzer(SIMPLE_CODE)
        result = analyzer.calculate_halstead_metrics()
        assert result["volume"] > 0

    def test_vocabulary_is_positive(self):
        analyzer = CodeAnalyzer(SIMPLE_CODE)
        result = analyzer.calculate_halstead_metrics()
        assert result["vocabulary"] > 0


# --- Bad Practices Tests ---

class TestDetectBadPractices:

    def test_detects_hardcoded_credentials(self):
        analyzer = CodeAnalyzer(CODE_WITH_CREDENTIALS)
        findings = analyzer.detect_bad_practices()
        assert any("credential" in f.lower() for f in findings)

    def test_detects_todo_placeholder(self):
        analyzer = CodeAnalyzer(CODE_WITH_TODO)
        findings = analyzer.detect_bad_practices()
        assert any("placeholder" in f.lower() or "todo" in f.lower() for f in findings)

    def test_detects_ghost_comments(self):
        analyzer = CodeAnalyzer(CODE_WITH_GHOST_COMMENT)
        findings = analyzer.detect_bad_practices()
        assert any("ghost" in f.lower() for f in findings)

    def test_detects_duplicate_imports(self):
        analyzer = CodeAnalyzer(CODE_WITH_DUPLICATE_IMPORTS)
        findings = analyzer.detect_bad_practices()
        assert any("duplicate" in f.lower() for f in findings)

    def test_detects_duplicate_from_imports(self):
        analyzer = CodeAnalyzer(CODE_WITH_DUPLICATE_FROM_IMPORTS)
        findings = analyzer.detect_bad_practices()
        assert any("duplicate" in f.lower() for f in findings)

    def test_clean_code_returns_no_findings(self):
        analyzer = CodeAnalyzer(SIMPLE_CODE)
        findings = analyzer.detect_bad_practices()
        assert findings == []
    def test_detects_mutable_default_list(self):
        code = "def process(items=[]):\n    return items"
        analyzer = CodeAnalyzer(code)
        findings = analyzer.detect_bad_practices()
        assert any("mutable default" in f.lower() for f in findings)
    def test_detects_mutable_default_dict(self):
        code = "def fibonacci(n, memo={}):\n    return memo.get(n, n)"
        analyzer = CodeAnalyzer(code)
        findings = analyzer.detect_bad_practices()
        assert any("mutable default" in f.lower() for f in findings)
    def test_clean_function_no_mutable_default(self):
            code = "def fibonacci(n, memo=None):\n    return n"
            analyzer = CodeAnalyzer(code)
            findings = analyzer.detect_bad_practices()
            assert not any("mutable default" in f.lower() for f in findings)


# --- Docstring Coverage Tests ---

class TestDocstringCoverage:

    def test_fully_documented_returns_100(self):
        analyzer = CodeAnalyzer(FULLY_DOCUMENTED_CODE)
        result = analyzer.get_docstring_coverage()
        assert result == 100.0

    def test_undocumented_returns_0(self):
        analyzer = CodeAnalyzer(UNDOCUMENTED_CODE)
        result = analyzer.get_docstring_coverage()
        assert result == 0.0

    def test_partial_coverage(self):
        analyzer = CodeAnalyzer(SIMPLE_CODE)
        result = analyzer.get_docstring_coverage()
        assert 0.0 < result < 100.0

    def test_no_functions_returns_none(self):
        analyzer = CodeAnalyzer(SCRIPT_NO_FUNCTIONS)
        result = analyzer.get_docstring_coverage()
        assert result is None

    def test_syntax_error_returns_0(self):
        analyzer = CodeAnalyzer(SYNTAX_ERROR_CODE)
        result = analyzer.get_docstring_coverage()
        assert result == 0.0

