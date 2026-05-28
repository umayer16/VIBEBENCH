# Changelog

All notable changes to VibeBench will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Nothing yet.

---

## [1.5.0] — 2026-05-25

## Added

- **flake8 enforcement in CI** — lint step added to GitHub Actions
  workflow before test step. PRs that introduce PEP 8 violations
  cannot be merged. Configuration in `setup.cfg`: max line length
  88, W503 ignored, `datasets/` excluded.

- **mypy type checking in CI** — type check step added to GitHub
  Actions workflow. All public methods in `core/` modules have
  return type annotations and parameter type hints. Run with
  `--ignore-missing-imports` to avoid third-party stub issues.

- **Type hints throughout `core/`** — `core/analyzer.py`,
  `core/executor.py`, `core/reporter.py`, `core/openai_generator.py`,
  `core/groq_generator.py` all have full type annotations on public
  methods. Return types, parameter types, and local variable
  annotations added.

- **Pre-commit hooks** — `.pre-commit-config.yaml` added with eight
  hooks: trailing-whitespace, end-of-file-fixer, check-yaml,
  check-json, check-merge-conflict, debug-statements, flake8, mypy.
  Install with: `pip install pre-commit && pre-commit install`.

- **Self-audit results** — `docs/self-audit.md` documents VibeBench
  evaluated against its own source code. All seven source files
  achieve 100% docstring coverage and 0 bad practices after fixes
  applied during audit. Average complexity: 5.72.

- **Updated leaderboard figure** — `figures/leaderboard_sample.png`
  replaced with 10-task 3-run benchmark results showing CO₂e column,
  Runs column, and ranking by success rate. JOSS paper recompiled
  with updated figure and caption.

- **TASK-010 human baseline** — `datasets/human_samples/TASK-010_manual.py`
  added. Demonstrates correct async HTTP dependency handling:
  guards against missing aiohttp with try/except ImportError,
  returns structured error dicts rather than raising exceptions.

### Fixed

- **`vibebench.py` analyze command UnicodeDecodeError** — file opened
  without `encoding='utf-8'`, causing cp1252 decode failure on Windows
  for files containing UTF-8 special characters (CO₂, →, etc.).
  Fixed by adding `encoding='utf-8'` to the open() call.

- **`core/reporter.py` complexity** — `generate_markdown()` had
  complexity 24, `compare_runs()` had complexity 36 — both above
  McCabe's high-risk threshold of 10. Refactored to extract helper
  methods: `_aggregate_model_stats()`, `_format_summary_row()`,
  `_format_detail_row()`, `_aggregate_run()`, `_format_delta()`,
  `_build_comparison_row()`. Average complexity dropped to 9.18.

- **`core/analyzer.py`** — TODO comment removed (triggered own bad
  practice detector).

- **`core/executor.py`** — `run_multiple()` missing docstring added.

- **Generator `main()` functions** — docstrings added to `main()`
  in all three generator modules (gemini, groq, openai).

- **`vibebench.py`** — `main()` and `_print_verbose()` missing
  docstrings added. Coverage: 71.43% → 100.0%.

- **OpenAI generator mock tests** — dependency injection pattern
  adopted (`_client` parameter). Eliminates need for `patch()` and
  prevents real API calls during testing.

### Changed

- `core/reporter.py` refactored — helper methods extracted from
  `generate_markdown()` and `compare_runs()` for maintainability.
- All source files now pass self-audit: 100% docstring coverage,
  0 bad practices, all complexity scores below McCabe threshold of 10.

---

## [1.4.0] — 2026-05-18

### Added

- **Statistical significance testing** — `compare_models_statistically()`
  in `core/reporter.py` performs pairwise two-sided Mann-Whitney U tests
  between all model pairs for execution time and complexity metrics.
  `generate_significance_report()` produces a Markdown table of p-values.
  Differences are considered significant at p < 0.05.

- **`report` subcommand** — new CLI subcommand in `vibebench.py` for
  generating reports from existing benchmark JSON files without re-running
  the full benchmark. Flags: `--leaderboard`, `--significance`,
  `--compare FILE_A FILE_B`.

- **`--compare` flag** — `vibebench report --compare run1.json run2.json`
  produces a regression/improvement report showing delta in success rate,
  average complexity, and average execution time between two benchmark runs.
  Models added or dropped between runs are highlighted.

- **`core/openai_generator.py`** — OpenAI GPT-4o API support for benchmark
  code generation, completing the three-provider generator suite (Gemini,
  Groq, OpenAI). Follows identical five-function pattern to existing
  generators. Optional dependency: `openai>=1.0.0`.

- **`docs/` tutorial directory** — three tutorial files targeting external
  researchers: `adding-a-model.md`, `adding-a-task.md`,
  `interpreting-results.md`. Index at `docs/README.md`. Directly satisfies
  the JOSS reviewer checklist requirement for documentation beyond the README.

