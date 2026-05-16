# I Built a Benchmark That Measures AI Code Quality Beyond

## Correctness — Here Is What I Found

Most AI code benchmarks answer one question: does the code pass
the tests? HumanEval, MBPP, and similar benchmarks measure
*functional correctness* — they run the generated code against
a test suite and report a pass rate.

That is a useful metric. But it is not the only metric that
matters in production software. Code that passes tests can still
be unmaintainable, undocumented, or fragile in deployment
environments different from where it was tested.

I spent several months building **VibeBench**, an open-source
Python framework that evaluates LLM-generated code holistically.
Then I ran it on 7 systems — ChatGPT, Claude, Gemini, Grok,
DeepSeek, LLaMA 3.3 70B, and a human baseline — across 10
benchmark tasks. Here are four findings that correctness-only
benchmarks would have missed entirely.

## Finding 1: Every AI Model Failed the Async Task

TASK-010 asked models to write an async Python function using
`aiohttp` to fetch a URL and handle errors gracefully. ChatGPT,
Claude, and Gemini all got Runtime Error. The human baseline
succeeded.

The code the models wrote was not wrong. It was syntactically
valid, logically correct async Python. It failed because `aiohttp`
was not installed in the sandboxed execution environment — and
every model assumed it would be.

This is a real deployment failure pattern. A developer generates
code in their local environment where they have `aiohttp`
installed, the code looks fine, and it breaks in production or
CI where the dependency is not present. VibeBench's sandboxed
execution catches this. A unit test suite running in a
pre-configured environment does not.

## Finding 2: The Documentation Gap Is Real and Model-Specific

Docstring coverage — the percentage of functions that include a
docstring — varied dramatically across models:

| Model | Avg Docstring Coverage |
| ------- | ---------------------- |
| Gemini | 87.5% |
| DeepSeek | 93.1% |
| ChatGPT | 65.0% |
| Grok | 82.0% |
| Claude | 20.0% |
| LLaMA 3.3 70B | 0.0% |
| Human Baseline | 10.0% |

Claude produced 0% docstring coverage on 7 of 10 tasks despite
a 70% functional success rate. LLaMA produced 0% across all 5
evaluated tasks. This is not a correctness problem — the code
runs fine. But undocumented code creates maintenance burden that
compounds over time.

Interestingly, the human baseline also has low docstring coverage
(10%) — reflecting real-world developer practice where short,
obvious functions often go undocumented. The question is whether
the AI models are making deliberate choices or just defaulting
to no documentation.

## Finding 3: AI Models Consistently Over-Engineer

Cyclomatic complexity measures the number of independent paths
through code — higher values mean more branching and harder-to-test
functions. Lower is generally better for maintainability.

The human baseline achieved the lowest average complexity (3.55)
across all 10 tasks. Every AI model scored higher:

| Model | Avg Complexity | vs Human Baseline |
| ------- | --------------- | ------------------ |
| Human | 3.55 | — |
| Claude | 3.78 | +6% |
| Gemini | 4.15 | +17% |
| ChatGPT | 4.28 | +21% |
| DeepSeek | 4.65 | +31% |
| Grok | 5.24 | +48% |
| LLaMA | 5.30 | +49% |

The pattern was consistent across easy and medium tasks. For
simple tasks like binary search (TASK-006) where human solutions
achieve complexity 1.0, AI solutions scored 2.0–4.0. The models
add defensive branching, input validation, and edge case handling
that was not requested — which sounds good but adds complexity
that makes the code harder to read and test.

## Finding 4: Static Heuristics Predict Runtime Failures

VibeBench includes a bad practice detector that flags patterns
like mutable default arguments (`def func(memo={})`). In our
evaluation, every file where this pattern was detected — Claude
TASK-005, DeepSeek TASK-005, LLaMA task-005 — also received a
Runtime Error status.

The predictive accuracy was 100% on this pattern in our dataset.
That is a small sample, but it validates the approach: static
analysis of code structure can predict dynamic execution failures
without running the code. For security-sensitive or resource-
constrained environments where sandboxed execution is not possible,
this heuristic approach provides a meaningful quality signal.

## What This Means for AI-Assisted Development

If you are using AI-generated code in production, functional
correctness is a necessary but not sufficient quality bar. The
findings above suggest you should additionally check:

1. **Dependency assumptions** — does the code assume libraries
   that may not be present in your deployment environment?
2. **Documentation** — different models have very different
   documentation habits; you may need to prompt explicitly for
   docstrings
3. **Complexity** — AI models tend to over-engineer; simpler
   solutions often exist
4. **Anti-patterns** — mutable default arguments and similar
   patterns are common in AI output and can cause subtle bugs

VibeBench automates all of these checks. It is open-source, MIT
licensed, and extensible — you can add your own tasks, models,
and heuristics.

**GitHub:** [VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)
**Paper:** [arXiv link when live]

---

*VibeBench is a research project by Muktadir Arif, Saint Joseph
Higher Secondary School, Dhaka, Bangladesh.*
