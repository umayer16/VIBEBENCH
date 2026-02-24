# VibeBench Reference Datasets

This directory contains the data used to benchmark LLM performance.

## 🏆 Human Baseline (Reference Data)
[cite_start]The files in `datasets/human_samples/` serve as the **Gold Standard** or **Benchmark Reference Data** for VibeBench[cite: 73]. 

These scripts were manually authored to demonstrate:
* [cite_start]**Optimal Complexity**: Minimal structural overhead (Avg: 3.60)[cite: 149, 175].
* [cite_start]**Resource Efficiency**: High-speed execution (Avg: 0.5297s)[cite: 149, 175].
* [cite_start]**Maintainability**: Proper use of "Human Touch" comments for memory and logic handling[cite: 207].

## 📂 Structure
* [cite_start]`prompts.json`: The core task definitions and complexity limits.
* [cite_start]`human_samples/`: Reference implementations for Tasks 001-005.
* [cite_start]`ai_samples/`: Raw outputs from evaluated models (Gemini, ChatGPT, etc.)[cite: 73].

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18758578.svg)](https://doi.org/10.5281/zenodo.18758578)
