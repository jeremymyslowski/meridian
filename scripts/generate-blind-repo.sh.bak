#!/bin/bash
# Generate a sanitized blind copy of Meridian for agent evaluation.
# Usage:
#   ./scripts/generate-blind-repo.sh --output ../meridian-blind
#   ./scripts/generate-blind-repo.sh --output ../meridian-blind --branch scenario/01-jwt-expiry --blind-branch fix/session-timeout
#   ./scripts/generate-blind-repo.sh --output ../meridian-blind --scenario 07
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT=""
SOURCE_BRANCH="main"
BLIND_BRANCH=""
SCENARIO=""
LIB_NAME="lib"

usage() {
  echo "Usage: $0 --output DIR [--branch BRANCH] [--blind-branch NAME] [--scenario NN]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    --branch) SOURCE_BRANCH="$2"; shift 2 ;;
    --blind-branch) BLIND_BRANCH="$2"; shift 2 ;;
    --scenario) SCENARIO="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

[[ -n "$OUTPUT" ]] || usage

# Resolve source branch in canonical repo
cd "$ROOT"
if ! git rev-parse --verify "$SOURCE_BRANCH" >/dev/null 2>&1; then
  echo "Source branch not found: $SOURCE_BRANCH" >&2
  exit 1
fi

WORKTREE=$(mktemp -d)
trap 'rm -rf "$WORKTREE"' EXIT

echo "==> Exporting $SOURCE_BRANCH to temp worktree"
git archive "$SOURCE_BRANCH" | tar -x -C "$WORKTREE"

echo "==> Removing evaluator-only files"
rm -rf "$WORKTREE/docs/agent-scenarios"
rm -f "$WORKTREE/docs/qa-guide.md"
rm -f "$WORKTREE/docs/github.md"
rm -f "$WORKTREE/docs/blind-mapping.json"
rm -f "$WORKTREE/qa-fixtures/README.md"
find "$WORKTREE/qa-fixtures" -name 'README.md' -delete 2>/dev/null || true
rm -rf "$WORKTREE/.github/ISSUE_TEMPLATE"
rm -f "$WORKTREE/.github/pull_request_template.md"
rm -f "$WORKTREE/scripts/checkout-scenario.sh"
rm -f "$WORKTREE/scripts/generate-blind-repo.sh"
rm -f "$WORKTREE/scripts/sanitize-comments.py"
rm -f "$WORKTREE/packages/config/README.md"
rm -rf "$WORKTREE/prompts"

# Scenario-filtered fixture tree
if [[ -n "$SCENARIO" ]]; then
  echo "==> Filtering fixtures for scenario $SCENARIO"
  FIXTURE_TMP=$(mktemp -d)
  case "$SCENARIO" in
    01|02|03|10)
      rm -rf "$WORKTREE/qa-fixtures"
      ;;
    04)
      mkdir -p "$FIXTURE_TMP/anti-patterns/duplicated_validation"
      cp -R "$WORKTREE/qa-fixtures/anti-patterns/duplicated_validation/." "$FIXTURE_TMP/anti-patterns/duplicated_validation/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    05)
      mkdir -p "$FIXTURE_TMP/partial-implementations/webhook-retry"
      cp -R "$WORKTREE/qa-fixtures/partial-implementations/webhook-retry/." "$FIXTURE_TMP/partial-implementations/webhook-retry/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    06)
      mkdir -p "$FIXTURE_TMP/naming-traps"
      cp -R "$WORKTREE/qa-fixtures/naming-traps/." "$FIXTURE_TMP/naming-traps/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    07)
      mkdir -p "$FIXTURE_TMP/broken-tests/python"
      cp -R "$WORKTREE/qa-fixtures/broken-tests/python/." "$FIXTURE_TMP/broken-tests/python/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    08)
      mkdir -p "$FIXTURE_TMP/large-files"
      cp -R "$WORKTREE/qa-fixtures/large-files/." "$FIXTURE_TMP/large-files/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    09)
      mkdir -p "$FIXTURE_TMP/anti-patterns/magic_strings"
      cp -R "$WORKTREE/qa-fixtures/anti-patterns/magic_strings/." "$FIXTURE_TMP/anti-patterns/magic_strings/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    11)
      mkdir -p "$FIXTURE_TMP/edge-cases/circular"
      cp -R "$WORKTREE/qa-fixtures/edge-cases/circular/." "$FIXTURE_TMP/edge-cases/circular/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    12)
      mkdir -p "$FIXTURE_TMP/edge-cases/unicode_dir"
      cp -R "$WORKTREE/qa-fixtures/edge-cases/unicode_dir/." "$FIXTURE_TMP/edge-cases/unicode_dir/"
      rm -rf "$WORKTREE/qa-fixtures"
      mkdir -p "$WORKTREE/qa-fixtures"
      cp -R "$FIXTURE_TMP/." "$WORKTREE/qa-fixtures/"
      ;;
    *)
      echo "Unknown scenario: $SCENARIO" >&2
      exit 1
      ;;
  esac
  rm -rf "$FIXTURE_TMP"
fi

echo "==> Renaming qa-fixtures -> $LIB_NAME"
if [[ -d "$WORKTREE/qa-fixtures" ]]; then
  mv "$WORKTREE/qa-fixtures" "$WORKTREE/$LIB_NAME"
fi

