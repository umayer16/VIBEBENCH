# How to Interpret VibeBench Results

This guide explains what each metric in the VibeBench output means
and how to read the leaderboard.

## The JSON Output

Each record in the benchmark JSON file represents one Python file
evaluated by VibeBench:

```json
{
  "schema_version": "1.1",
  "model": "chatgpt",
  "category": "AI Synthesis",
  "file": "TASK-001_chatgpt.py",
  "complexity": 1.8,
  "docstring_coverage": 100.0,
  "bad_practices_count": 0,
  "execution_time_sec": 0.060,
  "vibebench_score": 0.42,
  "status": "Success",
  "timestamp": "2026-05-08T19:30:00"
}
```

## Metrics Explained

### Cyclomatic Complexity (`complexity`)

Measures the number of linearly independent paths through the code,
computed using the `radon` library (McCabe 1976). Higher values
indicate more branching and harder-to-test code.

| Score | Interpretation |
| ------- | --------------- |
| 1–5 | Simple, low risk |
| 6–10 | Moderate complexity |
| 11–20 | High complexity — consider refactoring |
| 21+ | Very high risk — hard to test and maintain |

The human baseline average in VibeBench v1.3 is **3.55**. AI models
typically score 10–22% higher than this baseline.

### Docstring Coverage (`docstring_coverage`)

Percentage of functions, async functions, and classes that include
a docstring. Computed via AST inspection.

- `100.0` — every function is documented
- `0.0` — no functions have docstrings
- `null` — the file has no functions or classes (script-only files)

Note: Low docstring coverage is not necessarily bad for very short
functions. It becomes a concern in files with 3+ non-trivial
functions.

### Bad Practices Count (`bad_practices_count`)

Number of anti-patterns detected by VibeBench's heuristic engine.
Each detected issue adds 1 to the count. Current heuristics:

| Heuristic | Example |
| ----------- | --------- |
| Hardcoded credential | `api_key = "abc123xyz"` |
| TODO/FIXME placeholder | `# TODO: insert logic here` |
| Ghost comment | A line containing only `#` |
| Duplicate import | `import os` appearing twice |
| Mutable default argument | `def func(data=[]):` |

A count of 0 means no issues were detected. Any count above 0
should be investigated — even 1 mutable default argument can cause
subtle bugs that are hard to trace.

### Execution Time (`execution_time_sec`)

Wall-clock time to execute the file in a sandboxed subprocess,
measured in seconds. Includes import time.

This metric has high variance because:

- SSL tasks (TASK-002) involve network I/O and take 0.3–0.5s
- Algorithm tasks take 0.03–0.06s

Do not compare execution times across different task types.
Compare only within the same task (e.g., all models on TASK-001).

### VibeBench Score (`vibebench_score`)

A composite metric combining complexity, documentation, and runtime
efficiency into a single value. Lower is better.

Formula: Σ = w₁·V̂ + w₂·M̂ + w₃·Φ

Where:

- V̂ = min-max normalised Halstead Volume
- M̂ = min-max normalised Cyclomatic Complexity
- Φ = T_baseline / T_llm (Operational Parity, capped at 2.0)
- Default weights: w₁=0.4, w₂=0.4, w₃=0.2

A score of 0.0 means perfect performance on all three dimensions.
A score approaching 1.0 means high complexity, high Halstead
volume, and slower than baseline execution.

### Status (`status`)

| Value | Meaning |
| ------- | --------- |
| `Success` | File ran and exited with code 0 |
| `Runtime Error` | File ran but exited with non-zero code |
| `Timeout` | File exceeded the 5-second CPU time limit |
| `Error` | File could not be found or read |

## The Leaderboard

The leaderboard aggregates per-file metrics into per-model summaries.

**Rank** is determined by success rate (descending), with average
complexity as a tiebreaker. The human baseline is shown separately
with a — rank because it is a reference point, not a competitor.

**Reading the summary table:**

| Rank | Model   | Avg Complexity | Avg Exec Time | Avg Doc Coverage | Bad Practices | Success Rate |
| 1    | CHATGPT | 4.28           | 0.0851s       | 65.0%            | 0             | 9/10         |

This row tells you: ChatGPT ranked first overall, produced solutions
with average complexity 4.28 (higher than the human baseline of
3.55), took 85ms average to execute, had docstrings in 65% of
functions, had no bad practices detected, and succeeded on 9 of
10 tasks.

## The Significance Report

The significance report answers: "Is this difference real, or could
it be due to chance?"
| Model A  | Model B | U Statistic | p-value | Significant |
| CHATGPT  | CLAUDE  | 48.0        | 0.0312  | ✅ Yes      |
| CHATGPT  | GEMINI  | 52.0        | 0.4821  | ❌ No       |

A p-value below 0.05 means the difference between two models is
statistically significant at the 95% confidence level. A p-value
above 0.05 means the observed difference could plausibly be due
to chance given the sample sizes.

With only 10 tasks per model, statistical power is limited. Treat
significant results as strong indicators and non-significant results
as inconclusive rather than evidence of no difference.

## The Comparison Report

The comparison report shows how a model's performance changed
between two benchmark runs:
| Model   | Success A | Success B | Δ Success |
| CHATGPT | 8/10      | 9/10      | +10%      |
| CLAUDE  | 7/10      | 7/10      | —         |

A positive Δ Success means the model improved. A negative Δ Success
means it regressed. Use this when comparing benchmark results before
and after adding new tasks, or when a model provider releases an
updated version.

## Carbon Footprint (`carbon_footprint_gCO2e`)

An order-of-magnitude estimate of the CO₂ equivalent emitted
during execution, in grams.

Formula: `execution_time_sec × 15W × 475 gCO₂/kWh ÷ 3,600,000`

Typical values are extremely small — around 1–2 micrograms (µg)
per execution. The leaderboard shows totals in µg for readability.

**Important:** This is an estimate for relative comparison between
models, not an absolute measurement. Actual emissions depend on
your hardware TDP, location, and electricity grid carbon intensity.
A model that takes twice as long to execute produces approximately
twice the carbon footprint, all else being equal.

The human baseline typically has a lower total carbon footprint
than AI models because human-authored solutions tend to have lower
average execution time.

## Common Misinterpretations

**"Higher docstring coverage means better code."**
Not always. A file with trivial one-line functions and 100%
docstring coverage is not better than a file with complex logic
and 0% coverage. Docstring coverage is one signal among several.

**"Lower execution time means better code."**
Not for correctness. Faster execution can mean a simpler algorithm
(good) or a broken one that exits early (bad). Always read status
alongside execution time.

**"A Runtime Error means the model failed the task."**
Sometimes. Runtime Errors on TASK-010 across all AI models were
caused by a missing `aiohttp` dependency, not by incorrect logic.
Always inspect the actual file when investigating a failure.
