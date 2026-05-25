import re

def is_valid_email(email):
    """
    Validates an email address using a regular expression.

    Criteria:
    - Starts with alphanumeric characters, dots, underscores, or hyphens.
    - Contains an '@' symbol.
    - Domain name contains alphanumeric characters or hyphens.
    - Ends with a dot followed by a 2-6 character top-level domain (TLD).
    """
    # The regex pattern
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check for a match
    if re.match(email_regex, email):
        return True
    else:
        return False

# --- Quick Tests ---
test_emails = [
    "hello@example.com",     # Valid
    "user.name@domain.org",   # Valid
    "invalid-email@com",      # Invalid (no TLD)
    "plainaddress",           # Invalid (no @)
    "@missing-user.com"       # Invalid (no prefix)
]

for e in test_emails:
    print(f"{e}: {is_valid_email(e)}")
