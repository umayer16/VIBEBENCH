import re

def is_valid_email(email: str) -> bool:
    """
    Validates whether a given string is a valid email address using regex.

    Returns True if valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False

    # Basic but effective regex for most common email formats
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Match the entire string
    return bool(re.match(pattern, email.strip()))
