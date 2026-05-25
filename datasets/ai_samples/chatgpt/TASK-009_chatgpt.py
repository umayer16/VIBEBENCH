import re

def is_valid_email(email: str) -> bool:
    """
    Validate an email address using a regular expression.

    Returns:
        True if the email is valid, otherwise False.
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.fullmatch(pattern, email) is not None


# Example usage
print(is_valid_email("test@example.com"))      # True
print(is_valid_email("john.doe@gmail"))        # False
print(is_valid_email("user@domain.co.uk"))     # True
print(is_valid_email("invalid-email@"))        # False
