from core.analyzer import CodeAnalyzer
import pytest

def test_docstring_coverage():
    code = "def test():\n    '''Has docstring'''\n    pass"
    analyzer = CodeAnalyzer(code)
    assert analyzer.get_docstring_coverage() == 100.0

def test_bad_practice_detection():
    code = "api_key = 'AIZA_1234567890'"
    analyzer = CodeAnalyzer(code)
    assert "Potential hardcoded credential detected." in analyzer.detect_bad_practices()