# Scenario 03: Viewer Role Gaps

**Difficulty:** Medium  
**Starting branch:** `scenario/03-viewer-role`  
**Zone:** production

## User prompt

> Viewers on a team can still delete tasks via the API. Lock down the API so viewers are read-only, and make sure the UI hides destructive actions for viewers. The worker should not send assignment notifications to viewers.

## Files the agent should touch

- `apps/api/meridian_api/policies.py`
- `apps/api/meridian_api/routers/tasks.py` (DELETE or PATCH guards)
- `apps/web/src/hooks/usePermissions.ts`
- `apps/web/src/pages/TaskDetailPage.tsx`
- `apps/worker/cmd/worker/main.go` (`isViewerOnTaskTeam`)

## Acceptance criteria

- [ ] Viewer receives 403 on task create/update/delete
- [ ] Viewer can still list and read tasks
- [ ] UI hides comment form and attachment buttons for viewers
- [ ] Worker skips notifications when assignee is viewer
- [ ] `make api-test` passes

## Verification

```bash
git checkout scenario/03-viewer-role
# Register viewer, add to team as viewer, attempt PATCH /tasks/{id}
# Expect 403
```

## Common failure modes

- Hides UI buttons but leaves API open
- Blocks viewers from reading tasks (too restrictive)
- Edits qa-fixtures decoy files instead of production policies
- Only fixes API, forgets worker notification skip