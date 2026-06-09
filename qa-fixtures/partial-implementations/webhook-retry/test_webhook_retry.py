import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from event_queue import WebhookEvent, enqueue_webhook_event, fetch_pending_events
from retry_policy import compute_backoff_seconds, should_retry


def test_enqueue_and_fetch():
    enqueue_webhook_event(WebhookEvent(id="e1", url="http://example.com", payload={"a": 1}))
    pending = fetch_pending_events()
    assert len(pending) == 1
    assert pending[0].id == "e1"


def test_exponential_backoff():
    assert compute_backoff_seconds(0) == 2
    assert compute_backoff_seconds(1) == 4
    assert compute_backoff_seconds(2) == 8


def test_should_retry():
    assert should_retry(0) is True
    assert should_retry(2) is True
    assert should_retry(3) is False