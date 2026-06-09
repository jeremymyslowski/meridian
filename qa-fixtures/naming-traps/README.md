# Naming Traps

## Challenge

The repo contains **four** files related to "user service" across languages. An agent given a vague prompt like *"update the user service to handle deleted users"* often edits the wrong one.

## Files (decoys vs correct)

| File | Role |
|------|------|
| `decoy-frontend/UserService.ts` | **DECOY** — legacy frontend stub, not used |
| `decoy-legacy/user_service.py` | **DECOY** — archived Python script |
| `decoy-worker/internal/user/user.go` | **DECOY** — old Go prototype |
| `apps/api/meridian_api/services/user_service.py` | **CORRECT** — production API service |

## Expected agent behavior

1. Grep for `user_service` / `UserService` across the repo
2. Read this README or `apps/api/` structure to identify the production path
3. Ignore anything under `qa-fixtures/`
4. Edit `apps/api/meridian_api/services/user_service.py`

## Common failure modes

- Edits `decoy-frontend/UserService.ts` because TypeScript is listed first in grep results
- Edits `decoy-legacy/user_service.py` because filename matches snake_case convention
- Creates a brand-new file instead of finding the existing production service

## Sample prompt

> Add a `get_user_display_name(user_id)` function to the user service that returns the user's name or their email if name is empty.

**Must touch:** `apps/api/meridian_api/services/user_service.py`
**Must NOT touch:** any file under `qa-fixtures/naming-traps/`