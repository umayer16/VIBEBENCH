---
title: 'VibeBench: An Automated Framework for the Holistic Evaluation of LLM-Generated Code'
tags:
  - Python
  - LLM evaluation
  - static analysis
  - dynamic execution
  - software quality
authors:
  - name: Muktadir Arif
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Saint Joseph Higher Secondary School, Dhaka, Bangladesh
    index: 1
date: 24 February 2026
bibliography: paper.bib
---

# Summary

[cite_start]The rapid integration of Large Language Models (LLMs) into the software development lifecycle has necessitated more sophisticated evaluation frameworks that extend beyond basic functional correctness[cite: 68]. [cite_start]While traditional benchmarks focus on the ability of a model to pass unit tests, they often overlook critical software engineering attributes such as code complexity, maintainability, and resource efficiency[cite: 69].

[cite_start]`VibeBench` is an automated benchmarking suite designed for the holistic evaluation of LLM-generated code through integrated static analysis and sandboxed dynamic execution[cite: 70]. [cite_start]The framework moves beyond binary success/failure metrics by quantifying structural heuristics and measuring runtime stability in a controlled environment[cite: 89, 90].

# Statement of Need

[cite_start]Current evaluation methodologies for LLM-generated code primarily focus on functional correctness[cite: 85]. [cite_start]However, code in production environments must also be documented, adhere to security best practices, and operate within strict resource constraints[cite: 87]. [cite_start]Previous research has identified several "AI-isms" that compromise these standards, including overly complex logic and "ghost comments"[cite: 88].

[cite_start]`VibeBench` addresses this gap by providing a standardized methodology for researchers to audit AI-generated code for long-term maintainability[cite: 79]. [cite_start]By utilizing Abstract Syntax Tree (AST) walking and Unix-based resource limiting, `VibeBench` identifies subtle flaws that traditional unit tests ignore[cite: 71, 72].

# Mentions of Functionality

`VibeBench` is structured into three primary modules to ensure a reproducible evaluation pipeline:

## Static Quality Heuristics
[cite_start]The `CodeAnalyzer` module parses Python source code into an AST to perform deep structural inspections[cite: 131]. It implements the following **heuristic-based detections**:
- [cite_start]**Pattern Detection**: Identifies "ghost comments" (e.g., `# TODO: logic here`) and potential hardcoded credentials using targeted regular expressions[cite: 135].
- [cite_start]**Complexity Metrics**: Calculates Halstead metrics and cyclomatic complexity to estimate the "Mental Effort" required to maintain the code[cite: 133].
- [cite_start]**Documentation Coverage**: Measures the ratio of documented functions and classes to total definitions to assess readability[cite: 134].

## Sandboxed Dynamic Execution
[cite_start]The `CodeExecutor` module manages the runtime lifecycle of generated scripts[cite: 137]. [cite_start]To mitigate risks from inefficient or "hallucinated" code, it leverages Unix-based resource modules to enforce strict CPU time and memory address space limits[cite: 138].

## Benchmark Reference Data
The framework includes a suite of human-authored reference implementations located in `datasets/human_samples/`. [cite_start]These serve as a **Gold Standard** for comparing LLM efficiency and complexity against production-grade human standards[cite: 73, 175].

# Research Findings

[cite_start]An empirical study of five leading models—Gemini, ChatGPT, Claude, DeepSeek, and Grok—conducted with `VibeBench` revealed a significant "documentation crisis," with all evaluated AI models returning 0.0% docstring coverage[cite: 74, 115]. [cite_start]Furthermore, the results demonstrated a strong correlation between high structural complexity and runtime failure, particularly in models like Grok[cite: 75, 76]. [cite_start]In contrast, Gemini demonstrated the highest efficiency, closely approaching the human baseline performance[cite: 77].

# Acknowledgements

[cite_start]The author acknowledges the use of AI-assisted tools for language refinement and editing during the preparation of this manuscript[cite: 272]. [cite_start]All experimental design, framework implementation, and analysis were performed independently[cite: 273].

# References