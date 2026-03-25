# VibeBench

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18758578.svg)](https://doi.org/10.5281/zenodo.18758578)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![status](https://joss.theoj.org/papers/e2f0068b712c24134f3c43abdb394eb4/status.svg)](https://joss.theoj.org/papers/e2f0068b712c24134f3c43abdb394eb4)

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
|---|---|---|---|
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

**Requirements:** Python 3.8+, Unix-based OS (Linux/macOS) for sandboxed execution.
```bash
# Clone the repository
git clone https://github.com/umayer16/VIBEBENCH.git
cd VIBEBENCH

# Install dependencies
pip install -r requirements.txt
```

---

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
│   ├── analyzer.py      # Static analysis engine (AST-based)
│   ├── executor.py      # Sandboxed dynamic execution
│   └── reporter.py      # Leaderboard and visualization
├── datasets/            # Benchmark task definitions
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
