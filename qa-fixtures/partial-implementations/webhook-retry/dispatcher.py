"""Webhook dispatcher — partial implementation."""

from event_queue import WebhookEvent, fetch_pending_events, mark_attempt
from retry_policy import compute_backoff_seconds, should_retry


def dispatch_pending() -> list[str]:
    """Process pending webhook events. Returns list of dispatched event IDs."""
    results = []
    for event in fetch_pending_events():
        if not should_retry(event.attempts):
            continue
        # TODO: HTTP POST to event.url with event.payload
        # TODO: on failure, mark_attempt and schedule backoff via compute_backoff_seconds
        mark_attempt(event)
        results.append(event.id)
    return results