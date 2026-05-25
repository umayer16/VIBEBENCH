import json
import os
from typing import List, Dict, Any


def read_and_validate_json(
    file_path: str,
    required_keys: List[str]
) -> Dict[str, Any]:
    """
    Reads a JSON file, validates it contains all required keys, and returns the parsed data.

    Handles errors gracefully by raising descriptive exceptions.

    Args:
        file_path (str): Path to the JSON file
        required_keys (List[str]): List of keys that must be present in the JSON object

    Returns:
        Dict[str, Any]: The parsed JSON data as a dictionary

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file contains invalid JSON or is missing required keys
        TypeError: If the JSON root is not an object (dictionary)
    """

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: '{file_path}'")

    # Read and parse JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in '{file_path}': {str(e)}") from e
    except PermissionError:
        raise PermissionError(f"Permission denied when reading '{file_path}'")
    except Exception as e:
        raise IOError(f"Error reading file '{file_path}': {str(e)}") from e

    # Ensure the data is a dictionary
    if not isinstance(data, dict):
        raise TypeError(f"JSON content in '{file_path}' must be an object (dictionary), got {type(data).__name__}")

    # Validate required keys
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys in '{file_path}': {missing_keys}")

    return data