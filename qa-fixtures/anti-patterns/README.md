# Anti-Patterns

Intentionally poor code agents are asked to refactor or fix.

## Sub-zones

| Path | Challenge |
|------|-----------|
| `god_object/task_manager.py` | God object doing tasks, users, notifications, webhooks |
| `duplicated_validation/` | Same email check copy-pasted in 4 files |
| `magic_strings/legacy_errors.py` | Undocumented error code mapping |

## Expected agent behavior

- Extract shared validation into one module
- Split god object into focused classes/functions
- Read `legacy_errors.py` instead of inventing error mappings

## Sample prompts

**Duplication:** Extract duplicated email validation in `duplicated_validation/` into a shared module.

**Magic strings:** Users see error code `TEAM_42` with no useful message. Find the mapping in `magic_strings/legacy_errors.py`.

**God object:** Split `TaskManager` into separate task, notification, and webhook responsibilities.