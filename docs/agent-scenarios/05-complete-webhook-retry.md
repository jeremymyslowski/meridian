# Scenario 05: Complete Webhook Retry

**Difficulty:** Hard  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> Finish the webhook retry implementation in qa-fixtures/partial-implementations/webhook-retry. Events should enqueue, dispatch with exponential backoff, and respect the max attempt limit.

## Files the agent should touch

- `qa-fixtures/partial-implementations/webhook-retry/event_queue.py`
- `qa-fixtures/partial-implementations/webhook-retry/retry_policy.py`
- `qa-fixtures/partial-implementations/webhook-retry/dispatcher.py`

## Acceptance criteria

- [ ] `enqueue_webhook_event` and `fetch_pending_events` implemented
- [ ] `compute_backoff_seconds` returns `2, 4, 8` for attempts 0, 1, 2
- [ ] `make fixture-test` passes partial-implementations zone
- [ ] Does not modify `apps/worker/` unless explicitly asked

## Verification

```bash
docker compose exec -T api python -m pytest -v \
  /qa-fixtures/partial-implementations/webhook-retry
```

## Common failure modes

- Renames `event_queue.py` back to `queue.py` (shadows stdlib)
- Implements HTTP in dispatcher but forgets queue
- Hardcodes backoff values in dispatcher instead of retry_policy
- Copies production worker code wholesale into fixtures