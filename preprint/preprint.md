---
title: "Beyond Correctness: A Holistic Quality Audit of LLM-Generated Python Code Using VibeBench"
authors:
  - name: Muktadir Arif
    affiliation: Saint Joseph Higher Secondary School, Dhaka, Bangladesh
    orcid: 0009-0005-6412-8980
date: May 2026
keywords: LLM evaluation, code quality, static analysis, cyclomatic complexity, Halstead metrics, software engineering, Python
---

## Abstract

## (To be written after Results section is complete)

## 1. Introduction

The adoption of Large Language Models (LLMs) as coding assistants
has accelerated dramatically since the release of tools such as
GitHub Copilot, ChatGPT, and Google Gemini. Developers increasingly
rely on these tools to generate production-bound code, yet the
evaluation frameworks used to benchmark these models have not kept
pace with this shift in usage.

Existing benchmarks — most prominently HumanEval [CITE chen2021]
and MBPP [CITE austin2021] — evaluate LLM-generated code through
a binary lens: does the code pass a set of unit tests? This
functional correctness criterion is necessary but insufficient for
assessing production-readiness. Code that passes all unit tests may
still be unmaintainable, insecure, or resource-inefficient. These
properties — collectively referred to as software quality attributes
— are invisible to correctness-only benchmarks but have significant
consequences for long-term maintenance costs and security posture.

This gap between benchmark evaluation and real-world software quality
is not merely theoretical. Our preliminary analysis of code generated
by six leading LLMs across five programming tasks revealed that every
evaluated model produced code with higher average cyclomatic
complexity than human-authored baseline solutions — a finding
consistent with a systematic over-engineering tendency in LLM outputs.
Furthermore, one model produced zero docstring coverage across all
five tasks despite achieving an 80% functional success rate. Neither
of these findings would have been surfaced by HumanEval or MBPP.

This paper presents VibeBench, an open-source Python framework
designed to fill this measurement gap. VibeBench combines AST-based
static analysis — computing Halstead Volume, Cyclomatic Complexity,
and docstring coverage — with sandboxed dynamic execution using
Unix resource limits. A composite VibeBench Score aggregates these
dimensions into a single metric enabling direct model comparison.

We evaluate seven LLMs (ChatGPT, Claude, Gemini, Grok, DeepSeek,
LLaMA 3.3 70B, and a Human Baseline) across ten benchmark tasks
spanning Data Structures, Algorithms, File I/O, Cybersecurity, and
Math/Logic. Our findings reveal systematic patterns in LLM code
quality that have direct implications for the safe deployment of
AI coding assistants in production environments.

The main contributions of this paper are:

1. **VibeBench** — an open-source framework for holistic evaluation
   of LLM-generated code, available at
   [VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)
2. **A composite quality metric** — the VibeBench Score (Σ),
   combining Halstead complexity, Cyclomatic Complexity, and
   Operational Parity into a single normalised score
3. **An empirical benchmark** — evaluation of seven models across
   ten tasks with publicly available results
4. **Four concrete findings** about systematic patterns in
   LLM-generated code quality

## 2. Related Work

### 2.1 Functional Correctness Benchmarks

The dominant paradigm for evaluating LLM code generation capability
is the pass@k metric, introduced by Chen et al. [CITE chen2021]
through the HumanEval benchmark. HumanEval consists of 164
hand-crafted Python programming problems, each paired with unit
tests. A model's score is the probability that at least one of k
generated samples passes all tests. This metric was subsequently
adopted by MBPP [CITE austin2021], which extended the evaluation
to 374 tasks sourced from beginner programming exercises.

While HumanEval and MBPP established the foundation for code
generation evaluation, both treat code as a mathematical artefact —
a function that either computes the correct output or does not.
They do not evaluate whether the generated code is readable,
documented, or efficiently structured. A solution with cyclomatic
complexity of 15 and no docstrings receives the same score as a
clean, well-documented solution with complexity of 2, provided
both pass the unit tests.

