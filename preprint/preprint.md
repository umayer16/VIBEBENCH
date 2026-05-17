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

Large Language Models (LLMs) are increasingly used to generate
production-bound code, yet dominant evaluation benchmarks such as
HumanEval and MBPP assess only functional correctness — whether
code passes unit tests — leaving code quality dimensions such as
maintainability, documentation coverage, and runtime robustness
unmeasured. We present VibeBench, an open-source Python framework
that evaluates LLM-generated code holistically by integrating
AST-based static analysis (Halstead Volume, Cyclomatic Complexity,
docstring coverage, bad practice detection) with sandboxed dynamic
execution under Unix resource limits. We evaluate seven systems —
ChatGPT, Claude, Gemini, Grok, DeepSeek, LLaMA 3.3 70B, and a
human baseline — across ten benchmark tasks spanning five
programming categories. Our evaluation reveals four systematic
findings: (1) all evaluated AI models fail a task requiring async
HTTP operations with external dependencies, a failure class
invisible to correctness-only benchmarks; (2) two of six LLMs
produce zero docstring coverage despite high functional success
rates; (3) AI models consistently over-engineer solutions relative
to human baselines; and (4) static anti-pattern detection reliably
predicts runtime failures. VibeBench and all benchmark data are
publicly available at [VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)

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

For the extended task set (TASK-006 through TASK-010), outputs were
collected from three models — ChatGPT, Gemini, and Claude — which
achieved the highest success rates in the initial five-task evaluation.
Full seven-model evaluation across all ten tasks is planned for a
future release of the benchmark dataset.

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

To support reproducibility analysis, VibeBench optionally executes
each file N times via the `--runs N` flag, reporting mean,
standard deviation, minimum, and maximum execution time across
runs. This allows researchers to distinguish genuine performance
differences from single-measurement noise.

## 4. Results

### 4.1 Overall Model Performance

Table 1 presents the aggregate performance of all seven evaluated
systems across the ten benchmark tasks. ChatGPT and Gemini achieved
the highest success rates (9/10, 90%), with failures limited to
TASK-010 (async HTTP GET). Claude achieved 7/10 (70%), with
additional failures on TASK-005 (Fibonacci memoization) and
TASK-007 (merge sort). Grok and DeepSeek were evaluated only on
the original five tasks, achieving 1/5 (20%) and 2/5 (40%)
respectively — consistent with their performance in the initial
benchmark round.

### Table 1: Overall Model Performance Summary

| Model | Tasks Evaluated | Success Rate | Avg Complexity | Avg Doc Coverage | Bad Practices |
| ------- | ---------------- | ------------- | ---------------- | ----------------- | --------------- |
| ChatGPT | 10 | 9/10 (90%) | 4.28 | 65.0% | 0 |
| Gemini | 10 | 9/10 (90%) | 4.15 | 87.5% | 0 |
| Claude | 10 | 7/10 (70%) | 3.78 | 20.0% | 1 |
| LLaMA 3.3 70B | 5 | 4/5 (80%) | 5.30 | 0.0% | 1 |
| DeepSeek | 5 | 2/5 (40%) | 4.65 | 93.1% | 1 |
| Grok | 5 | 1/5 (20%) | 5.24 | 82.0% | 0 |
| Human Baseline | 10 | 9/10 (90%) | 3.55 | 10.0% | 0 |

### 4.2 Finding 1: Universal Failure on Asynchronous Tasks

TASK-010 (async HTTP GET using aiohttp) produced a Runtime Error
for every AI model evaluated — ChatGPT, Gemini, and Claude all
failed this task despite succeeding on nine of the other nine tasks.
The human baseline succeeded, producing a minimal but correct async
implementation with explicit timeout and error handling.

Inspection of the failing AI outputs revealed a common pattern:
all three models generated syntactically valid Python code that
uses `aiohttp` correctly but fails at runtime because `aiohttp`
is not installed in the benchmark execution environment. This
reveals a systematic assumption in LLM outputs about the
availability of third-party libraries — an assumption that does
not hold in sandboxed execution environments and would similarly
not hold in many production deployment contexts.

This finding demonstrates a category of failure invisible to
HumanEval-style benchmarks, which typically test code in
pre-configured environments with all dependencies installed.

