# Agent Scenario Playbook

Scripted QA tasks for evaluating AI coding agents against the Meridian repo.

## How to run a scenario

1. Check out the **starting point** branch (or stay on `main` for fixture-only scenarios)
2. Give the agent only the **user prompt** — do not share acceptance criteria
3. After the agent finishes, verify against **acceptance criteria**
4. Record which **failure modes** occurred

```bash
# Example: production bug scenario
git checkout scenario/01-jwt-expiry
# ... run agent ...
make api-test && cd apps/web && npm test -- --run

# Example: fixture-only scenario (stay on main)
# ... run agent ...
make fixture-test
```

## Scenario index

| # | Scenario | Start branch | Zone |
|---|----------|--------------|------|
| 01 | [JWT expiry mismatch](01-jwt-expiry-bug.md) | `scenario/01-jwt-expiry` | production |
| 02 | [Add task pagination](02-add-task-pagination.md) | `main` | production |
| 03 | [Viewer role enforcement](03-viewer-role-gaps.md) | `scenario/03-viewer-role` | production |
| 04 | [Refactor duplicated validation](04-refactor-duplicated-validation.md) | `main` | qa-fixtures |
| 05 | [Complete webhook retry](05-complete-webhook-retry.md) | `main` | qa-fixtures |
| 06 | [Navigate naming trap](06-navigate-naming-trap.md) | `main` | qa-fixtures |
| 07 | [Fix broken test suite](07-fix-broken-tests.md) | `main` | qa-fixtures |
| 08 | [Fix large-file normalization](08-fix-large-file-normalize.md) | `main` | qa-fixtures |
| 09 | [Document legacy error codes](09-legacy-error-codes.md) | `main` | qa-fixtures |
| 10 | [Add CLI task export](10-add-cli-export.md) | `scenario/10-cli-export` | production |
| 11 | [Fix circular imports](11-fix-circular-imports.md) | `main` | qa-fixtures |
| 12 | [Harden team name validator](12-team-name-validator.md) | `main` | qa-fixtures |

## Scoring suggestions

| Result | Definition |
|--------|------------|
| Pass | All acceptance criteria met, no unrelated file changes |
| Partial | Core fix works but missed edge cases or extra files changed |
| Fail | Wrong file edited, tests still broken, or hallucinated API |

## Branch strategy

- `main` — stable, CI green, fixture tests fail as documented
- `scenario/*` — intentional bugs for production-code scenarios
- Tags `scenario-NN-start` — optional pinned starting points (create with `git tag`)