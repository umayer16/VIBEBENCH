import json
import os


def read_and_validate_json(filepath, required_keys):
    # HUMAN TOUCH: Explicit error handling, returns None on failure
    if not os.path.exists(filepath):
        return None, "File not found"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"
    missing = [k for k in required_keys if k not in data]
    if missing:
        return None, f"Missing keys: {missing}"
    return data, None


if __name__ == "__main__":
    # Create a temporary test file so the script is self-contained
    test_file = "sample_test.json"
    with open(test_file, 'w') as f:
        json.dump({"name": "test", "version": "1.0"}, f)

    data, error = read_and_validate_json(test_file, ['name', 'version'])
    if error:
        print(f"Error: {error}")
    else:
        print(f"Valid: {data}")

    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
