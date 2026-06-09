# Meridian

A fictional team collaboration SaaS platform — built as a QA testing repository for AI coding agents.

## Repo Map

```
meridian/
├── apps/
│   ├── web/          → React + Vite frontend
│   ├── api/          → Python FastAPI backend
│   ├── worker/       → Go background job processor
│   └── cli/          → Admin CLI (stub)
├── packages/
│   ├── api-client/   → TypeScript API client
│   ├── shared-types/ → Shared type definitions
│   ├── ui-kit/       → Shared React components (Button, DataTable, Modal, …)
│   └── config/       → Feature flags and shared config
├── db/
│   ├── migrations/   → PostgreSQL schema (001–005)
│   └── seeds/        → Seed data directory
├── docs/
│   ├── architecture/ → System design docs
│   ├── api/          → OpenAPI spec
│   └── agent-scenarios/ → Agent QA playbooks (Phase 4)
├── qa-fixtures/      → Isolated agent challenge zones (Phase 3)
└── scripts/          → Bootstrap and seed helpers
```

**Start here:**
- Architecture overview: [docs/architecture/overview.md](docs/architecture/overview.md)
- API contract: [docs/api/openapi.yaml](docs/api/openapi.yaml)
- DB migrations: [db/migrations/README.md](db/migrations/README.md)

## Quick Start

Requires **Docker Desktop** running.

```bash
cp .env.example .env
make dev          # builds images and starts all services in background
make seed         # loads demo data (run once after first boot)
```

Open http://localhost:5173 and log in with `user1@example.com` / `password123`.

To watch logs: `docker compose logs -f`

To reset everything (including DB): `docker compose down -v && make dev && make seed`

## Services

| Service  | URL                    | Tech              |
|----------|------------------------|-------------------|
| Web      | http://localhost:5173  | React + Vite      |
| API      | http://localhost:8000  | Python + FastAPI  |
| API docs | http://localhost:8000/docs | Swagger UI  |
| Postgres | localhost:5432         | PostgreSQL 16     |
| Redis    | localhost:6379         | Redis 7           |
| Worker   | (background)           | Go                |

## User Flow (Phase 1)

1. **Login** — JWT auth against seeded users
2. **Projects** — list projects for your teams
3. **Task board** — kanban view (todo / in progress / done)
4. **Task detail** — view task and add comments
5. **Worker** — assignment events create notifications in the background

## Running Tests

```bash
# API tests (requires running Postgres)
make api-test

# Web tests
cd apps/web && npm install && npm test -- --run

# Worker tests
make worker-test
```

## Conventions

- UUIDs for all entity IDs
- API errors: `{ "error": { "code", "message", "details" } }`
- Never edit old DB migrations — add new numbered files
- OpenAPI spec is the API contract source of truth

## Phase 2 Features

- **RBAC** — owner / member / viewer roles enforced in API; UI hides edit controls for viewers
- **Pagination** — paginated task list with status filtering (`/projects/:id/list`)
- **Analytics** — dashboard at `/analytics` with task status breakdown
- **Attachments** — S3-stub file metadata on tasks
- **Webhooks** — outbound event queue processed by Go worker
- **Feature flags** — `packages/config/feature-flags.json`
- **Observability** — structured JSON logging + `X-Request-ID` in API and worker
- **UI Kit** — `@meridian/ui-kit` with 11 shared components

## Phase Roadmap

- [x] **Phase 1** — Vertical slice (login → tasks → comments)
- [x] **Phase 2** — RBAC, pagination, ui-kit, analytics, webhooks
- [ ] **Phase 3** — QA fixtures (naming traps, large files, broken tests)
- [ ] **Phase 4** — Agent scenario playbook
- [ ] **Phase 5** — CI matrix, GitHub publish