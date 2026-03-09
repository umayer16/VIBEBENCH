# VibeBench Leaderboard
*Last updated: March 9, 2026 — v1.1.0*

Benchmark results across 5 tasks covering Data Structures, Cybersecurity,
Algorithms, File I/O, and Math/Logic. Human-authored solutions serve as
the reference baseline.

---

## Overall Results

| Rank | Model | Avg Complexity | Avg Docstring Coverage | Bad Practices | Success Rate | Avg Execution Time |
|------|-------|---------------|----------------------|---------------|--------------|-------------------|
| 🥇 1 | **ChatGPT** | 4.76 | 80.0% | 0 | 5/5 (100%) | 0.111s |
| 🥈 2 | **Gemini** | 3.90 | 95.0% | 0 | 5/5 (100%) | 0.109s |
| 🥉 3 | **DeepSeek** | 4.65 | 93.1% | 1 | 2/5 (40%) | 0.135s |
| 4 | **Claude** | 3.77 | 0.0% | 0 | 4/5 (80%) | 0.131s |
| 5 | **LLaMA 3.3 70B** | 5.30 | 0.0% | 0 | 4/5 (80%) | 0.077s |
| 6 | **Grok** | 5.24 | 82.0% | 0 | 1/5 (20%) | 0.161s |
| — | **HUMAN BASELINE** | 3.60 | 20.0% | 0 | 5/5 (100%) | 0.147s |

---

## Per-Task Results

### TASK-001: Reverse a Linked List (Data Structures — Easy)

| Model | Complexity | Docstring Coverage | Bad Practices | Status | Execution Time |
|-------|-----------|-------------------|---------------|--------|----------------|
| ChatGPT | 1.8 | 0.0% | 0 | ✅ Success | 0.060s |
| Claude | 2.0 | 0.0% | 0 | ✅ Success | 0.047s |
| DeepSeek | 2.0 | 80.0% | 0 | ✅ Success | 0.048s |
| Gemini | 2.0 | 75.0% | 0 | ✅ Success | 0.048s |
| Grok | 2.2 | 60.0% | 0 | ❌ Runtime Error | 0.103s |
| LLaMA 3.3 | 2.0 | 0.0% | 0 | ✅ Success | 0.046s |
| **HUMAN** | **1.0** | **100.0%** | **0** | **✅ Success** | **0.048s** |

### TASK-002: SSL Certificate Checker (Cybersecurity — Medium)

| Model | Complexity | Docstring Coverage | Bad Practices | Status | Execution Time |
|-------|-----------|-------------------|---------------|--------|----------------|
| ChatGPT | 7.0 | 100.0% | 0 | ✅ Success | 0.387s |
| Claude | 6.5 | 0.0% | 0 | ✅ Success | 0.397s |
| DeepSeek | 9.0 | 100.0% | 0 | ❌ Runtime Error | 0.366s |
| Gemini | 2.0 | 100.0% | 0 | ✅ Success | 0.352s |
| Grok | 6.0 | 50.0% | 0 | ❌ Runtime Error | 0.472s |
| LLaMA 3.3 | 10.0 | 0.0% | 0 | ❌ Runtime Error | 0.197s |
| **HUMAN** | **2.0** | **0.0%** | **0** | **✅ Success** | **0.530s** |

### TASK-003: Dijkstra's Algorithm (Algorithms — Hard)

| Model | Complexity | Docstring Coverage | Bad Practices | Status | Execution Time |
|-------|-----------|-------------------|---------------|--------|----------------|
| ChatGPT | 6.0 | 100.0% | 0 | ✅ Success | 0.050s |
| Claude | 4.67 | 0.0% | 0 | ✅ Success | 0.054s |
| DeepSeek | 3.14 | 100.0% | 0 | ❌ Runtime Error | 0.101s |
| Gemini | 6.0 | 100.0% | 0 | ✅ Success | 0.051s |
| Grok | 5.5 | 100.0% | 0 | ❌ Runtime Error | 0.088s |
| LLaMA 3.3 | 6.5 | 0.0% | 0 | ✅ Success | 0.052s |
| **HUMAN** | **6.0** | **0.0%** | **0** | **✅ Success** | **0.067s** |

### TASK-004: CSV Average Calculator (File I/O — Easy)

| Model | Complexity | Docstring Coverage | Bad Practices | Status | Execution Time |
|-------|-----------|-------------------|---------------|--------|----------------|
| ChatGPT | 6.0 | 100.0% | 0 | ✅ Success | 0.050s |
| Claude | 3.33 | 0.0% | 0 | ✅ Success | 0.055s |
| DeepSeek | 6.33 | 100.0% | 0 | ✅ Success | 0.068s |
| Gemini | 7.0 | 100.0% | 0 | ✅ Success | 0.055s |
| Grok | 9.0 | 100.0% | 0 | ✅ Success | 0.051s |
| LLaMA 3.3 | 5.0 | 0.0% | 0 | ✅ Success | 0.047s |
| **HUMAN** | **6.0** | **0.0%** | **0** | **✅ Success** | **0.047s** |

### TASK-005: Fibonacci with Memoization (Math/Logic — Medium)

| Model | Complexity | Docstring Coverage | Bad Practices | Status | Execution Time |
|-------|-----------|-------------------|---------------|--------|----------------|
| ChatGPT | 3.0 | 100.0% | 0 | ✅ Success | 0.048s |
| Claude | 2.33 | 0.0% | 0 | ❌ Runtime Error | 0.102s |
| DeepSeek | 2.8 | 85.71% | 1 | ❌ Runtime Error | 0.092s |
| Gemini | 2.5 | 100.0% | 0 | ✅ Success | 0.048s |
| Grok | 3.5 | 100.0% | 0 | ❌ Runtime Error | 0.084s |
| LLaMA 3.3 | 3.0 | 0.0% | 0 | ✅ Success | 0.043s |
| **HUMAN** | **3.0** | **0.0%** | **0** | **✅ Success** | **0.045s** |

---

## Key Findings

- **ChatGPT and Gemini** achieved 100% success rates across all tasks
- **Grok** had the highest runtime error rate (4/5 failures) despite reasonable complexity scores
- **LLaMA 3.3 70B** was the fastest model overall with the lowest average execution time
- **DeepSeek** produced the only bad practice detection (TASK-005) across all models
- **Human baseline** achieved lowest average complexity (3.60) confirming AI models tend toward over-engineering
- **Claude** had 0% docstring coverage across all tasks — a significant documentation gap

---

## Methodology

All models were evaluated on identical tasks using VibeBench v1.1.0. Metrics collected:
- **Cyclomatic Complexity** via `radon`
- **Docstring Coverage** via AST analysis
- **Bad Practices** via heuristic detection
- **Execution Time** via sandboxed execution
- **Status** — Success or Runtime Error under resource constraints
