# Changelog  

All notable changes to VibeBench will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.3.0] — 2026-05-05

### Added
- `calculate_vibebench_score()` method in `core/analyzer.py` implementing
  the composite Sigma metric defined in paper.md Mathematics section (#8)
- `vibebench_score` field included in all JSON benchmark output records (#8)
- `--export-csv` flag on benchmark command exports results as CSV
  alongside JSON output (#9)
- Mutable default argument detection added to `detect_bad_practices()`
  covering list, dict, and set defaults in function signatures (#7)
- `pyproject.toml` for proper Python packaging — `pip install .` now
  works and installs the `vibebench` CLI entry point (#13)
- Matrix CI testing across Python 3.9, 3.10, 3.11 with coverage
  reporting via pytest-cov (#11)
- `datasets/data_quality_notes.md` formally documenting dataset quality
  issues DQ-001 and DQ-002 with severity, evidence, and decision (#5, #6)
- Benchmark task set expanded from 5 to 10 tasks — TASK-006 through
  TASK-010 added with human baseline solutions (#14)
- CI status badge added to README.md
- `CITATION.cff` keywords field added for improved discoverability

### Fixed
- Leaderboard now sorted by success rate descending in `reporter.py` (#10)
- Paper section headings corrected for JOSS compliance — `# Software design`
  lowercase d, all required sections present (#1, #2)
- `figures/architecture.png` replaced with clean publication-quality
  architecture diagram (#3)
- `figures/leaderboard_sample.png` updated with all 7 models sorted
  by success rate (#3)
- `save_report()` indentation corrected — was accidentally at module level
- Paper word count expanded from 531 to ~1450 words

### Changed
- Python requirement updated from 3.8+ to 3.9+
- Installation method updated to `pip install .` in README.md
- `--cov-omit` configuration moved to `pyproject.toml` `[tool.coverage.run]`

---

## [1.2.0] — 2026-03-09

###Added
- Full multi-model benchmark results committed to the repository, comparing
  ChatGPT, Claude, Gemini, Grok, DeepSeek, and LLaMA 3.3 70B across 5 tasks
- `VibeBench_Leaderboard.md` with ranked results and per-task breakdown
- LLM generator modules: `core/gemini_generator.py` and `core/groq_generator.py`
  for programmatic code generation via the Gemini and Groq APIs
- `CITATION.cff` file for academic citation support
- CLI via `argparse` with two subcommands: `analyze` (single file) and
  `benchmark` (full multi-model suite)
- Comprehensive `README.md` with installation, quick start, output format,
  project structure, and citation instructions
- `.gitignore` to prevent committing secrets, cache files, and output JSONs
- `.env.example` documenting required API key environment variables
- `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
- GitHub Actions CI workflow (`.github/workflows/tests.yml`) running pytest
  on every push and pull request

### Fixed
- Halstead Volume formula corrected to track N1/N2 (total occurrences) and
  n1/n2 (unique counts) separately, as required by Halstead (1977)
- Expanded operator detection in `CodeAnalyzer` to cover bitwise, boolean,
  unary, and all comparison operators
- Ghost comment detection regex fixed to correctly match empty `#` lines
- Docstring coverage edge case fixed: files with no functions/classes now
  return `None` instead of raising a `ZeroDivisionError`
- `datetime` import in `core/reporter.py` moved to module level to prevent
  `NameError` when called from outside `__main__`
- Duplicate `bandit` and other entries removed from `requirements.txt`

### Changed
- `datasets/` directory restructured: AI samples organised under
  `datasets/ai_samples/<model>/` and human baseline under
  `datasets/human_samples/`
- Human baseline formally labelled `"HUMAN_BASELINE (Reference)"` in reports
  for comparative integrity

---

## [1.1.0] — 2026-02-28

### Added
- Full `pytest` test suite in `tests/test_analyzer.py` covering Halstead
  metrics, bad practice detection, and docstring coverage across 15 test cases
- `tests/test_core.py` with smoke tests for credential detection and docstring
  coverage
- Duplicate import detection in `CodeAnalyzer.detect_bad_practices()` covering
  both `import x` and `from x import y` forms

### Fixed
- `CodeExecutor` resource limiting now skips `preexec_fn` on Windows (`os.name
  == 'nt'`) and when the `resource` module is unavailable, preventing import
  errors on non-Unix platforms
- Hardcoded credential regex tightened to require at least 8 characters,
  reducing false positives on short string assignments

### Changed
- `core/reporter.py` updated to handle `"Error"` strings in numeric fields
  gracefully when computing averages for the leaderboard summary table

---

## [1.0.0] — 2026-02-24

### Added
- Initial public release of VibeBench
- `core/analyzer.py`: AST-based static analysis engine implementing:
  - Halstead Volume and Vocabulary metrics
  - Cyclomatic Complexity via `radon`
  - Docstring coverage for functions, async functions, and classes
  - Bad practice detection: hardcoded credentials, TODO/FIXME placeholders,
    ghost comments (empty `#` lines), duplicate imports
- `core/executor.py`: sandboxed dynamic execution using Unix `resource` module
  with configurable CPU time (`RLIMIT_CPU`) and memory (`RLIMIT_AS`) limits
- `core/reporter.py`: leaderboard and Markdown table generation from JSON
  benchmark output
- `vibebench.py`: main orchestration script walking the `datasets/` directory
  and producing timestamped JSON reports
- `datasets/prompts.json`: 5 benchmark task definitions across Data Structures,
  Cybersecurity, Algorithms, File I/O, and Math/Logic categories
- `datasets/ai_samples/`: initial code samples for ChatGPT, Claude, Gemini,
  Grok, DeepSeek, and LLaMA 3.3 70B
- `datasets/human_samples/`: human-authored baseline solutions for all 5 tasks
- `paper.md`: JOSS submission paper with Summary, Statement of Need, State of
  the Field, Software Design, Mathematics, and Acknowledgements sections
- `paper.bib`: bibliography with citations for HumanEval, MBPP,
  CodeSearchNet, Halstead (1977), and McCabe (1976)
- Zenodo DOI archived: `10.5281/zenodo.18758578`

---



[Unreleased]: https://github.com/umayer16/VIBEBENCH/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/umayer16/VIBEBENCH/releases/tag/v1.0.0
