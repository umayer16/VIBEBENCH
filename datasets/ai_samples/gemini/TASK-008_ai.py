import json
import os

def load_and_validate_json(file_path, required_keys):
    """
    Reads a JSON file and validates the presence of specific keys.
    
    Args:
        file_path (str): The path to the JSON file.
        required_keys (set): A set of keys that must be present in the JSON.
        
    Returns:
        dict: The parsed data if valid, None otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Ensure the data is a dictionary before checking keys
        if not isinstance(data, dict):
            print("Error: JSON root is not an object (dictionary).")
            return None

        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            print(f"Error: Missing required keys: {', '.join(missing_keys)}")
            return None

        return data

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e.msg} at line {e.lineno}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

# --- Example Usage ---
# requirements = {"id", "name", "version"}
# result = load_and_validate_json("config.json", requirements)