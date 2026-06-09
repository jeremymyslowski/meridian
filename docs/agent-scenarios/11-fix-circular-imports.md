# Scenario 11: Fix Circular Imports

**Difficulty:** Medium  
**Starting branch:** `main`  
**Zone:** qa-fixtures

## User prompt

> module_a and module_b in qa-fixtures/edge-cases/circular have a circular import. Fix it so both modules can be imported without error.

## Files the agent should touch

- `qa-fixtures/edge-cases/circular/module_a.py`
- `qa-fixtures/edge-cases/circular/module_b.py`
- `qa-fixtures/edge-cases/circular/shared_types.py` (expected extraction point)

## Acceptance criteria

- [ ] `python3 -c "import module_a; import module_b"` works from circular/ directory
- [ ] `get_b_value()` still returns sensible value
- [ ] Uses `shared_types.py` or lazy imports — not hacky import reorder only

## Verification

```bash
cd qa-fixtures/edge-cases/circular
python3 -c "import module_a; import module_b; print(module_b.get_b_value())"
```

## Common failure modes

- Deletes one module entirely
- Moves everything to one file without preserving structure
- Ignores `shared_types.py` already provided as hint