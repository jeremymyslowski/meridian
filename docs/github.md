# Publishing Meridian to GitHub

This guide covers pushing the repo, branch strategy, and how CI relates to agent QA.

## Create and push the remote

```bash
cd meridian

# One-time: create an empty repo on GitHub (no README/license — this repo has them)
git remote add origin git@github.com:YOUR_ORG/meridian.git

git push -u origin main
git push origin scenario/01-jwt-expiry scenario/03-viewer-role scenario/10-cli-export

# Optional starting-point tags (if you created them locally)
git push origin --tags
```

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable baseline; production tests green; fixture tests intentionally fail |
| `scenario/*` | Planted production bugs for agent scenarios 01, 03, 10 |
| Feature branches | Agent or human fixes; open PRs against `main` or a scenario branch |

Checkout helpers:

```bash
make scenario NUM=01   # scenario/01-jwt-expiry
make scenario NUM=03   # scenario/03-viewer-role
make scenario NUM=10   # scenario/10-cli-export
```

Fixture-only scenarios (04–09, 11–12) run on `main` — see [docs/agent-scenarios/README.md](agent-scenarios/README.md).

## CI workflows

| Workflow | Trigger | What it checks |
|----------|---------|----------------|
| [CI](../.github/workflows/ci.yml) | PRs + pushes to `main` / `scenario/**` | API matrix (Python 3.11/3.12 + Postgres), web (Node 20), worker (Go 1.22), OpenAPI contract |
| [Codegen Check](../.github/workflows/codegen-check.yml) | OpenAPI / api-client changes | `docs/api/openapi.yaml` ↔ `@meridian/api-client` via `contract-manifest.json` |
| [Agent Scenario Smoke](../.github/workflows/agent-scenario-smoke.yml) | Pushes to `main` | API smoke tests + scenario doc count |

Add status badges to your fork’s README:

```markdown
![CI](https://github.com/YOUR_ORG/meridian/actions/workflows/ci.yml/badge.svg)
```

## Local parity with CI

```bash
# Full local CI mirror (requires Postgres on localhost:5432)
make ci

# Contract check only
make codegen-check
```

## Running agent evaluations

1. Check out the scenario branch (or stay on `main` for fixtures).
2. Give the agent **only** the user prompt from the scenario doc.
3. Verify with acceptance criteria (not shared with the agent).
4. File a result with the [agent scenario issue template](../.github/ISSUE_TEMPLATE/agent-scenario.md).

Expected test behavior on `main`:

- `make api-test` / `make worker-test` / web tests — **pass**
- `make fixture-test` — **fails** until an agent fixes the planted issues

## Secrets (optional)

Meridian CI does not require secrets for the default workflows. If you add deployment or coverage uploads later, configure them under **Settings → Secrets and variables → Actions**.