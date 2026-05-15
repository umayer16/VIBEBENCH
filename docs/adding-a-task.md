# How to Add a New Benchmark Task to VibeBench

This guide explains how to add a new coding task to the VibeBench
benchmark suite, collect model outputs, and run the evaluation.

## Overview

Each benchmark task consists of:

1. A task definition in `datasets/prompts.json`
2. A human-authored baseline solution in `datasets/human_samples/`
3. Model-generated solutions in `datasets/ai_samples/<model>/`

## Step 1 — Define the Task in prompts.json

Open `datasets/prompts.json` and add a new entry. Follow the
existing schema exactly:

```json
{
  "id": "TASK-011",
  "category": "Data Structures",
  "difficulty": "Easy",
  "prompt": "Write a Python function that implements a stack with push, pop, and peek operations.",
  "expected_complexity_limit": 3.0
}
```

Fields:

- `id` — Sequential task identifier. Use the next available number.
- `category` — One of: Data Structures, Algorithms, Cybersecurity,
  File I/O, Math/Logic. Add a new category if genuinely needed.
- `difficulty` — One of: Easy, Medium, Hard.
- `prompt` — The natural language instruction given to the model.
  Keep it concise and unambiguous. Do not include examples or
  starter code — models should generate everything from scratch.
- `expected_complexity_limit` — The cyclomatic complexity above
  which a solution is considered over-engineered for this task.

## Step 2 — Write the Human Baseline Solution

Create `datasets/human_samples/TASK-011_manual.py`. Write a clean,
minimal solution that a competent developer would be satisfied with.

Guidelines for baseline solutions:

- Prioritise clarity over cleverness
- Keep complexity low — the baseline sets the reference point
- Make the `__main__` block self-contained (create any needed input
  files, clean them up after)
- Do not write docstrings unless they are genuinely necessary —
  the human baseline intentionally has low docstring coverage to
  reflect real-world practice

Example baseline for a stack task:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    print(s.peek())   # 2
    print(s.pop())    # 2
    print(s.pop())    # 1
```

## Step 3 — Verify the Baseline Runs

```bash
vibebench analyze --input datasets/human_samples/TASK-011_manual.py
```

Check the output. The baseline should:

- Have no syntax errors (Halstead metrics must be a dict, not
  "Syntax Error")
- Execute without Runtime Error when run directly:
  `python datasets/human_samples/TASK-011_manual.py`

Fix any issues before collecting model outputs. A broken baseline
causes incorrect Phi (Operational Parity) scores for all models
on this task.

## Step 4 — Collect Model Outputs

For each model you want to evaluate, paste the prompt from Step 1
into the model's interface and save the output. Follow these rules:

- Use a fresh conversation — no prior context
- Copy the code exactly as generated — do not edit it
- Save to `datasets/ai_samples/<model>/TASK-011_<model>.py`

File naming conventions:

| Model | Filename |
| ------- | ---------- |
| ChatGPT | `TASK-011_chatgpt.py` |
| Claude | `TASK-011_claude.py` |
| Gemini | `TASK-011_ai.py` |
| DeepSeek | `TASK-011_deepseek.py` |
| Grok | `TASK-011_grok.py` |

If using a generator script:

```bash
python core/openai_generator.py --tasks datasets/prompts.json --model gpt-4o
```

The generator will produce outputs for all tasks including the new
one automatically.

## Step 5 — Verify Each Model Output

```bash
vibebench analyze --input datasets/ai_samples/chatgpt/TASK-011_chatgpt.py
```

If `halstead_metrics` returns `"Syntax Error"`, the model generated
invalid Python. Document this in `datasets/data_quality_notes.md`
using the existing DQ-NNN format.

## Step 6 — Run the Full Benchmark

```bash
vibebench benchmark --tasks datasets/prompts.json --export-csv --verbose
```

The new task will appear in the JSON report and leaderboard
automatically — VibeBench discovers tasks by walking the datasets
directory, not by reading prompts.json.

## Step 7 — Update the Preprint or Documentation

If you are contributing the new task to the public VibeBench
repository, update:

- `README.md` — update the task count in the benchmark description
- `CHANGELOG.md` — add an entry under `[Unreleased]`
- Open a Pull Request with the new task files and updated docs

## Common Mistakes

**Mistake: Baseline uses an external file that does not exist.**
The executor runs the file in the VIBEBENCH root directory.
If your baseline opens `data.csv`, that file must exist there,
or the baseline must create it. See TASK-004 and TASK-008 for
examples of self-contained baselines.

**Mistake: Prompt is ambiguous about the expected interface.**
"Write a sorting function" can be interpreted many ways.
"Write a Python function `merge_sort(arr)` that takes an unsorted
list and returns a new sorted list" produces more comparable
outputs across models.

**Mistake: Difficulty set too high, causing all models to fail.**
If all models get Runtime Error, the task produces no useful
comparative data. Start with Easy or Medium difficulty.
