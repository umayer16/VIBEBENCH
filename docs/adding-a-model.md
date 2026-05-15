# How to Add a New Model Generator to VibeBench

This guide walks you through adding support for a new LLM provider
so VibeBench can collect benchmark outputs from it automatically.

## Overview

Each model provider has a dedicated generator module in `core/`.
The three existing generators follow an identical pattern:

| File | Provider | API Key Variable |
| ------ | ---------- | ----------------- |
| `core/gemini_generator.py` | Google Gemini | `GEMINI_API_KEY` |
| `core/groq_generator.py` | Groq (LLaMA) | `GROQ_API_KEY` |
| `core/openai_generator.py` | OpenAI GPT-4o | `OPENAI_API_KEY` |

Adding a new generator takes approximately 30 minutes and follows
the same five-function structure every time.

## Step 1 — Install the Provider SDK

Add the provider's Python SDK to `requirements.txt` under the
optional LLM Generator APIs section:

--- LLM Generator APIs (optional) ---
google-genai>=0.3.0
groq>=0.4.0
openai>=1.0.0
your-provider-sdk>=1.0.0   # add this line

Install it in your environment:

```bash
pip install your-provider-sdk
```

## Step 2 — Create the Generator File

Create `core/your_provider_generator.py`. Copy the structure from
`core/openai_generator.py` as your starting point — it is the
most recently written and cleanest template.

Your file must implement exactly these five functions:

### `generate_code_your_provider(prompt, model_name)`

Calls the provider API and returns raw Python code as a string.
Strip any markdown code fences from the response before returning:

```python
import re

code = re.sub(r'^```python\s*', '', code, flags=re.MULTILINE)
code = re.sub(r'^```\s*', '', code, flags=re.MULTILINE)
return code.strip()
```

### `load_tasks(tasks_file)`

Reads `datasets/prompts.json` and returns a list of task dicts.
This function is identical across all generators — copy it verbatim.

### `save_generated_code(code, model_name, task_name, output_dir)`

Saves the generated code to `datasets/<model_name>/<task_name>.py`.
This function is also identical across all generators — copy it
verbatim.

### `run_generator(tasks_file, model_name, output_dir)`

The main loop: loads tasks, calls `generate_code_your_provider()`
for each, saves the output. Tracks success and failure counts.

### `main()`

Argument parsing with `argparse`. Must accept `--tasks`, `--model`,
and `--output-dir` flags matching the other generators.

## Step 3 — Add the API Key

Open `.env.example` and add your provider's key:
YOUR_PROVIDER_API_KEY=your_key_here

Read the key from the environment in your generator:

```python
api_key = os.environ.get("YOUR_PROVIDER_API_KEY")
if not api_key:
    raise EnvironmentError(
        "YOUR_PROVIDER_API_KEY environment variable is not set."
    )
```

## Step 4 — Add the System Prompt

Use the same system prompt as the other generators. Consistency
in the system prompt is important — it means differences in output
are attributable to the model, not to different instructions:

```python
system_prompt = (
    "You are an expert Python developer. "
    "Write a complete, working Python function for the following task. "
    "Return ONLY the raw Python code with no markdown, no explanations, "
    "and no code fences."
)
```

## Step 5 — Write Tests

Create `tests/test_your_provider_generator.py`. Use
`tests/test_openai_generator.py` as your template. The key
requirement is that tests must not make real API calls — use
`unittest.mock.patch` to intercept the API client.

Your test file must cover:

- `load_tasks()` loads a valid file
- `load_tasks()` raises `FileNotFoundError` on missing file
- `save_generated_code()` creates the output file
- `save_generated_code()` sanitises the model name in the path
- `generate_code_your_provider()` raises `EnvironmentError`
  without an API key
- `generate_code_your_provider()` strips markdown fences

## Step 6 — Run the Generator

Set your API key and run:

```bash
export YOUR_PROVIDER_API_KEY=your_key_here
python core/your_provider_generator.py --tasks datasets/prompts.json
```

Outputs are saved to `datasets/your_provider_model_name/`.

## Step 7 — Run the Benchmark

```bash
vibebench benchmark --tasks datasets/prompts.json --export-csv
```

VibeBench automatically discovers the new model's outputs and
includes them in the leaderboard.

## Step 8 — Open a Pull Request

Follow the standard contribution workflow:

1. Create a branch: `git checkout -b feature/your-provider-generator`
2. Commit your generator file and tests
3. Open a PR referencing any related Issue
4. Ensure all tests pass in CI before merging

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contribution
guidelines.
