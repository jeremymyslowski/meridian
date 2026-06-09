"""Copy 3 of email validation."""

import re

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def is_valid_contact_email(email: str) -> bool:
    if not email:
        return False
    if " " in email:
        return False
    return bool(EMAIL_RE.match(email))