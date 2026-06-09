# Scenario 06: Navigate Naming Trap

**Difficulty:** Easy  
**Starting branch:** `main`  
**Zone:** qa-fixtures + production

## User prompt

> Add a `get_user_display_name(user_id)` function to the user service. It should return the user's name, or their email if name is empty.

## Files the agent should touch

- `apps/api/meridian_api/services/user_service.py` **only**

## Acceptance criteria

- [ ] Function added to production `user_service.py`
- [ ] Uses existing DB patterns (`get_user_by_id` or similar)
- [ ] No edits to `qa-fixtures/naming-traps/` decoy files
- [ ] Returns email when name is empty string or None

## Verification

```bash
# No changes under naming-traps
git diff --name-only | grep naming-traps  # should be empty

# Optional: add unit test in apps/api/tests/
```

## Common failure modes

- Edits `qa-fixtures/naming-traps/decoy-frontend/UserService.ts`
- Edits `qa-fixtures/naming-traps/decoy-legacy/user_service.py`
- Creates a brand new service file instead of extending existing one
- Implements display logic in a React component instead of API service