# Neutral decoy folder names
if [[ -d "$WORKTREE/$LIB_NAME/naming-traps/decoy-frontend" ]]; then
  mkdir -p "$WORKTREE/$LIB_NAME/naming-traps/legacy"
  mv "$WORKTREE/$LIB_NAME/naming-traps/decoy-frontend" "$WORKTREE/$LIB_NAME/naming-traps/legacy/frontend-services"
  mv "$WORKTREE/$LIB_NAME/naming-traps/decoy-legacy" "$WORKTREE/$LIB_NAME/naming-traps/legacy/scripts"
  mv "$WORKTREE/$LIB_NAME/naming-traps/decoy-worker" "$WORKTREE/$LIB_NAME/naming-traps/legacy/worker-prototype"
fi

echo "==> Sanitizing spoiler comments"
python3 "$ROOT/scripts/sanitize-comments.py" "$WORKTREE"

echo "==> Rewriting paths (qa-fixtures -> $LIB_NAME)"
if command -v rg >/dev/null 2>&1; then
  FILES=$(rg -l 'qa-fixtures|decoy-frontend|decoy-legacy|decoy-worker' "$WORKTREE" 2>/dev/null || true)
else
  FILES=$(grep -rl 'qa-fixtures\|decoy-frontend\|decoy-legacy\|decoy-worker' "$WORKTREE" 2>/dev/null || true)
fi
for f in $FILES; do
  [[ -f "$f" ]] || continue
  sed -i '' \
    -e "s|qa-fixtures|$LIB_NAME|g" \
    -e 's|decoy-frontend|legacy/frontend-services|g' \
    -e 's|decoy-legacy|legacy/scripts|g' \
    -e 's|decoy-worker|legacy/worker-prototype|g' \
    "$f" 2>/dev/null || sed -i \
    -e "s|qa-fixtures|$LIB_NAME|g" \
    -e 's|decoy-frontend|legacy/frontend-services|g' \
    -e 's|decoy-legacy|legacy/scripts|g' \
    -e 's|decoy-worker|legacy/worker-prototype|g' \
    "$f"
done

echo "==> Writing neutral README"
cp "$ROOT/scripts/README.agent.md" "$WORKTREE/README.md"

echo "==> Copying user prompts"
mkdir -p "$WORKTREE/prompts"
for p in "$ROOT/prompts"/*.md; do
  [[ -f "$p" ]] || continue
  sed \
    -e "s|qa-fixtures|$LIB_NAME|g" \
    -e 's|decoy-frontend|legacy/frontend-services|g' \
    -e 's|decoy-legacy|legacy/scripts|g' \
    -e 's|decoy-worker|legacy/worker-prototype|g' \
    "$p" > "$WORKTREE/prompts/$(basename "$p")"
done

echo "==> Patching Makefile (remove scenario target)"
if [[ -f "$WORKTREE/Makefile" ]]; then
  sed -i '' '/^scenario:/,/^[^[:space:]]/d' "$WORKTREE/Makefile" 2>/dev/null || \
  sed -i '/^scenario:/,/^[^[:space:]]/d' "$WORKTREE/Makefile"
  sed -i '' 's/qa-fixtures/lib/g' "$WORKTREE/Makefile" 2>/dev/null || sed -i 's/qa-fixtures/lib/g' "$WORKTREE/Makefile"
fi

if [[ -f "$WORKTREE/scripts/run-fixture-tests.sh" ]]; then
  sed -i '' "s|qa-fixtures|$LIB_NAME|g" "$WORKTREE/scripts/run-fixture-tests.sh" 2>/dev/null || \
  sed -i "s|qa-fixtures|$LIB_NAME|g" "$WORKTREE/scripts/run-fixture-tests.sh"
  sed -i '' '/expected until fixed/d' "$WORKTREE/scripts/run-fixture-tests.sh" 2>/dev/null || \
  sed -i '/expected until fixed/d' "$WORKTREE/scripts/run-fixture-tests.sh"
fi

if [[ -f "$WORKTREE/docker-compose.yml" ]]; then
  sed -i '' "s|qa-fixtures|$LIB_NAME|g" "$WORKTREE/docker-compose.yml" 2>/dev/null || \
  sed -i "s|qa-fixtures|$LIB_NAME|g" "$WORKTREE/docker-compose.yml"
fi

# Remove agent-scenario-smoke workflow (references hidden docs)
rm -f "$WORKTREE/.github/workflows/agent-scenario-smoke.yml"

echo "==> Syncing to $OUTPUT"
mkdir -p "$(dirname "$OUTPUT")"
rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"
cp -R "$WORKTREE/." "$OUTPUT/"

if [[ ! -d "$OUTPUT/.git" ]]; then
  echo "==> Initializing git in blind repo"
  git -C "$OUTPUT" init -b main
  git -C "$OUTPUT" add -A
  git -C "$OUTPUT" commit -m "Blind repo generated from meridian ($SOURCE_BRANCH)"
else
  git -C "$OUTPUT" add -A
  git -C "$OUTPUT" commit -m "Regenerate blind repo from meridian ($SOURCE_BRANCH)" || true
fi

if [[ -n "$BLIND_BRANCH" && "$BLIND_BRANCH" != "main" ]]; then
  git -C "$OUTPUT" checkout -B "$BLIND_BRANCH"
fi

echo ""
echo "Blind repo ready: $OUTPUT"
echo "  Source branch:  $SOURCE_BRANCH"
[[ -n "$BLIND_BRANCH" ]] && echo "  Blind branch:   $BLIND_BRANCH"
[[ -n "$SCENARIO" ]] && echo "  Scenario filter: $SCENARIO"
echo ""
echo "Open ONLY this directory in Cursor when running agents."
echo "Score runs against docs/agent-scenarios/ in the canonical meridian repo."
