# Benchmark Results

This directory contains the official benchmark results used in the
VibeBench arXiv preprint.

## Files

- `vibebench_v1.3_full_benchmark.json` — Full benchmark results for
  all 7 models across all 10 tasks (VibeBench v1.3.0)
- `vibebench_v1.3_full_benchmark.csv` — Same data in CSV format for
  analysis in Excel, pandas, or R

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
