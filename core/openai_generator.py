"""
openai_generator.py

Generates Python code solutions using the OpenAI API for a given
set of benchmark tasks, saving outputs to the datasets directory for
VibeBench analysis.

Usage:
    python core/openai_generator.py --tasks datasets/prompts.json
    python core/openai_generator.py --tasks datasets/prompts.json --model gpt-4o
"""

import os
import json
import argparse
import re

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def generate_code_openai(prompt, model_name="gpt-4o"):

    if OpenAI is None:
        raise ImportError("openai is not installed.")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Get a key at https://platform.openai.com/api-keys"
        )

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are an expert Python developer. "
        "Write a complete, working Python function for the following task. "
        "Return ONLY the raw Python code with no markdown, no explanations, "
        "and no code fences."
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {prompt}"}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    code = response.choices[0].message.content.strip()

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
        list: A list of task dicts with 'id' and 'prompt' keys.

    Raises:
        FileNotFoundError: If the tasks file does not exist.
    """
    if not os.path.exists(tasks_file):
        raise FileNotFoundError(
            f"Tasks file not found: {tasks_file}"
        )
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_generated_code(code, model_name, task_name, output_dir="datasets"):
    """
    Saves generated code to the datasets directory under a
    model-named subfolder.

    Args:
        code (str): The generated Python code.
        model_name (str): The model name (used as subfolder name).
        task_name (str): The task name (used as filename).
        output_dir (str): Root datasets directory.

    Returns:
        str: The full path to the saved file.
    """
    safe_model = (
        model_name.replace("/", "_")
                  .replace("-", "_")
                  .replace(".", "_")
    )
    model_dir = os.path.join(output_dir, safe_model)
    os.makedirs(model_dir, exist_ok=True)

    safe_task = task_name.replace(" ", "_").lower()
    filepath = os.path.join(model_dir, f"{safe_task}.py")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"  ✅ Saved: {filepath}")
    return filepath


def run_generator(tasks_file, model_name, output_dir="datasets"):
    """
    Main generation loop — loads tasks, calls OpenAI, saves outputs.

    Args:
        tasks_file (str): Path to tasks JSON file.
        model_name (str): OpenAI model name to use.
        output_dir (str): Root datasets directory.
    """
    tasks = load_tasks(tasks_file)
    print(
        f"\n🤖 Generating code with {model_name} "
        f"for {len(tasks)} tasks...\n"
    )

    success = 0
    failed = 0

    for task in tasks:
        name = task.get("name") or task.get("id", "unnamed_task")
        prompt = task.get("prompt", "")
        category = task.get("category", "")
        difficulty = task.get("difficulty", "")

        enriched_prompt = prompt
        if category or difficulty:
            enriched_prompt = (
                f"[Category: {category} | Difficulty: {difficulty}]\n"
                f"{prompt}"
            )

        print(f"  [{name}] {category} ({difficulty}) — Generating...")

        try:
            code = generate_code_openai(
                enriched_prompt, model_name=model_name
            )
            save_generated_code(code, model_name, name, output_dir)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed [{name}]: {e}")
            failed += 1

    print(
        "\n✅ Generation complete: "
        f"{success} succeeded, {failed} failed."
    )
    print("\nRun VibeBench to analyze results:")
    print(f"  python vibebench.py benchmark --tasks {tasks_file}")


def main():
    """
    Command-line entry point for the OpenAI code generator.
    """
    parser = argparse.ArgumentParser(
        prog="openai_generator",
        description="Generate benchmark code solutions using OpenAI API."
    )
    parser.add_argument(
        "--tasks",
        required=True,
        metavar="FILE",
        help="Path to tasks JSON file (e.g. datasets/prompts.json)."
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        metavar="MODEL",
        help=(
            "OpenAI model to use (default: gpt-4o). "
            "Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo"
        )
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