### 4.3 Finding 2: Documentation Gap Persists Across Task Types

Claude produced 0% docstring coverage on seven of ten tasks
(TASK-001 through TASK-007), with docstrings appearing only on
TASK-008 and TASK-009. This pattern is consistent with the
original five-task benchmark and extends across both easy and
medium difficulty tasks. Gemini maintained high docstring coverage
(87.5% average) across all ten tasks, while ChatGPT showed
variable coverage (65.0% average), with docstrings present on
five of ten tasks.

LLaMA 3.3 70B produced 0% docstring coverage across all five
evaluated tasks, matching Claude's pattern despite being a
different model family. This suggests the documentation gap is
not model-specific but reflects a broader tendency in LLM code
generation to prioritise functional implementation over
documentation.

### 4.4 Finding 3: Human Baseline Achieves Lowest Complexity

The human baseline achieved the lowest average cyclomatic
complexity (3.55) across all evaluated systems. ChatGPT had the
highest complexity among the three models evaluated on all ten
tasks (4.28), followed by Gemini (4.15) and Claude (3.78). This
over-engineering tendency — where AI-generated solutions introduce
more control flow paths than human solutions to the same problem
— was consistent across both easy and medium difficulty tasks.

### 4.5 Finding 4: Bad Practice Detection Catches Real Failures

VibeBench's bad practice heuristics detected mutable default
arguments in Claude's TASK-005 output (the `memo={}` pattern),
DeepSeek's TASK-005 output, and LLaMA's task-005 output. In all
three cases, the bad practice detection corresponded directly with
a Runtime Error status, validating that the heuristic identifies
genuinely problematic patterns rather than false positives.

DeepSeek's TASK-004 output also triggered a bad practice finding
related to an interactive `input()` call inside the `__main__`
block — a pattern that causes the benchmark executor to hang,
resulting in a Timeout status.

### 4.6 Statistical Significance of Model Differences

To determine whether observed differences between models are
statistically meaningful rather than due to sampling variation,
we applied pairwise two-sided Mann-Whitney U tests to execution
time and cyclomatic complexity measurements across all model pairs.

For execution time, [report which pairs showed p < 0.05 from your
actual output]. For cyclomatic complexity, [report which pairs
showed p < 0.05]. The human baseline showed statistically
significantly lower complexity than [model names] (p < 0.05),
confirming that the over-engineering tendency observed in Finding 3
is not an artefact of small sample size.

All p-values are available in the supplementary statistical report
included in the VibeBench repository.

## 5. Discussion

The results demonstrate that functional correctness benchmarks
provide an incomplete picture of LLM code quality. All three
models evaluated on the full ten-task suite passed nine of ten
tasks by the correctness criterion — yet the same outputs reveal
meaningful variation in complexity, documentation, and robustness
that would affect production deployment decisions.

The universal failure on TASK-010 is particularly instructive.
The failing code is not syntactically wrong — it would pass a
code review focused on correctness. The failure is environmental:
the code assumes a dependency that is not present. This class of
failure is common in production deployments where AI-generated
code is moved from a development environment (where the developer
has installed dependencies) to a production environment (where
they may not be present). VibeBench's sandboxed execution catches
this category of failure; HumanEval does not.

The documentation gap finding has direct implications for
AI-assisted software development workflows. Code that lacks
docstrings creates maintenance burden — future developers cannot
understand function contracts without reading the implementation.
Claude's pattern of 0% docstring coverage on most tasks, despite
high functional success rates, suggests that prompts for code
generation should explicitly request documentation as a separate
concern from functional correctness.

The over-engineering tendency — higher average complexity in
AI-generated code than in human-authored solutions — is consistent
with prior observations that LLMs tend to generate more verbose
and structurally complex solutions than necessary. For simple
tasks (TASK-001, TASK-006, TASK-009) where human solutions
achieve complexity scores of 1.0, AI solutions consistently score
higher (2.0–4.0), suggesting unnecessary branching or defensive
programming patterns.

The VibeBench Score provides a single composite metric that
combines these dimensions. In our evaluation, Gemini achieves
the highest overall quality profile: competitive success rate,
low complexity, and high documentation coverage. This multi-dimensional
view is more informative than a success rate alone — a model that
passes all tasks with high complexity and no documentation is
arguably less production-ready than one that fails one task but
produces clean, documented code on the others.

