# Meridian QA Guide

How to use this repository to evaluate AI coding agents — what to test, where things break on purpose, and how to run evaluations that produce useful scores.

Meridian is not a product QA suite. It is a **controlled environment** for measuring whether an agent can navigate a realistic monorepo, edit the right files, respect contracts, and leave the codebase in a better state than it found it.

---

## What you are QA-ing

Every scenario probes one or more **agent capabilities**. Group your evaluations around these dimensions:

| Capability | What it measures | Where to test it |
|------------|------------------|------------------|
| **Navigation** | Finds the correct file among similar names, languages, and folder depths | `qa-fixtures/naming-traps/`, `edge-cases/nested/` |
| **Cross-layer reasoning** | Traces a bug or feature across API, web, worker, and config | Scenarios 01, 03, 10 |
| **Contract discipline** | Reads OpenAPI, migrations, and error shapes instead of inventing APIs | Scenarios 02, 10; `docs/api/openapi.yaml` |
| **RBAC & policy** | Applies authorization consistently at every layer | Scenario 03; `apps/api/meridian_api/policies.py` |
| **Test literacy** | Reads failure output, fixes root cause, does not delete tests | `qa-fixtures/broken-tests/` |
| **Surgical editing** | Makes a small fix in a large or noisy file | `qa-fixtures/large-files/` |
| **Refactoring judgment** | Extracts shared logic without scope creep | `qa-fixtures/anti-patterns/` |
| **Incomplete feature completion** | Wires stubs across multiple files with correct naming | `qa-fixtures/partial-implementations/` |
| **Repo hygiene** | Avoids editing decoys, generated code, or `qa-fixtures/` when the task is production | Scenario 06; all naming-trap prompts |
| **Minimal diff** | Solves the stated problem without unrelated refactors | All scenarios |

A strong agent passes the **stated task** and keeps **production CI green**. A weak agent often passes a superficial check while breaking something else — or edits a convincing-looking wrong file.

---

## Two zones: production vs fixtures

Meridian deliberately splits the repo into two areas. Understanding this split is the foundation of effective QA.

### Production zone (`apps/`, `packages/`, `db/`)

Realistic SaaS code: React frontend, FastAPI backend, Go worker, shared packages, Postgres migrations.

- **On `main`:** production tests are expected to **pass** (`make api-test`, `make web-test`, `make worker-test`, GitHub Actions CI).
- **On `scenario/*` branches:** intentional bugs are planted for specific scenarios (01, 03, 10). Production tests may fail until the agent fixes the planted issue.

Use production scenarios when you want to measure whether an agent can debug and extend a system that looks like real work.

### Fixture zone (`qa-fixtures/`)

Isolated traps and puzzles. **Never imported by production code.** Each subfolder targets a specific failure mode.

- **On `main`:** `make fixture-test` is expected to **fail** in `broken-tests` and `partial-implementations` until an agent fixes them.
- Passing fixture tests after a run is a positive signal. Leaving them broken means the agent did not finish (or made things worse).

Use fixture scenarios when you want to isolate one skill (navigation, test fixing, large-file surgery) without noise from the full app.

---

## Fixture zones and edge cases

### Naming traps

**Edge case:** Four "user service" files exist across TypeScript, Python, and Go. Grep returns decoys first.

| File | Verdict |
|------|---------|
| `qa-fixtures/naming-traps/decoy-frontend/UserService.ts` | Decoy |
| `qa-fixtures/naming-traps/decoy-legacy/user_service.py` | Decoy |
| `qa-fixtures/naming-traps/decoy-worker/internal/user/user.go` | Decoy |
| `apps/api/meridian_api/services/user_service.py` | **Correct** |

**Watch for:** Agent edits a decoy, creates a new file instead of finding the existing service, or implements the feature in the React layer when the prompt implied backend.

### Large files

**Edge case:** `task_registry.py` is ~1,100 lines of repetitive handlers. The bug is in `normalize_task_title` near the bottom.

**Watch for:** Agent rewrites the whole file, edits a similarly named handler, or adds a parallel utility module instead of fixing the one function.

### Broken tests

**Edge case:** Tests fail for documented, distinct reasons — not because the runner is broken.

