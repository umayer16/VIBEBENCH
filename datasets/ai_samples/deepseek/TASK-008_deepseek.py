import json
import os
from typing import Dict, Any, List, Optional, Union

def read_and_validate_json(
    file_path: str,
    required_keys: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Reads a JSON file and validates that it contains all required keys.

    Args:
        file_path (str): Path to the JSON file
        required_keys (List[str]): List of keys that must be present in the JSON

    Returns:
        Optional[Dict[str, Any]]: Parsed JSON data if successful, None otherwise

    Raises:
        No exceptions - all errors are handled gracefully with print statements
    """

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    # Check if file is empty
    if os.path.getsize(file_path) == 0:
        print(f"Error: File '{file_path}' is empty.")
        return None

    # Try to read and parse the JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}': {e}")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read file '{file_path}'")
        return None
    except Exception as e:
        print(f"Error: Unexpected error while reading file '{file_path}': {e}")
        return None

    # Validate that data is a dictionary
    if not isinstance(data, dict):
        print(f"Error: JSON root must be an object/dictionary, got {type(data).__name__}")
        return None

    # Check for required keys
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        print(f"Error: Missing required keys: {', '.join(missing_keys)}")
        print(f"Present keys: {list(data.keys())}")
        return None

    # Success - return the parsed data
    return data


# Example usage and test cases
if __name__ == "__main__":
    # Example 1: Create a sample valid JSON file
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "city": "New York"
    }

    # Write sample JSON to a file
    with open("sample.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    # Test with valid file and required keys
    required = ["name", "email"]
    result = read_and_validate_json("sample.json", required)
    print(f"Valid case result: {result}\n")

    # Test with missing key
    required_with_missing = ["name", "email", "phone"]
    result = read_and_validate_json("sample.json", required_with_missing)
    print(f"Missing key case result: {result}\n")

    # Test with non-existent file
    result = read_and_validate_json("nonexistent.json", required)
    print(f"Missing file case result: {result}\n")

    # Test with invalid JSON
    with open("invalid.json", "w") as f:
        f.write("{invalid json content}")
    result = read_and_validate_json("invalid.json", required)
    print(f"Invalid JSON case result: {result}\n")

    # Test with empty file
    with open("empty.json", "w") as f:
        pass  # Create empty file
    result = read_and_validate_json("empty.json", required)
    print(f"Empty file case result: {result}\n")

    # Clean up test files
    import os
    for test_file in ["sample.json", "invalid.json", "empty.json"]:
        if os.path.exists(test_file):
            os.remove(test_file)