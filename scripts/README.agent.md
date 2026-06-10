# Meridian

A team collaboration platform for managing projects, tasks, and team workflows.

## Repo Map

```
meridian/
├── apps/
│   ├── web/          → React + Vite frontend
│   ├── api/          → Python FastAPI backend
│   ├── worker/       → Go background job processor
│   └── cli/          → Admin CLI
├── packages/
│   ├── api-client/   → TypeScript API client
│   ├── shared-types/ → Shared type definitions
│   ├── ui-kit/       → Shared React components
│   └── config/       → Feature flags and shared config
├── db/
│   ├── migrations/   → PostgreSQL schema
│   └── seeds/        → Seed data directory
├── lib/              → Internal libraries and utilities
├── docs/
│   ├── architecture/ → System design docs
│   └── api/          → OpenAPI spec
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

## Running Tests

```bash
make api-test          # requires Postgres
make web-test
make worker-test
make fixture-test      # internal library tests
make ci                # full local CI mirror
```

## Conventions

- UUIDs for all entity IDs
- API errors: `{ "error": { "code", "message", "details" } }`
- Never edit old DB migrations — add new numbered files
- OpenAPI spec is the API contract source of truth