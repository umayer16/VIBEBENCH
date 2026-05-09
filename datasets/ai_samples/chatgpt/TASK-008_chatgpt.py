import json
from pathlib import Path


def load_and_validate_json(file_path, required_keys):
    """
    Reads a JSON file, validates required keys, and returns parsed data.

    Args:
        file_path (str or Path): Path to the JSON file.
        required_keys (set or list): Keys that must exist in the JSON object.

    Returns:
        dict: Parsed JSON data if valid.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON is invalid or required keys are missing.
    """
    try:
        # Read and parse JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Ensure JSON root is a dictionary
        if not isinstance(data, dict):
            raise ValueError("JSON content must be an object (dictionary).")

        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise ValueError(
                f"Missing required key(s): {', '.join(missing_keys)}"
            )

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


# Example usage
if __name__ == "__main__":
    required = {"name", "email", "age"}

    try:
        result = load_and_validate_json("data.json", required)
        print("Valid JSON data:")
        print(result)

    except Exception as err:
        print(f"Error: {err}")