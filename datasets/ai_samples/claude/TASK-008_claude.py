import json
import os
from typing import Any

def read_and_validate_json(
    filepath: str,
    required_keys: set[str] | list[str] | None = None
) -> dict[str, Any]:
    """
    Read a JSON file, validate required keys, and return parsed data.

    Args:
        filepath:      Path to the JSON file.
        required_keys: Keys that must be present at the top level.
                       Pass None (default) to skip key validation.

    Returns:
        Parsed JSON data as a dict.

    Raises:
        FileNotFoundError: File does not exist at the given path.
        ValueError:        Content is not valid JSON, not a JSON object,
                           or is missing required keys.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in '{filepath}': {e}") from e

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected a JSON object (dict) at the top level, "
            f"got {type(data).__name__}."
        )

    if required_keys:
        missing = set(required_keys) - data.keys()
        if missing:
            raise ValueError(
                f"Missing required key(s): {', '.join(sorted(missing))}"
            )

    return data
