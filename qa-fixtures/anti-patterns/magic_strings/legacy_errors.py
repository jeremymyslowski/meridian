"""Legacy error codes — intentionally undocumented outside this file."""

LEGACY_ERROR_MESSAGES = {
    "TEAM_42": "Team has reached maximum member limit",
    "TASK_99": "Task is locked by another user",
    "AUTH_7": "Session expired - please log in again",
}


def resolve_legacy_error(code: str) -> str:
    return LEGACY_ERROR_MESSAGES.get(code, "Unknown error")