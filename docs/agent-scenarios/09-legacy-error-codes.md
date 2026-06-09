# Scenario 09: Legacy Error Codes

**Difficulty:** Easy  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> Users report seeing error code `TEAM_42` with no helpful message. Find where this code is defined and add a docstring plus a `get_error_message(code)` helper that returns the human-readable text.

## Files the agent should touch

- `qa-fixtures/anti-patterns/magic_strings/legacy_errors.py`

## Acceptance criteria

- [ ] Module docstring explains legacy error code convention
- [ ] `get_error_message("TEAM_42")` returns team member limit message
- [ ] Does not invent codes not in `LEGACY_ERROR_MESSAGES`
- [ ] No changes outside qa-fixtures

## Verification

```bash
cd qa-fixtures/anti-patterns/magic_strings
python3 -c "from legacy_errors import get_error_message; print(get_error_message('TEAM_42'))"
```

## Common failure modes

- Hallucinates error codes without reading the file
- Adds mapping to production `apps/api/meridian_api/errors.py` instead
- Documents codes in a new markdown file only, no code change