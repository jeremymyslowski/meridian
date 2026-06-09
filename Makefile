.PHONY: dev down test seed migrate api-test web-test worker-test lint

dev:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose exec postgres psql -U meridian -d meridian -f /docker-entrypoint-initdb.d/migrations/001_users_teams.sql
	docker compose exec postgres psql -U meridian -d meridian -f /docker-entrypoint-initdb.d/migrations/002_projects.sql
	docker compose exec postgres psql -U meridian -d meridian -f /docker-entrypoint-initdb.d/migrations/003_tasks.sql
	docker compose exec postgres psql -U meridian -d meridian -f /docker-entrypoint-initdb.d/migrations/004_comments.sql
	docker compose exec postgres psql -U meridian -d meridian -f /docker-entrypoint-initdb.d/migrations/005_notifications.sql

seed:
	pip3 install -q -r scripts/requirements.txt 2>/dev/null || true
	python3 scripts/seed.py

test: api-test web-test worker-test

api-test:
	cd apps/api && python3 -m pytest tests/ -v

web-test:
	cd apps/web && npm test -- --run

worker-test:
	cd apps/worker && go test ./...

lint:
	cd apps/api && python3 -m ruff check .
	cd apps/web && npm run lint

setup-local:
	cp -n .env.example .env 2>/dev/null || true
	cd apps/api && pip install -r requirements.txt
	cd apps/web && npm install
	cd apps/worker && go mod download