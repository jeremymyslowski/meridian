# QA Fixtures

Isolated challenge zones for AI agent stress-testing. **Not imported by production code.**

Each subfolder has a README with the challenge, expected agent behavior, and sample prompts.

## Zones

| Zone | Purpose |
|------|---------|
| [naming-traps/](naming-traps/) | Similar filenames across languages — pick the right file |
| [large-files/](large-files/) | 1,300+ line file — find the one function to edit |
| [edge-cases/](edge-cases/) | Circular imports, deep nesting, generated code headers |
| [anti-patterns/](anti-patterns/) | God objects, duplicated logic, magic strings |
| [broken-tests/](broken-tests/) | Failing tests with documented root causes |
| [partial-implementations/](partial-implementations/) | TODO stubs across multiple files |

## Running fixture tests

```bash
make fixture-test
```

Broken and partial zones are **expected to fail** until an agent fixes them. See each zone README for details.

## Rules

1. Never import `qa-fixtures/` from `apps/` or `packages/`
2. Production naming-trap target: `apps/api/meridian_api/services/user_service.py`
3. Agent scenarios in `docs/agent-scenarios/` reference these zones (Phase 4)