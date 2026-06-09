# Large Files

## Challenge

`task_registry.py` is ~1,100 lines of repetitive handler functions. The function agents need to edit is buried after hundreds of similar-looking definitions.

## Target

**File:** `task_registry.py`  
**Function:** `normalize_task_title` (search for `TARGET FUNCTION` comment)

## Expected behavior

`normalize_task_title("  hello   world  ")` should return `"hello world"`.

## Expected agent behavior

1. Grep for `normalize_task_title` rather than reading the entire file top-to-bottom
2. Edit only the target function near the bottom of the file
3. Add or update tests in `test_task_registry.py`

## Common failure modes

- Edits `register_handler_0` or another similarly-named function by mistake
- Rewrites the entire file instead of a 3-line fix
- Creates a new utility module instead of fixing the existing function

## Sample prompt

> Fix the task title normalization in the task registry — titles with extra whitespace aren't being cleaned up.