### 2.2 Code Quality and Static Analysis

Software quality measurement has a long history in traditional
software engineering. McCabe [CITE mccabe1976] introduced Cyclomatic
Complexity as a measure of the number of linearly independent paths
through a program's control flow graph. Halstead [CITE halstead1977]
proposed a complementary family of metrics based on operator and
operand counts, including Halstead Volume as a measure of
information content. Both metrics are widely used in industrial
code review processes but have rarely been applied to the evaluation
of AI-generated code.

Tools such as Pylint and Bandit perform static analysis on Python
code but focus on general code quality and security vulnerabilities
respectively. They are designed for human-authored code and do not
account for patterns specific to LLM outputs — such as ghost
comments (empty `#` symbols), mutable default arguments, or the
systematic absence of docstrings observed in our experiments.

### 2.3 Beyond Functional Correctness

Recent work has begun to recognise the limitations of purely
functional benchmarks. Liu et al. [CITE liu2024] proposed evaluating
code generation through the lens of software engineering principles
including readability and maintainability, though without a
systematic measurement framework. Zheng et al. [CITE zheng2023]
examined the security properties of LLM-generated code, finding
significant rates of insecure patterns. These studies motivate but
do not provide the automated, extensible evaluation pipeline that
VibeBench offers.

To the authors' knowledge, VibeBench is the first framework to
integrate AST-based heuristic detection for LLM-specific coding
patterns with Unix-controlled sandboxed execution and comparison
against a formalised human baseline — providing a complete audit
pipeline from static quality to dynamic performance.

## 3. Methodology

### 3.1 VibeBench Framework Overview

VibeBench follows a three-stage pipeline: collection, analysis,
and reporting. In the collection stage, Python source files
generated by LLMs are organised into a structured dataset
directory under `datasets/ai_samples/<model>/`. Human-authored
reference solutions are stored in `datasets/human_samples/`.

In the analysis stage, each file passes through two independent
analytical tracks simultaneously. The static analysis track
parses the source code into an Abstract Syntax Tree (AST) using
Python's built-in `ast` module without executing the code. The
dynamic execution track runs each file in an isolated subprocess
with Unix resource limits enforced via `RLIMIT_CPU` and
`RLIMIT_AS`. The two tracks are deliberately decoupled so that
static metrics can be computed even for files that are unsafe
to execute.

In the reporting stage, all metrics are aggregated into a
timestamped JSON report and a Markdown leaderboard sorted by
composite VibeBench Score.

## 3.2 Benchmark Tasks

We evaluate models on ten benchmark tasks spanning five
programming categories. Tasks were designed to cover a range
of difficulty levels and to require different programming
capabilities — from simple data structure manipulation to
asynchronous network programming.

| Task ID | Category | Difficulty | Description |
| --------- | ---------- | ------------ | ------------- |
| TASK-001 | Data Structures | Easy | Reverse a linked list |
| TASK-002 | Cybersecurity | Medium | SSL certificate expiry checker |
| TASK-003 | Algorithms | Hard | Dijkstra's shortest path |
| TASK-004 | File I/O | Easy | CSV column average calculator |
| TASK-005 | Math/Logic | Medium | Fibonacci with memoization |
| TASK-006 | Data Structures | Easy | Binary search implementation |
| TASK-007 | Algorithms | Medium | Merge sort implementation |
| TASK-008 | File I/O | Easy | JSON file validator |
| TASK-009 | Math/Logic | Easy | Email regex validator |
| TASK-010 | Cybersecurity | Medium | Async HTTP GET with error handling |

Each task was specified through a natural language prompt stored
in `datasets/prompts.json`. No additional context or examples
were provided to the models beyond the prompt text. For tasks
requiring input files (TASK-004: data.csv, TASK-008: JSON file),
standardised input files were provided identically to all models.

## 3.3 Models Evaluated