| Test | Root cause | Wrong "fix" |
|------|------------|-------------|
| `test_off_by_one.py` | Loop excludes last element | Delete the test |
| `test_wrong_assertion.py` | Expected status code is wrong | Mock the HTTP layer |
| `test_missing_fixture.py` | Undefined `db_session` fixture | Edit production API code |

**Watch for:** Agent deletes failing tests, mocks everything, or "fixes" unrelated production code in `apps/`.

### Partial implementations

**Edge case:** Webhook retry is split across `event_queue.py`, `retry_policy.py`, and `dispatcher.py` with TODOs. Note: the queue module is named `event_queue.py` (not `queue.py`) to avoid clashing with the Python stdlib — agents that blindly create `queue.py` cause import confusion.

**Watch for:** Agent completes one file and declares done, uses wrong module names, or implements retry logic that never dispatches.

### Anti-patterns

**Edge case:** God objects, four copies of the same email validator, undocumented magic error codes like `TEAM_42`.

**Watch for:** Agent rewrites everything instead of extracting one shared module, or invents error mappings without reading `legacy_errors.py`.

### Edge-case layout

**Edge case:** Circular imports, six-level nested config paths, directories named `unicode_dir` (ASCII paths only — no Unicode filenames), and files marked `GENERATED CODE`.

**Watch for:** Agent hand-edits generated clients, breaks circular imports by deleting modules, or gives up on deep paths instead of searching.

---

## Scenario playbook (12 tasks)

Each scenario in `docs/agent-scenarios/` has a **user prompt** (give this to the agent), **acceptance criteria** (keep this for yourself), and **common failure modes**.

| # | Focus | Branch | Expected test outcome |
|---|-------|--------|------------------------|
| 01 | Cross-layer config (JWT TTL web vs API) | `scenario/01-jwt-expiry` | `make api-test`, web tests pass |
| 02 | Feature work against OpenAPI contract | `main` | CI green; contract still valid |
| 03 | RBAC across API, UI, worker | `scenario/03-viewer-role` | API tests pass; viewers get 403 on writes |
| 04 | Refactor duplicated validation | `main` | Fixture zone tests pass |
| 05 | Complete multi-file webhook retry | `main` | `partial-implementations` tests pass |
| 06 | Naming trap navigation | `main` | No edits under `qa-fixtures/naming-traps/` |
| 07 | Diagnose broken tests | `main` | `broken-tests` zone passes |
| 08 | Surgical fix in large file | `main` | `large-files` tests pass |
| 09 | Read legacy code, don't invent | `main` | Correct error mapping documented |
| 10 | CLI feature + API integration | `scenario/10-cli-export` | CLI runs; uses real API patterns |
| 11 | Fix circular imports | `main` | Both modules import cleanly |
| 12 | Validator edge cases (empty names) | `main` | Validator rejects empty input |

Full prompts and checklists: [docs/agent-scenarios/README.md](agent-scenarios/README.md).

---

## Where tests fail (and what that means)

### Expected failures on `main` (before any agent run)

```bash
make fixture-test
```

| Zone | Expected on `main` | Meaning if still failing after agent |
|------|--------------------|-------------------------------------|
| `large-files` | May fail until scenario 08 fix | Agent did not find or fix `normalize_task_title` |
| `broken-tests` | **Fails** (3 tests) | Agent did not diagnose test root causes |
| `partial-implementations` | **Fails** | Agent did not complete webhook retry stubs |

### Expected passes on `main`

```bash
make api-test      # 12 tests — needs Postgres (make dev)
make web-test      # Vitest unit tests
make worker-test   # Go worker tests
make codegen-check # OpenAPI ↔ api-client contract
```

GitHub Actions runs the same production checks on every PR. **CI red on `main` after an agent run is a serious failure** — the agent broke production.

### Scenario branch failures (before fix)

| Branch | Planted issue | CI impact |
|--------|---------------|-----------|
| `scenario/01-jwt-expiry` | Web session TTL = 30 min, API = 60 min | Tests may pass; behavior is wrong |
| `scenario/03-viewer-role` | Viewers can write via API; worker notifies viewers | `test_viewer_cannot_create_task` may fail |
| `scenario/10-cli-export` | CLI is a stub | No export command exists |

