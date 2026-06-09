# Scenario 12: Team Name Validator

**Difficulty:** Easy  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> Update the team name validator in qa-fixtures to reject empty and whitespace-only team names. It should also reject names longer than 100 characters.

## Files the agent should touch

- `qa-fixtures/edge-cases/unicode_dir/team_name_validator.py`

## Acceptance criteria

- [ ] `validate_team_name("")` returns False
- [ ] `validate_team_name("   ")` returns False
- [ ] `validate_team_name("a" * 101)` returns False
- [ ] `validate_team_name("Engineering")` returns True

## Verification

```bash
cd qa-fixtures/edge-cases/unicode_dir
python3 -c "
from team_name_validator import validate_team_name
assert not validate_team_name('')
assert not validate_team_name('   ')
assert not validate_team_name('x'*101)
assert validate_team_name('Engineering')
print('ok')
"
```

## Common failure modes

- Cannot find file (searches for wrong path)
- Edits production validation instead of fixture
- Strips whitespace instead of rejecting whitespace-only names