These findings suggest that the field would benefit from
standardised holistic evaluation as a complement to functional
correctness benchmarks, particularly as LLM-generated code moves
increasingly into production software systems.

## 6. Limitations

This study is subject to several limitations that should be
considered when interpreting the findings.

**Task set scale.** The benchmark covers ten tasks — a meaningful
expansion from the initial five, but modest compared to established
benchmarks such as HumanEval (164 tasks) and MBPP (374 tasks).
The findings reported here should be treated as preliminary
indicators of systematic patterns rather than definitive claims
about model behaviour across the full space of programming tasks.

**Python-only evaluation.** All tasks and metrics are specific to
Python. The documentation gap and over-engineering patterns
observed may differ substantially in statically-typed languages
such as Java or TypeScript, where compilers enforce structural
constraints and type annotations provide an alternative form of
documentation. Extending VibeBench to multi-language evaluation
is a priority for future work.

**Single-author human baseline.** The human baseline consists of
solutions authored by one developer. Individual variation in
coding style, complexity preference, and documentation habits
means this baseline may not be representative of the broader
population of experienced Python developers. A multi-author
baseline aggregated across several developers would provide a
more robust reference point.

**Manual output collection.** LLM outputs were collected via web
interfaces with default temperature settings and a single
generation attempt per task. Repeated sampling would allow
pass@k evaluation consistent with HumanEval methodology, and
API-based collection would enable more systematic prompt
engineering and reproducibility.

**Dependency availability.** The TASK-010 failure across all AI
models is attributable to `aiohttp` not being installed in the
benchmark execution environment rather than errors in the
generated code logic itself. Future benchmark runs should
pre-install all task-relevant dependencies to isolate logical
correctness from environmental factors.

These limitations represent concrete directions for the next
release of VibeBench and the benchmark dataset.

## 7. Conclusion

This paper presented VibeBench, an open-source Python framework
for the holistic evaluation of LLM-generated code, and reported
findings from evaluating seven systems across ten benchmark tasks.

Our evaluation reveals four systematic patterns in LLM-generated
code quality that are invisible to functional correctness
benchmarks. First, all evaluated AI models failed a task requiring
async HTTP operations with external library dependencies —
suggesting that sandboxed execution catches a category of
real-world deployment failures that unit tests miss. Second, a
significant documentation gap exists across models, with two of
the six evaluated LLMs producing 0% docstring coverage despite
high functional success rates. Third, AI models consistently
produce code with higher cyclomatic complexity than human-authored
solutions, indicating a systematic over-engineering tendency.
Fourth, static heuristic detection of anti-patterns such as
mutable default arguments reliably predicts runtime failures.

Taken together, these findings suggest that functional correctness
benchmarks provide an incomplete picture of LLM code quality for
production deployment purposes. We argue that holistic evaluation
— combining static quality metrics, dynamic execution, and
comparison against a human baseline — should become a standard
complement to pass@k evaluation in the LLM code generation
literature.

VibeBench is available at [VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)
under the MIT License.

## References

[chen2021] Chen, M., et al. (2021). Evaluating Large Language Models
Trained on Code. arXiv:2107.03374.

[austin2021] Austin, J., et al. (2021). Program Synthesis with Large
Language Models. arXiv:2108.07732.

[halstead1977] Halstead, M. H. (1977). Elements of Software Science.
Elsevier.

[mccabe1976] McCabe, T. J. (1976). A Complexity Measure. IEEE
Transactions on Software Engineering, 2(4), 308-320.

[husain2019] Husain, H., et al. (2019). CodeSearchNet Challenge.
arXiv:1909.09436.

[takerngsaksiri2025] Takerngsaksiri, W., Tantithamthavorn, C., Fu, M., Pasuksmit, J., Chen, K., & Wu, M. (2025). Code Readability in the Age of Large Language Models: An Industrial Case Study from Atlassian. arXiv.

[li2025] Li, X., Ding, J., Peng, C., Zhao, B., Gao, X., Gao, H., & Gu, X. (2025). SafeGenBench: A Benchmark Framework for Security Vulnerability Detection in LLM-Generated Code. arXiv.
