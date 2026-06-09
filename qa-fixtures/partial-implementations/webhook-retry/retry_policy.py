"""Retry backoff policy — partial implementation."""

MAX_ATTEMPTS = 3
BASE_DELAY_SECONDS = 2


def compute_backoff_seconds(attempts: int) -> int:
    """Return delay before next retry. Exponential: base * 2^attempts."""
    # TODO: implement exponential backoff
    raise NotImplementedError("compute_backoff_seconds not implemented")


def should_retry(attempts: int) -> bool:
    return attempts < MAX_ATTEMPTS