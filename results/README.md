# Benchmark Results

This directory contains the official benchmark results used in the
VibeBench arXiv preprint.

## Files

- `vibebench_v1.3_full_benchmark.json` — Single-run benchmark,
  7 models, 10 tasks (v1.3.0, May 2026)
- `vibebench_v1.3_full_benchmark.csv` — Same data in CSV format
- `vibebench_v1.4_reproducible_benchmark.json` — Three-run
  reproducibility benchmark, 7 models, 10 tasks (v1.4.0, May 2026).
  Includes mean, std dev, min, max execution time per file.
- `vibebench_v1.4_reproducible_benchmark.csv` — Same data in CSV

## How to reproduce

```bash
pip install .
vibebench benchmark --tasks datasets/prompts.json --export-csv
```

## Collection date

May 10, 2026

## Models evaluated

ChatGPT, Claude, Gemini, Grok, DeepSeek, LLaMA 3.3 70B, Human Baseline

## Tasks

TASK-001 through TASK-010 (see datasets/prompts.json for full prompts)
