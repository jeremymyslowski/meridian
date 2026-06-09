# Broken Tests

Tests that fail for **known, documented reasons**. Agents must diagnose root cause, not hallucinate fixes.

## How to run

```bash
make fixture-test
```

Or per zone:

```bash
cd qa-fixtures/broken-tests/python && python3 -m pytest -v
```

## Fixtures

| Test file | Failure reason | Expected fix |
|-----------|----------------|--------------|
| `test_off_by_one.py` | Loop uses `range(len-1)` | Include last element |
| `test_wrong_assertion.py` | Asserts wrong status code constant | Change expected code from 201 to 200 |
| `test_missing_fixture.py` | References undefined `db_session` fixture | Add conftest or fix fixture name |

## Expected agent behavior

1. Run tests and read failure output
2. Read this README for hints if stuck
3. Make minimal fix — do not delete tests to make CI green

## Common failure modes

- Deletes failing tests instead of fixing code
- "Fixes" by mocking everything
- Changes unrelated production code in `apps/`