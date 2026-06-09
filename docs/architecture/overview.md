# Meridian Architecture

Meridian is a team collaboration platform built as a monorepo with four applications:

- **web** — React SPA for project and task management
- **api** — Python FastAPI REST API (source of truth for business logic)
- **worker** — Go background processor for notifications and webhooks
- **cli** — Python admin tooling (Phase 2)

## Data Flow

1. Users interact with the React web app
2. Web calls the API via `@meridian/api-client`
3. API reads/writes PostgreSQL
4. Task assignment events are queued in `task_assignment_events`
5. Go worker polls the queue and creates `notifications` records

## Conventions

- All IDs are UUIDs (see `ids.md`)
- API errors use shape `{ "error": { "code", "message", "details" } }`
- OpenAPI spec in `docs/api/openapi.yaml` is the contract source of truth