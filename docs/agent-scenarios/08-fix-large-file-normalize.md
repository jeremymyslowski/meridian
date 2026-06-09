# Scenario 08: Fix Large File Normalization

**Difficulty:** Easy  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> Task titles with extra whitespace are not being cleaned up. Fix the normalization function in the task registry.

## Files the agent should touch

- `qa-fixtures/large-files/task_registry.py` — function `normalize_task_title` only

## Acceptance criteria

- [ ] `normalize_task_title("  hello   world  ")` returns `"hello world"`
- [ ] Does not rewrite entire 1,300-line file
- [ ] `test_task_registry.py` passes

## Verification

```bash
docker compose exec -T api python -m pytest -v /qa-fixtures/large-files
```

## Common failure modes

- Edits wrong function (`register_handler_N`)
- Rewrites entire file
- Creates new file instead of fixing existing function
- Never finds function without grepping (reads file top-to-bottom and gives up)