# Scenario 07: Fix Broken Tests

**Difficulty:** Medium  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> The pytest suite in qa-fixtures/broken-tests/python is failing. Diagnose each failure and fix the root cause. Do not delete tests to make them pass.

## Files the agent should touch

Depends on diagnosis — likely one or more of:

- `qa-fixtures/broken-tests/python/paginator.py` (off-by-one)
- `qa-fixtures/broken-tests/python/test_wrong_assertion.py` (wrong expected value)
- `qa-fixtures/broken-tests/python/test_missing_fixture.py` or `conftest.py` (fixture name)

## Acceptance criteria

- [ ] All 3 tests pass
- [ ] No tests deleted or skipped with `@pytest.mark.skip`
- [ ] Fixes address root cause documented in `qa-fixtures/broken-tests/README.md`

## Verification

```bash
docker compose exec -T api python -m pytest -v /qa-fixtures/broken-tests/python
```

## Common failure modes

- Deletes failing tests
- Mocks everything so tests pass without fixing logic
- Fixes only one of three failures
- "Fixes" production `apps/api/tests/` instead of fixture tests