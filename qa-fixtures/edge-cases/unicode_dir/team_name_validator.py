"""Team name validator — lives under unicode_dir to test path discovery."""

FORBIDDEN_NAMES = {"", " ", "admin", "root"}


def validate_team_name(name: str) -> bool:
    """Return True if team name is acceptable."""
    return name not in FORBIDDEN_NAMES