Always record **both** whether acceptance criteria passed and whether unrelated tests regressed.

---

## Effective QA approach

### 1. Run one scenario at a time

Mixed prompts produce mixed scores. Give the agent **only** the user prompt from the scenario doc — not acceptance criteria, not file paths, not this guide.

```bash
make scenario NUM=01   # production bug scenarios
# fixture scenarios: stay on main
```

### 2. Fix the environment first

```bash
make dev    # Postgres, API, web, worker
make seed   # demo data (first time only)
```

For API tests without Docker: Postgres on `localhost:5432` with migrations applied (`scripts/ci-migrate.sh`).

### 3. Verify in layers

After the agent finishes, check in this order:

1. **Diff scope** — `git diff --name-only`. Did it touch decoys, unrelated apps, or the whole repo?
2. **Acceptance criteria** — scenario doc checklist (403 for viewers, TTL aligned, etc.).
3. **Production tests** — `make api-test`, `make web-test`, `make worker-test`.
4. **Fixture tests** — `make fixture-test` (if the scenario targets `qa-fixtures/`).
5. **Contract** — `make codegen-check` if API or client changed.

### 4. Score consistently

| Result | Definition |
|--------|------------|
| **Pass** | All acceptance criteria met; production CI green; minimal unrelated changes |
| **Partial** | Core task works but missed edge cases, extra files changed, or one test suite still fails |
| **Fail** | Wrong file edited, tests deleted to go green, hallucinated API, or production CI broken |

Record failure modes from the scenario doc (e.g. "fixed API TTL instead of frontend", "edited decoy UserService.ts"). Patterns across runs matter more than a single score.

### 5. Compare agents on the same starting point

- Use the same branch (`main` or `scenario/NN-*`).
- Optionally tag starting points: `scenario-01-start`, etc.
- Reset between runs: `git checkout . && git clean -fd` or re-clone.

### 6. Weight scenarios by what you care about

Suggested bundles:

| Goal | Run these |
|------|-----------|
| **Onboarding / navigation** | 06, 08, 11 |
| **Realistic product work** | 01, 02, 03, 10 |
| **Test & debug discipline** | 07, 01, 03 |
| **Refactor quality** | 04, 09, anti-patterns zone |
| **Full battery** | All 12, in random order |

---

## What good agents do differently

Agents that score well tend to:

- Search before reading (`grep`, `rg`) and read zone READMEs when they land in `qa-fixtures/`
- Trace cross-layer bugs by following config and env vars, not guessing
- Fix the smallest correct surface (one function, one constant, one policy check)
- Run tests and read stderr instead of asserting success
- Leave `qa-fixtures/` untouched when the prompt targets production

Agents that score poorly tend to:

- Edit the first grep hit
- Add refresh-token infrastructure for a constant mismatch
- Hide UI buttons while leaving the API open (or vice versa)
- Delete or skip failing tests
- Hand-edit files marked `GENERATED CODE`
- Refactor unrelated code "while they're in there"

---

## Recording results

Use the GitHub issue template (`.github/ISSUE_TEMPLATE/agent-scenario.md`) or a simple spreadsheet:

| Field | Example |
|-------|---------|
| Scenario | 06 |
| Agent / model | — |
| Branch | `main` |
| Result | Partial |
| Files touched | 2 production, 0 decoys |
| Tests | api ✓, fixture ✗ |
| Failure modes | Edited decoy first, self-corrected |

Over time, aggregate **failure mode frequency** — that tells you what to improve in prompts, tooling, or training — more than a single pass/fail.

---

## Quick reference

```bash
# Start environment
make dev && make seed

# Production test suite (should pass on main)
make api-test && make web-test && make worker-test

# Fixture suite (expected failures on main until fixed)
make fixture-test

# Full local CI mirror
make ci

# Scenario checkout
make scenario NUM=01

# Contract check
make codegen-check
```

**Related docs:**

- [Agent scenario playbook](agent-scenarios/README.md) — prompts and per-scenario criteria
- [QA fixtures README](../qa-fixtures/README.md) — zone details
- [GitHub publishing guide](github.md) — CI and branch strategy
- [Architecture overview](architecture/overview.md) — system design