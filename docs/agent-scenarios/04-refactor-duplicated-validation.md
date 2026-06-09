# Scenario 04: Refactor Duplicated Validation

**Difficulty:** Medium  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> We have the same email validation logic copy-pasted in four places under qa-fixtures. Extract it into a shared module and update all the call sites to use it.

## Files the agent should touch

- `qa-fixtures/anti-patterns/duplicated_validation/validator_*.py` (all 4)
- New shared module e.g. `qa-fixtures/anti-patterns/duplicated_validation/email_validator.py`

## Acceptance criteria

- [ ] Single `validate_email()` (or equivalent) function defined once
- [ ] All 4 validators import from shared module
- [ ] Inconsistent function names (`email_ok`, `is_valid_contact_email`) unified or wrapped
- [ ] No changes to `apps/` production code

## Verification

```bash
grep -l "EMAIL_RE = re.compile" qa-fixtures/anti-patterns/duplicated_validation/*.py
# Should only appear in shared module after fix
```

## Common failure modes

- Creates shared module in `apps/api/` instead of qa-fixtures
- Extracts but leaves dead code in original files
- Changes regex behavior while refactoring
- Only updates 2 of 4 files