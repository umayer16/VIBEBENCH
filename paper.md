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
    orcid: 0009-0005-6412-8980
    affiliation: 1
affiliations:
  - name: Saint Joseph Higher Secondary School, Dhaka, Bangladesh
    index: 1
date: 6 March 2026
bibliography: paper.bib
---

# Summary
The rapid integration of Large Language Models (LLMs) into the software development lifecycle has created a critical need for evaluation frameworks that extend beyond basic functional correctness. Traditional benchmarks, such as HumanEval or MBPP, primarily measure a model's ability to pass unit tests (functional correctness). However, they often overlook essential software engineering attributes like code maintainability, structural complexity, and operational resource efficiency.

VibeBench is an automated, extensible Python framework designed to fill this gap. It provides a holistic evaluation of LLM-generated code by integrating static quality heuristics with sandboxed dynamic execution. By walking the Abstract Syntax Tree (AST), VibeBench quantifies Halstead complexity metrics and identifies non-standard "bad practices"—such as ghost comments, hardcoded credentials, and documentation gaps—that are frequently found in AI-synthesized outputs but missed by traditional testers.

Simultaneously, the framework manages a secure lifecycle for generated scripts using Unix-based resource limiting (CPU time and memory address space) to measure runtime stability and latency. VibeBench is built for AI researchers, software auditors, and developers who need to quantify the "technical debt" introduced by autonomous agents. By grounding AI performance against a formalized Human Baseline, it provides the necessary metrics to determine if AI-generated code is truly production-ready.


# Statement of Need
Current evaluation methodologies for Large Language Model (LLM) generated code, such as HumanEval [@chen2021codex] and MBPP, primarily focus on functional correctness through unit testing. While these benchmarks are effective at determining if a model can solve a specific problem, they fail to audit the structural integrity and production-readiness of the resulting code. In a production environment, code that "works" but is overly complex, undocumented, or resource-inefficient creates significant technical debt and security risks.

VibeBench addresses this gap by providing a toolset that treats AI-generated code as software artifacts rather than just mathematical solutions. There is a documented "documentation crisis" in LLM outputs, where models frequently omit docstrings and internal comments required for maintainability. Furthermore, existing benchmarks rarely account for the correlation between high structural complexity and runtime instability.

VibeBench allows researchers and software auditors to:

Quantify Technical Debt: Measure Halstead complexity and documentation coverage to predict long-term maintenance costs.

Audit Security and Best Practices: Detect "AI-isms" like ghost comments or hardcoded credentials using AST-based heuristics.

Benchmark Operational Parity: Compare AI performance against a formalized human baseline in a resource-constrained sandbox.

By providing these metrics in an automated, reproducible framework, VibeBench enables the scientific community to move toward more robust and responsible autonomous code generation.

# State of the field
Several benchmarks and frameworks currently exist for evaluating the code generation capabilities of Large Language Models (LLMs). The most prominent among these are HumanEval [@chen2021codex] and MBPP (Mostly Basic Python Problems) [@austin2021program]. These benchmarks establish functional correctness by measuring the pass@k metric—a statistical representation of whether a model can produce at least one solution that passes a provided suite of unit tests. Other tools, such as CodeSearchNet [@husain2019codesearchnet], provide large-scale datasets for code retrieval and summarization but are not designed for direct execution-based benchmarking.

Despite their widespread adoption, these tools share a common limitation: they treat code as a mathematical solution rather than a software artifact. They prioritize "binary success" (the code runs) over "structural health" (the code is maintainable). For instance, HumanEval does not penalize models for producing "spaghetti code" or failing to include docstrings, provided the output passes the unit tests.

VibeBench was developed to bridge this gap between functional testing and software engineering audits. While existing tools like Evaluating Large Language Models Trained on Code focus on the logic of the algorithm, VibeBench provides an automated pipeline for quantifying technical debt. It is the first framework of its kind to integrate AST-based heuristic detection for "AI-isms" with Unix-controlled dynamic resource limiting to audit the operational parity of LLM-synthesized software against a formalized human baseline.

# Software design
VibeBench is designed as a modular, extensible pipeline written in Python. The framework follows a "Collector-Analyzer-Executor" architecture to ensure that static heuristics and dynamic performance metrics are decoupled and independently verifiable.

The core logic is divided into three primary sub-packages:

1. Static Quality Analyzer (core/analyzer.py)
The CodeAnalyzer class serves as the static analysis engine. It utilizes the Python ast (Abstract Syntax Tree) module to parse generated code into a tree structure without execution.

