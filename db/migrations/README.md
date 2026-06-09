# Database Migrations

Migrations are numbered sequentially (`001_`, `002_`, ...). **Never edit old migrations** — add a new file instead.

Run order is enforced by filename. Postgres init runs all files in `db/migrations/` on first container boot via `scripts/init-db.sh`.