import re

def is_valid_email(email):
    """
    Validates whether a given string is a valid email address.

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if email matches the pattern
    if re.match(pattern, email):
        return True
    return False

# Alternative version with more comprehensive validation
def is_valid_email_comprehensive(email):
    """
    More comprehensive email validation with additional rules.

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # More detailed pattern that enforces specific rules:
    # - Local part: letters, numbers, dots, underscores, percent, plus, hyphen
    # - Domain part: letters, numbers, dots, hyphens (must have at least one dot)
    # - TLD: at least 2 letters
    pattern = r'^[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]{1,255}\.[a-zA-Z]{2,}$'

    # Additional validation: no consecutive dots, no dot at start/end of local part
    if not re.match(pattern, email):
        return False

    # Split into local and domain parts
    local_part, domain_part = email.split('@')

    # Check for consecutive dots in local part
    if '..' in local_part:
        return False

    # Check local part doesn't start or end with dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    # Check domain part doesn't start or end with hyphen
    if domain_part.startswith('-') or domain_part.endswith('-'):
        return False

    # Check for consecutive dots in domain part
    if '..' in domain_part:
        return False

    return True

# Test examples
if __name__ == "__main__":
    test_emails = [
        "user@example.com",           # Valid
        "first.last@example.com",     # Valid
        "user+tag@example.co.uk",     # Valid
        "user_name@example.com",      # Valid
        "user@example.c",             # Invalid (TLD too short)
        "user@.com",                  # Invalid
        "@example.com",               # Invalid (no local part)
        "user@example",               # Invalid (no TLD)
        "user name@example.com",      # Invalid (space)
        "user..name@example.com",     # Invalid (consecutive dots)
        ".user@example.com",          # Invalid (starts with dot)
        "user@-example.com",          # Invalid (domain starts with hyphen)
        "user@example..com",          # Invalid (consecutive dots in domain)
    ]

    for email in test_emails:
        result = is_valid_email(email)
        print(f"{email:30} -> {result}")
