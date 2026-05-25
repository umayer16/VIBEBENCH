"""groq_generator.py

Generates Python code solutions using the Groq API for a given
set of benchmark tasks, saving outputs to the datasets directory for
VibeBench analysis.

Usage:
    (python core/groq_generator.py
        --tasks datasets/prompts.json --model llama-3.3-70b-versatile)
    (python core/groq_generator.py
        --tasks datasets/prompts.json --model mixtral-8x7b-32768)
"""

import argparse
import json
import os
import re
from typing import Any, Optional


def generate_code_groq(
    prompt: str, model_name: str = "llama-3.3-70b-versatile"
) -> str:
    """Sends a code generation prompt to the Groq API and returns the

    generated Python code as a string.

    Args:
        prompt (str): The coding task description to send to the model.
        model_name (str): The Groq model to use.

    Returns:
        str: The generated Python code, or an error message string.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("groq is not installed. " "Run: pip install groq")

    api_key: Optional[str] = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY environment variable is not set. "
            "Get a free key at https://console.groq.com"
        )

    client = Groq(api_key=api_key)

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
            {"role": "user", "content": f"Task: {prompt}"},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    raw_code: Any = response.choices[0].message.content
    code: str = str(raw_code).strip() if raw_code is not None else ""

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
    safe_model: str = (
        model_name.replace("/", "_").replace("-", "_").replace(".", "_")
    )
    model_dir: str = os.path.join(output_dir, safe_model)
    os.makedirs(model_dir, exist_ok=True)

    safe_task: str = task_name.replace(" ", "_").lower()
    filepath: str = os.path.join(model_dir, f"{safe_task}.py")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"  ✅ Saved: {filepath}")
    return filepath


def run_generator(
    tasks_file: str, model_name: str, output_dir: str = "datasets"
) -> None:
    """Main generation loop — loads tasks, calls Groq, saves outputs.

    Args:
        tasks_file (str): Path to tasks JSON file.
        model_name (str): Groq model name to use.
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

        enriched_prompt: str = prompt
        if category or difficulty:
            enriched_prompt = (
                f"[Category: {category} | Difficulty: {difficulty}]\n{prompt}"
            )

        print(f"  [{name}] {category} ({difficulty}) — Generating...")

        try:
            code: str = generate_code_groq(enriched_prompt, model_name=model_name)
            save_generated_code(code, model_name, name, output_dir)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed [{name}]: {e}")
            failed += 1

    print(f"\n✅ Generation complete: {success} succeeded, {failed} failed.")
    print("\nRun VibeBench to analyze results:")
    print(f"  python vibebench.py benchmark --tasks {tasks_file}")


def main() -> None:
    """Command-line entry point for the Groq code generator."""
    ...
    parser = argparse.ArgumentParser(
        prog="groq_generator",
        description="Generate benchmark code solutions using Groq API.",
    )
    parser.add_argument(
        "--tasks",
        required=True,
        metavar="FILE",
        help="Path to tasks JSON file (e.g. datasets/prompts.json).",
    )
    parser.add_argument(
        "--model",
        default="llama-3.3-70b-versatile",
        metavar="MODEL",
        help="Groq model to use (default: llama-3.3-70b-versatile). "
        "Options: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it",
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