- **Carbon footprint estimation** — `carbon_footprint_gCO2e` field added to
  every benchmark record. Formula: `execution_time × 15W × 475 gCO₂/kWh
  ÷ 3,600,000`. Defaults assume a 15W laptop CPU and IEA 2023 global average
  carbon intensity. Documented as an order-of-magnitude estimate for relative
  comparison. Total CO₂e column added to leaderboard summary table.

- **`--runs N` reproducibility flag** — `vibebench benchmark --runs 3`
  executes each file N times and reports mean, standard deviation (Bessel-
  corrected), minimum, and maximum execution time. `run_multiple()` method
  added to `CodeExecutor`. Std dev displayed as `mean ± std` in verbose
  output and detailed leaderboard table.

- **`outreach/` directory** — Reddit post drafts, blog post draft, and
  professor email template prepared for arXiv preprint promotion.

- **arXiv preprint submitted** — "Beyond Correctness: A Holistic Quality
  Audit of LLM-Generated Python Code Using VibeBench" submitted to arXiv
  cs.SE on May 13, 2026. Awaiting moderation.

- **10-task benchmark dataset** — model outputs collected for TASK-006
  through TASK-010 from ChatGPT, Gemini, and Claude. Full benchmark now
  covers 10 tasks across 7 systems (3 models fully evaluated on all 10
  tasks, 4 models evaluated on original 5 tasks).

## Fixed

- **Leaderboard column mismatch** — summary table header had 5 columns
  but rows had 6 values. Fixed in `core/reporter.py`.
- **`report` subcommand handler missing** — `elif args.command == "report"`
  block was absent from `vibebench.py`. Fixed.
- **OpenAI generator mock patching** — `OpenAI` imported inside function
  body prevented `unittest.mock.patch` from intercepting it. Moved to
  module-level `try/except` import.
- **`TASK-008_manual.py` Runtime Error** — human baseline created
  `sample.json` in `__main__` block rather than using a self-contained
  test file. Fixed to create and clean up a temporary file.

## Changed

- `core/reporter.py` leaderboard sorted by success rate descending
  (previously sorted by model name alphabetically).
- Detailed file analysis table now includes Runs and std dev columns
  when `--runs N > 1` is used.
- `--input` flag on `report` subcommand changed from required to optional
  (not needed when using `--compare`).
- `pyproject.toml` now includes optional `[llm]` dependency group:
  `pip install vibebench[llm]` installs all three generator SDKs.

## Dependencies

- Added `scipy>=1.11.0` as a core dependency for statistical testing.
- Added `openai>=1.0.0` to optional `[llm]` dependency group.

---

## [1.3.0] — 2026-05-03

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

## Fixed

- Leaderboard now sorted by success rate descending in `reporter.py` (#10)
- Paper section headings corrected for JOSS compliance — `# Software design`
  lowercase d, all required sections present (#1, #2)
- `figures/architecture.png` replaced with clean publication-quality
  architecture diagram (#3)
- `figures/leaderboard_sample.png` updated with all 7 models sorted
  by success rate (#3)
- `save_report()` indentation corrected — was accidentally at module level
- Paper word count expanded from 531 to ~1450 words

## Changed

- Python requirement updated from 3.8+ to 3.9+
- Installation method updated to `pip install .` in README.md
- `--cov-omit` configuration moved to `pyproject.toml` `[tool.coverage.run]`

---

## [1.2.0] — 2026-03-09

## Added

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

## Fixed

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

## Changed

- `datasets/` directory restructured: AI samples organised under
  `datasets/ai_samples/<model>/` and human baseline under
  `datasets/human_samples/`
- Human baseline formally labelled `"HUMAN_BASELINE (Reference)"` in reports
  for comparative integrity

---

## [1.1.0] — 2026-02-28

## Added

- Full `pytest` test suite in `tests/test_analyzer.py` covering Halstead
  metrics, bad practice detection, and docstring coverage across 15 test cases
- `tests/test_core.py` with smoke tests for credential detection and docstring
  coverage
- Duplicate import detection in `CodeAnalyzer.detect_bad_practices()` covering
  both `import x` and `from x import y` forms

## Fixed

- `CodeExecutor` resource limiting now skips `preexec_fn` on Windows (`os.name
  == 'nt'`) and when the `resource` module is unavailable, preventing import
  errors on non-Unix platforms
- Hardcoded credential regex tightened to require at least 8 characters,
  reducing false positives on short string assignments

## Changed

- `core/reporter.py` updated to handle `"Error"` strings in numeric fields
  gracefully when computing averages for the leaderboard summary table

---

## [1.0.0] — 2026-02-24

## Added

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

[Unreleased]: https://github.com/umayer16/VIBEBENCH/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/umayer16/VIBEBENCH/releases/tag/v1.3.0
[1.2.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/umayer16/VIBEBENCH/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/umayer16/VIBEBENCH/releases/tag/v1.0.0
