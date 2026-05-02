import re

def validate_email(email):
    # HUMAN TOUCH: Concise regex, covers the common cases without over-engineering
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

if __name__ == "__main__":
    tests = [
        'user@example.com',
        'invalid-email',
        'missing@domain',
        'good.email+tag@sub.domain.org'
    ]
    for t in tests:
        print(f"{t}: {validate_email(t)}")