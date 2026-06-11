# GitHub MCP fixture seeding

Evaluator-only guide for seeding GitHub issues, PRs, labels, and tags on a **fork** of `meridian-blind` before running MCP connector QA.

The blind template repo stays clean — agents never see this doc or pre-seeded issues on the template itself.

## Fixture numbering

On an empty fork, the seeder creates items in this order:

| # | Type | Title / branch |
|---|------|----------------|
| 1 | PR | `fix/viewer-permissions` → `main` |
| 2 | PR | `qa/viewer-worker-skip` → `main` |
| 3 | PR | `qa/analytics-copy-fix` → `main` |
| 4–12 | Issues | Nine labeled issues (issue **#12** = “Add CLI task export command”) |
| 13 | Draft PR | `feature/task-export-cli` → `main` |

A closed marker issue `mcp-seed-v1` is created last so re-runs are idempotent.

## Quick start

### 1. Fork the template

Fork `jeremymyslowski/meridian-blind` into your org (one fork per MCP test run).

GitHub forks copy only the default branch by default — the bootstrap step copies missing PR head branches from the template.

### 2. Seed the fork

**Local (requires `gh` auth):**

```bash
make seed-github REPO=my-org/eval-run-42
```

Re-seed after a test run:

```bash
make seed-github REPO=my-org/eval-run-42 FORCE=1
```

**GitHub Actions (on the fork):**

Actions → **Seed MCP Fixtures** → Run workflow. Uses `GITHUB_TOKEN` with `--force`.

### 3. Run MCP tests

Point the agent at the fork (`my-org/eval-run-42`), not the canonical `meridian` repo or the shared template. Use prompts from `github-mcp-connector-qa.csv`.

### 4. Verify

```bash
gh pr list -R my-org/eval-run-42
gh issue list -R my-org/eval-run-42
```

Expected numbers are printed at the end of the seed script and listed in `fixtures/github-mcp/manifest.json` under `expected_numbers`.

## Files

| Path | In blind mirror? | Purpose |
|------|------------------|---------|
| `fixtures/github-mcp/manifest.json` | Yes | Seed data |
| `scripts/seed-github-mcp-fixtures.sh` | Yes | Main seeder |
| `scripts/bootstrap-github-mcp-branches.sh` | Yes | Copy missing branches from template/parent |
| `.github/workflows/seed-mcp-fixtures.yml` | Yes | One-click seed on fork |
| `docs/github-mcp-fixtures.md` | **No** | This evaluator guide |

## Regenerating the blind template

After changing fixture branches or manifest data on canonical `meridian`:

```bash
make blind-repo OUT=../meridian-blind ALL_BRANCHES=1
git -C ../meridian-blind push -u origin --all
```

The full mirror includes `main`, `fix/session-timeout`, `fix/viewer-permissions`, `feature/task-export-cli`, `qa/viewer-worker-skip`, and `qa/analytics-copy-fix`.