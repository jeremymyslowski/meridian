# Partial Implementations

TODO stubs spread across multiple files. Agents must complete them coherently.

## Sub-zone: webhook-retry

Simulates incomplete webhook retry logic (mirrors production worker patterns).

| File | Status |
|------|--------|
| `webhook-retry/event_queue.py` | Stub — enqueue not implemented |
| `webhook-retry/retry_policy.py` | Partial — backoff formula missing |
| `webhook-retry/dispatcher.py` | Partial — calls missing queue functions |

## Expected agent behavior

1. Read all three files before editing any
2. Implement `enqueue_webhook_event` and `fetch_pending_events` in event_queue.py
3. Complete `compute_backoff_seconds` in retry_policy.py
4. Wire dispatcher to queue and policy modules
5. Run `pytest webhook-retry/test_webhook_retry.py`

## Sample prompt

> Finish the webhook retry implementation in qa-fixtures — events should retry with exponential backoff up to 3 attempts.

**Must touch:** all 3 Python files in `webhook-retry/` plus tests  
**Must NOT touch:** `apps/worker/` unless scenario says so