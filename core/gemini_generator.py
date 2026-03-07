"""
gemini_generator.py

Generates Python code solutions using the Google Gemini API for a given
set of benchmark tasks, saving outputs to the datasets directory for
VibeBench analysis.

Usage:
    python core/gemini_generator.py --tasks datasets/tasks.json --model gemini-1.5-flash
    python core/gemini_generator.py --tasks datasets/tasks.json --model gemini-2.0-flash
"""

import os
import json
import argparse
import re


def generate_code_gemini(prompt, model_name="gemini-1.5-flash"):
    """
    Sends a code generation prompt to the Gemini API and returns
    the generated Python code as a string.

    Args:
        prompt (str): The coding task description to send to the model.
        model_name (str): The Gemini model to use.

    Returns:
        str: The generated Python code, or an error message string.
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai is not installed. "
            "Run: pip install google-generativeai"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY environment variable is not set. "
            "Get a free key at https://aistudio.google.com/app/apikey"
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    system_prompt = (
        "You are an expert Python developer. "
        "Write a complete, working Python function for the following task. "
        "Return ONLY the raw Python code with no markdown, no explanations, "
        "and no code fences."
    )

    response = model.generate_content(f"{system_prompt}\n\nTask: {prompt}")
    code = response.text.strip()

    # Strip markdown code fences if model includes them despite instructions
    code = re.sub(r'^```python\s*', '', code, flags=re.MULTILINE)
    code = re.sub(r'^```\s*', '', code, flags=re.MULTILINE)

    return code.strip()


def load_tasks(tasks_file):
    """
    Loads benchmark tasks from a JSON file.

    Args:
        tasks_file (str): Path to the tasks JSON file.

    Returns:
        list: A list of task dicts with 'name' and 'prompt' keys.
    """
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_generated_code(code, model_name, task_name, output_dir="datasets"):
    """
    Saves generated code to the datasets directory under a model-named subfolder.

    Args:
        code (str): The generated Python code.
        model_name (str): The model name (used as subfolder name).
        task_name (str): The task name (used as filename).
        output_dir (str): Root datasets directory.
    """
    # Sanitize model name for use as directory name
    safe_model = model_name.replace("/", "_").replace("-", "_").replace(".", "_")
    model_dir = os.path.join(output_dir, safe_model)
    os.makedirs(model_dir, exist_ok=True)

    # Sanitize task name for use as filename
    safe_task = task_name.replace(" ", "_").lower()
    filepath = os.path.join(model_dir, f"{safe_task}.py")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"  ✅ Saved: {filepath}")
    return filepath


def run_generator(tasks_file, model_name, output_dir="datasets"):
    """
    Main generation loop — loads tasks, calls Gemini, saves outputs.

    Args:
        tasks_file (str): Path to tasks JSON file.
        model_name (str): Gemini model name to use.
        output_dir (str): Root datasets directory.
    """
    tasks = load_tasks(tasks_file)
    print(f"\n🤖 Generating code with {model_name} for {len(tasks)} tasks...\n")

    success = 0
    failed = 0

    for task in tasks:
        name = task.get("name", "unnamed_task")
        prompt = task.get("prompt", "")

        print(f"  [{name}] Generating...")

        try:
            code = generate_code_gemini(prompt, model_name=model_name)
            save_generated_code(code, model_name, name, output_dir)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed [{name}]: {e}")
            failed += 1

    print(f"\n✅ Generation complete: {success} succeeded, {failed} failed.")
    print(f"Run VibeBench to analyze results:\n")
    print(f"  python vibebench.py benchmark --tasks {tasks_file}")


def main():
    parser = argparse.ArgumentParser(
        prog="gemini_generator",
        description="Generate benchmark code solutions using Google Gemini."
    )
    parser.add_argument(
        "--tasks",
        required=True,
        metavar="FILE",
        help="Path to tasks JSON file (e.g. datasets/tasks.json)."
    )
    parser.add_argument(
        "--model",
        default="gemini-1.5-flash",
        metavar="MODEL",
        help="Gemini model to use (default: gemini-1.5-flash). "
             "Options: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash"
    )
    parser.add_argument(
        "--output-dir",
        default="datasets",
        metavar="DIR",
        help="Root directory to save generated code (default: datasets/)."
    )

    args = parser.parse_args()
    run_generator(args.tasks, args.model, args.output_dir)


if __name__ == "__main__":
    main()
```
