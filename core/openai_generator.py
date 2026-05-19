"""openai_generator.py

Generates Python code solutions using the OpenAI API for a given
set of benchmark tasks, saving outputs to the datasets directory for
VibeBench analysis.

Usage:
    python core/openai_generator.py --tasks datasets/tasks.json --model gpt-4o
    python core/openai_generator.py --tasks datasets/tasks.json --model gpt-4o-mini
"""

import argparse
import json
import os
import re
from typing import Any, Optional


def generate_code_openai(prompt: str, model_name: str = "gpt-4o") -> str:
    """Sends a code generation prompt to the OpenAI API and returns the
    generated Python code as a string.

    Args:
        prompt (str): The coding task description to send to the model.
        model_name (str): The OpenAI model to use.

    Returns:
        str: The generated Python code, or an error message string.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai is not installed. " "Run: pip install openai"
        )

    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Get a key at https://platform.openai.com/api-keys"
        )

    client = OpenAI(api_key=api_key)

    system_prompt: str = (
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
        ]
    )

    # Safely extract string content
    raw_code: str = response.choices[0].message.content if response.choices[0].message.content is not None else ""
    code: str = raw_code.strip()

    # Strip markdown code fences if model includes them despite instructions
    code = re.sub(r"^```python\s*", "", code, flags=re.MULTILINE)
    code = re.sub(r"^```\s*", "", code, flags=re.MULTILINE)

    return code.strip()


def load_tasks(tasks_file: str) -> list[dict[str, Any]]:
    """Loads benchmark tasks from a JSON file.

    Args:
        tasks_file (str): Path to the tasks JSON file.

    Returns:
        list: A list of task dicts.
    """
    with open(tasks_file, "r", encoding="utf-8") as f:
        data: list[dict[str, Any]] = json.load(f)
        return data


def save_generated_code(
    code: str, model_name: str, task_name: str, output_dir: str = "datasets"
) -> str:
    """Saves generated code to the datasets directory under a model-named
    subfolder.

    Args:
        code (str): The generated Python code.
        model_name (str): The model name (used as subfolder name).
        task_name (str): The task name (used as filename).
        output_dir (str): Root datasets directory.
    """
    # Sanitize model name for use as directory name
    safe_model: str = (
        model_name.replace("/", "_").replace("-", "_").replace(".", "_")
    )
    model_dir: str = os.path.join(output_dir, safe_model)
    os.makedirs(model_dir, exist_ok=True)

    # Sanitize task name for use as filename
    safe_task: str = task_name.replace(" ", "_").lower()
    filepath: str = os.path.join(model_dir, f"{safe_task}.py")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"  ✅ Saved: {filepath}")
    return filepath


def run_generator(
    tasks_file: str, model_name: str, output_dir: str = "datasets"
) -> None:
    """Main generation loop — loads tasks, calls OpenAI, saves outputs.

    Args:
        tasks_file (str): Path to tasks JSON file.
        model_name (str): OpenAI model name to use.
        output_dir (str): Root datasets directory.
    """
    tasks: list[dict[str, Any]] = load_tasks(tasks_file)
    print(f"\n🤖 Generating code with {model_name} for {len(tasks)} tasks...\n")
    success: int = 0
    failed: int = 0

    for task in tasks:
        # Support both 'name' and 'id' as task identifier
        name: str = str(task.get("name") or task.get("id", "unnamed_task"))
        prompt: str = str(task.get("prompt", ""))
        category: str = str(task.get("category", ""))
        difficulty: str = str(task.get("difficulty", ""))

        # Enrich the prompt with category and difficulty context
        enriched_prompt: str = prompt
        if category or difficulty:
            enriched_prompt = (
                f"[Category: {category} | Difficulty: {difficulty}]\n{prompt}"
            )

        print(f"  [{name}] {category} ({difficulty}) — Generating...")

        try:
            code: str = generate_code_openai(enriched_prompt, model_name=model_name)
            save_generated_code(code, model_name, name, output_dir)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed [{name}]: {e}")
            failed += 1

    print(f"\n✅ Generation complete: {success} succeeded, {failed} failed.")
    print("\nRun VibeBench to analyze results:")
    print(f"  python vibebench.py benchmark --tasks {tasks_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openai_generator",
        description="Generate benchmark code solutions using OpenAI.",
    )
    parser.add_argument(
        "--tasks",
        required=True,
        metavar="FILE",
        help="Path to tasks JSON file (e.g. datasets/tasks.json).",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        metavar="MODEL",
        help="OpenAI model to use (default: gpt-4o). "
        "Options: gpt-4o, gpt-4o-mini, o1-mini",
    )
    parser.add_argument(
        "--output-dir",
        default="datasets",
        metavar="DIR",
        help="Root directory to save generated code (default: datasets/).",
    )

    args = parser.parse_args()
    run_generator(args.tasks, args.model, args.output_dir)


if __name__ == "__main__":
    main()