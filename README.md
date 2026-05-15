# VibeBench

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18758578.svg)](https://doi.org/10.5281/zenodo.18758578)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![status](https://joss.theoj.org/papers/e2f0068b712c24134f3c43abdb394eb4/status.svg)](https://joss.theoj.org/papers/e2f0068b712c24134f3c43abdb394eb4)
[![Tests](https://github.com/umayer16/VIBEBENCH/actions/workflows/tests.yml/badge.svg)](https://github.com/umayer16/VIBEBENCH/actions/workflows/tests.yml)

**VibeBench** is an automated, extensible Python framework for the holistic
evaluation of LLM-generated code. It goes beyond functional correctness by
integrating static quality heuristics with sandboxed dynamic execution to
measure the true production-readiness of AI-generated software.

---

## Why VibeBench?

Existing benchmarks like HumanEval and MBPP only check if code *runs correctly*.
VibeBench additionally checks if code is *maintainable, secure, and efficient* —
the metrics that matter in real-world software engineering.

| Metric | HumanEval | MBPP | VibeBench |
| --- | --- | --- | --- |
| Functional correctness | ✅ | ✅ | ✅ |
| Halstead complexity | ❌ | ❌ | ✅ |
| Cyclomatic complexity | ❌ | ❌ | ✅ |
| Docstring coverage | ❌ | ❌ | ✅ |
| Hardcoded credential detection | ❌ | ❌ | ✅ |
| Ghost comment detection | ❌ | ❌ | ✅ |
| Sandboxed execution with resource limits | ❌ | ❌ | ✅ |
| Operational parity vs human baseline | ❌ | ❌ | ✅ |

---

## Installation

**Requirements:** Python 3.9+, Unix-based OS (Linux/macOS) for
sandboxed execution features.

### Standard Install

```bash
git clone https://github.com/umayer16/VIBEBENCH.git
cd VIBEBENCH
pip install .
```

After installation, the `vibebench` command is available globally:

```bash
vibebench --help
```

### Development Install

For contributors who want changes to take effect immediately:

```bash
pip install -e ".[dev]"
```

### Optional LLM Generator Dependencies

To use the model code generators (Gemini, Groq, OpenAI):

```bash
pip install ".[llm]"

```

````text

Two important changes here: the Python requirement is now `3.9+` to match `pyproject.toml`, and the installation uses `pip install .` rather than `pip install -r requirements.txt`. Also note you removed `Python 3.8+` — `pyproject.toml` specifies `requires-python = ">=3.9"` and you should be consistent.

## Quick Start

### Analyze a single code snippet
```python
from core.analyzer import CodeAnalyzer

code = """
def add(a, b):
    return a + b
"""

analyzer = CodeAnalyzer(code)

print(analyzer.calculate_halstead_metrics())
# {'vocabulary': 4, 'volume': 8.0}

print(analyzer.get_docstring_coverage())
# 0.0

print(analyzer.detect_bad_practices())
# []
```

### Run the full benchmark
```bash
python vibebench.py
```

Results are saved as a timestamped JSON file (e.g. `vibebench_multimodel_20260224_1912.json`)
and a leaderboard is generated at `VibeBench_Leaderboard.md`.

---

## Output Format

VibeBench produces a JSON results file with the following structure per model:
```json
{
  "model": "gpt-4o",
  "task": "fibonacci",
  "halstead_volume": 42.5,
  "cyclomatic_complexity": 3,
  "docstring_coverage": 100.0,
  "bad_practices": [],
  "execution_success": true,
  "execution_time_ms": 12.4,
  "operational_parity": 0.95
}
```

---

## Leaderboard

Current benchmark results across evaluated models:

See [VibeBench_Leaderboard.md](VibeBench_Leaderboard.md) for full results.

---

## Project Structure
```
VIBEBENCH/
├── core/
│   ├── analyzer.py          # Static analysis engine (AST-based)
│   ├── executor.py          # Sandboxed dynamic execution
│   ├── reporter.py          # Leaderboard and visualization
│   ├── gemini_generator.py  # Gemini API code generator
│   ├── groq_generator.py    # Groq API code generator
│   └── openai_generator.py  # OpenAI API code generator
├── datasets/            # Benchmark task definitions
├── docs/
│   ├── adding-a-model.md        # Tutorial: add a new generator
│   ├── adding-a-task.md         # Tutorial: add a new task
│   └── interpreting-results.md  # Guide: understand the metrics
├── figures/             # Architecture and leaderboard figures
├── tests/               # pytest test suite
├── vibebench.py         # Main entry point
├── paper.md             # JOSS paper
└── requirements.txt
```

---

## Running Tests
```bash
pip install pytest
pytest tests/
```

---

## Reproducing Benchmark Results
To reproduce the findings from our v1.2.0 release:
1. Ensure your API keys are set in a `.env` file (see `.env.example`).
2. Run the full suite:
   ```bash
   python vibebench.py benchmark --tasks datasets/prompts.json --verbose

## Output Format

VibeBench produces a JSON results file with the following structure per file:

```json
{
  "schema_version": "1.1",
  "model": "chatgpt",
  "category": "AI Synthesis",
  "file": "TASK-001_chatgpt.py",
  "complexity": 1.8,
  "docstring_coverage": 100.0,
  "bad_practices_count": 0,
  "execution_time_sec": 0.060,
  "carbon_footprint_gCO2e": 0.000000119,
  "vibebench_score": 0.42,
  "status": "Success",
  "timestamp": "2026-05-08T19:30:00"
}
```

> **Note on `carbon_footprint_gCO2e`:** This is an order-of-magnitude
> estimate computed as `execution_time_sec × 15W × 475 gCO₂/kWh ÷
> 3,600,000`. It assumes a 15W laptop CPU and the IEA 2023 global
> average carbon intensity. Actual emissions depend on your hardware,
> location, and electricity grid mix. Use for relative comparisons
> between models, not as absolute environmental measurements.

## Documentation

| Guide | Description |
| ------- | ------------- |
| [Adding a Model](docs/adding-a-model.md) | Add a new LLM provider |
| [Adding a Task](docs/adding-a-task.md) | Add a new benchmark task |
| [Interpreting Results](docs/interpreting-results.md) | Read the metrics |

## Citation

If you use VibeBench in your research, please cite:
```bibtex
@software{arif2026vibebench,
  author = {Arif, Muktadir},
  title  = {VibeBench: An Automated Framework for the Holistic Evaluation of LLM-Generated Code},
  year   = {2026},
  doi    = {10.5281/zenodo.18758578},
  url    = {https://github.com/umayer16/VIBEBENCH}
}
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before
opening a pull request.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
```
