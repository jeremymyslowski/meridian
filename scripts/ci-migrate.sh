#!/bin/bash
# Apply all Meridian DB migrations in order (for CI and local Postgres).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATABASE_URL="${DATABASE_URL:-postgresql://meridian:meridian@localhost:5432/meridian}"

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required but not installed" >&2
  exit 1
fi

echo "Migrating database: ${DATABASE_URL%%\?*}"
for migration in "$ROOT"/db/migrations/*.sql; do
  echo "  -> $(basename "$migration")"
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$migration"
done
echo "Migrations complete."