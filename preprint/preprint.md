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

## 4. Results

## 5. Discussion

## 6. Limitations

## 7. Conclusion

## References
