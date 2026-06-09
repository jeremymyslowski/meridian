# Scenario 02: Add Task Pagination

**Difficulty:** Hard  
**Starting branch:** `main` (pagination exists — use as regression or skip if already implemented)  
**Zone:** production

## User prompt

> The task list endpoint returns every task at once and it's getting slow. Add pagination with page and page_size query params, plus optional status filtering. Update the API client and add a paginated list view in the web app.

## Files the agent should touch

- `docs/api/openapi.yaml`
- `apps/api/meridian_api/routers/tasks.py`
- `apps/api/meridian_api/schemas.py` (`PaginatedTasksResponse`)
- `packages/api-client/src/index.ts`
- `apps/web/src/pages/TaskListPage.tsx` (or create it)
- `apps/api/tests/test_tasks.py`

## Acceptance criteria

- [ ] `GET /api/v1/projects/{id}/tasks?page=1&page_size=10` returns `{ items, meta }`
- [ ] `status` query param filters by task status
- [ ] API client `listTasks()` accepts pagination params
- [ ] Web list view shows prev/next controls
- [ ] `make api-test` passes

## Verification

```bash
curl -s "http://localhost:8000/api/v1/projects/<ID>/tasks?page=1&page_size=5" \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
```

## Common failure modes

- Paginates in frontend only (client-side slice) without API changes
- Breaks kanban board by changing list endpoint response shape without updating all consumers
- Forgets to update OpenAPI spec
- Implements offset pagination but omits `total` count in meta

## Note

On current `main`, this is **already implemented**. Use this scenario to test whether an agent redundantly re-implements existing code, or assign it on an older commit before Phase 2.