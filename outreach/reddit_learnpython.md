# Title

I benchmarked 7 AI models on Python code quality beyond
correctness — 4 findings that correctness-only benchmarks miss
Body:
I built VibeBench, an open-source Python framework that evaluates
LLM-generated code on metrics that HumanEval and MBPP ignore:
cyclomatic complexity, docstring coverage, bad practice detection,
and sandboxed execution with resource limits.

I evaluated ChatGPT, Claude, Gemini, Grok, DeepSeek, LLaMA 3.3 70B,
and a human baseline across 10 benchmark tasks.

**4 findings:**

**1. ALL AI models failed the async HTTP task** — not because the
code was wrong, but because they assumed aiohttp was installed.
Sandboxed execution catches this. Unit tests running in a
pre-configured environment don't.

**2. Documentation gap is real and model-specific** — Claude produced
0% docstring coverage on 7 of 10 tasks despite a 70% success rate.
LLaMA 3.3 70B: 0% across all 5 evaluated tasks. Gemini: 87.5%
average. Same functional result, very different maintainability.

**3. AI models consistently over-engineer** — Human baseline average
cyclomatic complexity: 3.55. Best AI model (Claude): 3.78. Worst
(LLaMA): 5.30. The human wrote simpler code on every task.

**4. Static heuristics predict runtime failures** — Mutable default
argument detection (def func(memo={})) flagged Claude TASK-005,
DeepSeek TASK-005, and LLaMA task-005. All three got Runtime Error
status. 100% predictive accuracy on this pattern.

GitHub:
Paper: [arXiv link when live]

Happy to answer questions about the methodology or findings.
