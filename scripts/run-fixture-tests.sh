#!/bin/bash

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== QA Fixtures Test Runner ==="
echo ""

run_pytest() {
  local dir="$1"
  if docker compose ps api 2>/dev/null | grep -q "Up"; then
    docker compose exec -T api pip install -q pytest 2>/dev/null || true
    docker compose exec -T api python -m pytest -v "/qa-fixtures/${dir#qa-fixtures/}"
  elif python3 -m pytest --version >/dev/null 2>&1; then
    (cd "$dir" && python3 -m pytest -v)
  else
    echo "SKIP: pytest not available. Start Docker (make dev) or install pytest."
    return 1
  fi
}

run_zone() {
  local name="$1"
  local dir="$2"
  echo "--- $name ---"
  if run_pytest "$dir"; then
    echo "PASS: $name"
  else
    echo "FAIL (may be expected): $name"
  fi
  echo ""
}

run_zone "large-files" "qa-fixtures/large-files"
run_zone "broken-tests" "qa-fixtures/broken-tests/python"
run_zone "partial-implementations" "qa-fixtures/partial-implementations/webhook-retry"

echo "Done. Failures in broken-tests and partial-implementations are expected until fixed."