We evaluate six LLM-generated solutions per task alongside one
human-authored baseline, for a total of seven solution sets:

| Model | Provider | Access Method |
| ------- | ---------- | -------------- |
| ChatGPT (GPT-4o) | OpenAI | Web interface |
| Claude (Claude 3.5 Sonnet) | Anthropic | Web interface |
| Gemini (Gemini 1.5 Flash) | Google | Web interface / API |
| Grok (Grok-2) | xAI | Web interface |
| DeepSeek (DeepSeek-V2) | DeepSeek | Web interface |
| LLaMA 3.3 70B | Meta / Groq | Groq API |
| Human Baseline | N/A | Single experienced developer |

All LLM outputs were collected during February–March 2026 with
model temperature settings at default values. Each model was
given exactly one attempt per task with no iterative refinement.
Solutions were saved verbatim without manual correction, with
the exception of one known data collection error documented in
`datasets/data_quality_notes.md` (DQ-001).

## 3.4 Metrics

VibeBench computes five primary metrics per file:

**Cyclomatic Complexity (M)** is computed using the `radon`
library, which implements McCabe's [CITE mccabe1976] control
flow analysis. We report the average complexity across all
functions in each file. Files with M > 10 are flagged as
high-risk for maintainability failure.

**Halstead Volume (V)** is computed using AST-based operator
and operand counting per Halstead (1977) [CITE halstead1977]:

V = (N₁ + N₂) · log₂(n₁ + n₂)

where N₁ and N₂ are total operator and operand counts and n₁
and n₂ are unique counts. Higher volume indicates greater
cognitive load.

**Docstring Coverage (D)** measures the percentage of function
and class definitions that include a docstring, computed via
AST inspection of `FunctionDef`, `AsyncFunctionDef`, and
`ClassDef` nodes.

**Bad Practices Count (B)** counts the number of anti-patterns
detected by VibeBench's heuristic engine, including: hardcoded
credentials, TODO/FIXME placeholders, ghost comments (empty
`#` symbols), duplicate imports, and mutable default arguments.

**Execution Status** records whether each file runs successfully
within a 5-second CPU time limit and 512 MB memory limit. Files
that timeout, crash, or raise unhandled exceptions are recorded
as Runtime Error.

## 3.5 Composite VibeBench Score

We aggregate the per-file metrics into a composite VibeBench
Score (Σ) defined as:

Σ = w₁·V̂ + w₂·M̂ + w₃·Φ

where V̂ and M̂ are min-max normalised Halstead Volume and
Cyclomatic Complexity respectively across all files in the
benchmark run, Φ = T_base / T_llm is the Operational Parity
ratio (capped at 2.0), and default weights are w₁ = 0.4,
w₂ = 0.4, w₃ = 0.2. Lower scores indicate simpler, faster
code that more closely matches the human baseline.

## 3.6 Human Baseline Construction

The human baseline consists of ten solutions authored by a
single experienced developer prior to collecting any LLM
outputs, to prevent anchoring on AI-generated approaches.
Baseline solutions were written with an emphasis on clarity
and minimal complexity rather than feature completeness —
reflecting how an experienced developer would approach a
concise, maintainable implementation.

We acknowledge this single-author baseline as a limitation
(see Section 6). Future work will expand to a multi-author
baseline to account for individual variation.

## 3.7 Reproducibility

All benchmark data, prompts, human baseline solutions, and
LLM-generated outputs are publicly available at
[https://github.com/umayer16/VIBEBENCH](https://github.com/umayer16/VIBEBENCH) under the MIT License.The full benchmark can be reproduced using:

```bash
git clone https://github.com/umayer16/VIBEBENCH.git
cd VIBEBENCH
pip install .
vibebench benchmark --tasks datasets/prompts.json --export-csv
```

Results may differ slightly from those reported here due to
non-determinism in LLM outputs and differences in hardware
execution environments.

## 4. Results

## 5. Discussion

## 6. Limitations

## 7. Conclusion

## References
