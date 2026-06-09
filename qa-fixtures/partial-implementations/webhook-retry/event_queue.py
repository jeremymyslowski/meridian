"""Webhook event queue — partial implementation."""

from dataclasses import dataclass, field


@dataclass
class WebhookEvent:
    id: str
    url: str
    payload: dict
    attempts: int = 0


_QUEUE: list[WebhookEvent] = []


def enqueue_webhook_event(event: WebhookEvent) -> None:
    # TODO: append event to _QUEUE
    raise NotImplementedError("enqueue_webhook_event not implemented")


def fetch_pending_events(limit: int = 10) -> list[WebhookEvent]:
    # TODO: return events with attempts < 3
    raise NotImplementedError("fetch_pending_events not implemented")


def mark_attempt(event: WebhookEvent) -> None:
    event.attempts += 1