Heuristic Engine: It implements custom visitors to detect "AI-isms"—patterns common in LLM outputs like ghost comments (empty # symbols) or hardcoded credentials.

Complexity Metrics: It integrates the radon and halstead libraries to compute Cyclomatic Complexity and Halstead volume, providing a mathematical basis for maintainability.

2. Sandboxed Dynamic Executor (core/executor.py)
To safely evaluate unverified AI code, the CodeExecutor implements a secure lifecycle management system.

Resource Limiting: It leverages the Unix resource module to enforce "hard limits" on CPU time (RLIMIT_CPU) and maximum memory address space (RLIMIT_AS). This prevents "hallucinated" infinite loops or memory-leak attacks from crashing the host system.

Isolation: Each test run is executed in a clean environment, capturing stdout, stderr, and exit codes to determine runtime stability.

3. Reporting and Visualization (core/reporter.py)
The framework includes a post-processing layer that aggregates JSON-formatted raw data into human-readable formats.

Leaderboard Generation: It automatically calculates averages across multiple trials and generates Markdown tables for direct inclusion in documentation.

Performance Plotting: It utilizes matplotlib to visualize the correlation between structural complexity and execution success rates.


# Research impact statement
VibeBench provides a critical utility for the growing field of AI-assisted software engineering (AISE). As Large Language Models (LLMs) transition from simple code-completion assistants to autonomous agents, the scientific community requires robust tools to audit the "technical debt" and operational risks associated with machine-generated code.

The impact of VibeBench is centered on three research areas:

Automated Software Auditing: Researchers can use the framework to perform large-scale longitudinal studies on model evolution. By quantifying metrics like Halstead complexity and documentation coverage, VibeBench provides a standardized way to measure if newer model iterations are producing more maintainable code or merely more complex "spaghetti" logic.

Resource Efficiency Research: The framework’s sandboxed execution environment allows researchers to safely benchmark the energy and compute efficiency of AI-generated algorithms. This is particularly relevant for Green IT research and deploying AI code in resource-constrained edge computing environments.

Safety and Best Practices: By detecting "AI-isms" and hardcoded security risks through AST walking, VibeBench serves as a foundation for building "AI-Audit" pipelines. It enables the development of guardrails that ensure autonomous agents adhere to human-centric documentation and security standards.

By providing these capabilities in an open-source, modular format, VibeBench empowers researchers to move toward a more holistic understanding of AI performance that prioritizes long-term software sustainability over short-term functional success.

# Mathematics

`VibeBench` quantifies software quality and operational performance using standardized mathematical models. Single dollars ($) are used for inline mathematics, such as the Halstead Volume $V$.

Double dollars make self-standing equations for static complexity:

$$V = (N_{1} + N_{2}) \cdot \log_{2}(n_{1} + n_{2})$$

You can also use plain \LaTeX for equations like the Cyclomatic Complexity calculation:

\begin{equation}\label{eq:cyclomatic}
M = E - N + 2P
\end{equation}

and refer to \autoref{eq:cyclomatic} from the text to explain the relationship between control flow edges ($E$) and nodes ($N$).

For dynamic evaluation, we define **Operational Parity** ($\Phi$) as the ratio of human-authored baseline latency ($T_{base}$) to the LLM execution time ($T_{llm}$):

\begin{equation}\label{eq:parity}
\Phi = \frac{T_{base}}{T_{llm}}
\end{equation}

where a value of $\Phi \approx 1$ represents optimal performance parity with human standards.

# Citations

Citations to entries in `paper.bib` should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format. 

The following citation keys are used throughout this manuscript to ground the development of `VibeBench` in established software science and LLM benchmarking research:

- `@chen2021codex` -> "Chen et al. (2021)" for the foundations of functional correctness in the HumanEval benchmark.
- `[@austin2021program]` -> "(Austin et al., 2021)" regarding the MBPP dataset and program synthesis.
- `[@halstead1977elements]` -> "(Halstead, 1977)" for the mathematical basis of the complexity metrics implemented in the `analyzer` module.
- `[@husain2019codesearchnet]` -> "(Husain et al., 2019)" for large-scale code retrieval and representation standards.

If you wish to cite the `VibeBench` software repository directly for use in other research, please use the provided Zenodo DOI: `10.5281/zenodo.18758578`.


# Figures

Figures in JOSS are included using standard Markdown syntax with an additional LaTeX label for cross-referencing. 

![The VibeBench System Architecture, illustrating the modular flow from LLM code ingestion to AST-based static analysis and sandboxed execution.\label{fig:architecture}](figures/architecture.png)

As shown in \autoref{fig:architecture}, the framework ensures that static heuristics (Halstead complexity, docstring coverage) are captured independently of dynamic performance metrics.

Figure sizes can be customized to fit the page layout by adding a width parameter:

![A sample of the VibeBench Leaderboard output, demonstrating how model performance is ranked across multiple trials.\label{fig:leaderboard}](figures/leaderboard_sample.png){ width=80% }


# AI usage disclosure

In accordance with JOSS policies, the author discloses that generative AI tools (specifically Google Gemini and ChatGPT) were utilized during the development of this project. 

- **Software Development**: AI was used to assist in writing standard boilerplate code for the reporting engine and for debugging Abstract Syntax Tree (AST) visitor patterns. The core logic of the VibeBench evaluation framework, including the specific static quality heuristics and the dynamic resource-limiting implementation, was designed and verified by the author.
- **Manuscript Preparation**: AI tools were used for language refinement, grammatical correction, and optimizing the LaTeX formatting of the manuscript. 

All scientific claims, experimental results, and data interpretations presented in this paper are the original work of the author and have been manually verified for accuracy.

# Acknowledgements

The author expresses gratitude to Saint Joseph Higher Secondary School, Dhaka, for providing the academic environment necessary to pursue this research. Special thanks are extended to the Executive Committee and members of the Josephite Scintilla Science Club (JSSC) for their feedback on the framework's utility and their support of independent student research in software engineering. 

The author also acknowledges the peer reviewers and editors at the Journal of Open Source Software (JOSS) whose preliminary feedback helped refine the structural documentation and scientific grounding of this manuscript.

# References
