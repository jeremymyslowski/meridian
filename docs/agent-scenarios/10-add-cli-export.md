# Scenario 10: Add CLI Task Export

**Difficulty:** Hard  
**Starting branch:** `scenario/10-cli-export`  
**Zone:** production

## User prompt

> Add a CLI command `meridian tasks export --project-id <uuid>` that exports all tasks for a project as CSV to stdout. Use the existing API.

## Files the agent should touch

- `apps/cli/meridian_cli/main.py` (or similar — stub exists on branch)
- `apps/cli/pyproject.toml` or `requirements.txt`
- `apps/api/meridian_api/routers/tasks.py` (only if export endpoint needed)
- Possibly `packages/api-client/src/index.ts`

## Acceptance criteria

- [ ] `python -m meridian_cli tasks export --project-id <id>` prints CSV header + rows
- [ ] Requires auth (API token env var or login flag)
- [ ] Columns: id, title, status, assignee_id
- [ ] Works against running API (`make dev`)

## Verification

```bash
git checkout scenario/10-cli-export
export MERIDIAN_TOKEN=<token>
python -m meridian_cli tasks export --project-id <project-uuid>
```

## Common failure modes

- Writes CSV to random path instead of stdout
- Bypasses API and connects to DB directly
- Never creates CLI package structure
- Hardcodes fake data instead of calling API