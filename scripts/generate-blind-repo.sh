#!/bin/bash
# Generate a sanitized blind copy of Meridian for agent evaluation.
#
# Full mirror (all branches, all lib/ zones):
#   ./scripts/generate-blind-repo.sh --output ../meridian-blind --all-branches
#
# Single branch:
#   ./scripts/generate-blind-repo.sh --output ../meridian-blind --branch scenario/01-jwt-expiry --blind-branch fix/session-timeout
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT=""
SOURCE_BRANCH="main"
BLIND_BRANCH=""
SCENARIO=""
ALL_BRANCHES=false
LIB_NAME="lib"

usage() {
  echo "Usage: $0 --output DIR [--all-branches | --branch BRANCH [--blind-branch NAME] [--scenario NN]]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    --branch) SOURCE_BRANCH="$2"; shift 2 ;;
    --blind-branch) BLIND_BRANCH="$2"; shift 2 ;;
    --scenario) SCENARIO="$2"; shift 2 ;;
    --all-branches) ALL_BRANCHES=true; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

[[ -n "$OUTPUT" ]] || usage

if $ALL_BRANCHES && { [[ -n "$SCENARIO" ]] || [[ -n "$BLIND_BRANCH" ]] || [[ "$SOURCE_BRANCH" != "main" ]]; }; then
  echo "--all-branches cannot be combined with --branch, --blind-branch, or --scenario" >&2
  exit 1
fi

cd "$ROOT"

sed_inplace() {
  if sed --version >/dev/null 2>&1; then
    sed -i "$@"
  else
    sed -i '' "$@"
  fi
}

filter_fixtures() {
  local worktree="$1"
  [[ -n "$SCENARIO" ]] || return 0
  echo "==> Filtering fixtures for scenario $SCENARIO"
  local fixture_tmp
  fixture_tmp=$(mktemp -d)
  case "$SCENARIO" in
    01|02|03|10) rm -rf "$worktree/qa-fixtures" ;;
    04)
      mkdir -p "$fixture_tmp/anti-patterns/duplicated_validation"
      cp -R "$worktree/qa-fixtures/anti-patterns/duplicated_validation/." "$fixture_tmp/anti-patterns/duplicated_validation/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    05)
      mkdir -p "$fixture_tmp/partial-implementations/webhook-retry"
      cp -R "$worktree/qa-fixtures/partial-implementations/webhook-retry/." "$fixture_tmp/partial-implementations/webhook-retry/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    06)
      mkdir -p "$fixture_tmp/naming-traps"
      cp -R "$worktree/qa-fixtures/naming-traps/." "$fixture_tmp/naming-traps/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    07)
      mkdir -p "$fixture_tmp/broken-tests/python"
      cp -R "$worktree/qa-fixtures/broken-tests/python/." "$fixture_tmp/broken-tests/python/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    08)
      mkdir -p "$fixture_tmp/large-files"
      cp -R "$worktree/qa-fixtures/large-files/." "$fixture_tmp/large-files/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    09)
      mkdir -p "$fixture_tmp/anti-patterns/magic_strings"
      cp -R "$worktree/qa-fixtures/anti-patterns/magic_strings/." "$fixture_tmp/anti-patterns/magic_strings/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    11)
      mkdir -p "$fixture_tmp/edge-cases/circular"
      cp -R "$worktree/qa-fixtures/edge-cases/circular/." "$fixture_tmp/edge-cases/circular/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    12)
      mkdir -p "$fixture_tmp/edge-cases/unicode_dir"
      cp -R "$worktree/qa-fixtures/edge-cases/unicode_dir/." "$fixture_tmp/edge-cases/unicode_dir/"
      rm -rf "$worktree/qa-fixtures" && mkdir -p "$worktree/qa-fixtures" && cp -R "$fixture_tmp/." "$worktree/qa-fixtures/" ;;
    *) echo "Unknown scenario: $SCENARIO" >&2; exit 1 ;;
  esac
  rm -rf "$fixture_tmp"
}

process_worktree() {
  local worktree="$1"
  echo "==> Removing evaluator-only files"
  rm -rf "$worktree/docs/agent-scenarios"
  rm -f "$worktree/docs/qa-guide.md" "$worktree/docs/github.md" "$worktree/docs/blind-mapping.json"
  rm -f "$worktree/docs/github-mcp-fixtures.md"
  rm -f "$worktree/qa-fixtures/README.md"
  find "$worktree/qa-fixtures" -name 'README.md' -delete 2>/dev/null || true
  rm -rf "$worktree/.github/ISSUE_TEMPLATE"
  rm -f "$worktree/.github/pull_request_template.md"
  rm -f "$worktree/scripts/checkout-scenario.sh" "$worktree/scripts/generate-blind-repo.sh" "$worktree/scripts/sanitize-comments.py"
  rm -f "$worktree/packages/config/README.md"
  rm -rf "$worktree/prompts"
  filter_fixtures "$worktree"
  echo "==> Renaming qa-fixtures -> $LIB_NAME"
  [[ -d "$worktree/qa-fixtures" ]] && mv "$worktree/qa-fixtures" "$worktree/$LIB_NAME"
  if [[ -d "$worktree/$LIB_NAME/naming-traps/decoy-frontend" ]]; then
    mkdir -p "$worktree/$LIB_NAME/naming-traps/legacy"
    mv "$worktree/$LIB_NAME/naming-traps/decoy-frontend" "$worktree/$LIB_NAME/naming-traps/legacy/frontend-services"
    mv "$worktree/$LIB_NAME/naming-traps/decoy-legacy" "$worktree/$LIB_NAME/naming-traps/legacy/scripts"
    mv "$worktree/$LIB_NAME/naming-traps/decoy-worker" "$worktree/$LIB_NAME/naming-traps/legacy/worker-prototype"
  fi
  echo "==> Sanitizing spoiler comments"
  python3 "$ROOT/scripts/sanitize-comments.py" "$worktree"
  echo "==> Rewriting paths"
  local files=""
  if command -v rg >/dev/null 2>&1; then
    files=$(rg -l 'qa-fixtures|decoy-frontend|decoy-legacy|decoy-worker' "$worktree" 2>/dev/null || true)
  else
    files=$(grep -rl 'qa-fixtures\|decoy-frontend\|decoy-legacy\|decoy-worker' "$worktree" 2>/dev/null || true)
  fi
  for f in $files; do
    [[ -f "$f" ]] || continue
    sed_inplace -e "s|qa-fixtures|$LIB_NAME|g" -e 's|decoy-frontend|legacy/frontend-services|g' -e 's|decoy-legacy|legacy/scripts|g' -e 's|decoy-worker|legacy/worker-prototype|g' "$f"
  done
  cp "$ROOT/scripts/README.agent.md" "$worktree/README.md"
  mkdir -p "$worktree/prompts"
  for p in "$ROOT/prompts"/*.md; do
    [[ -f "$p" ]] || continue
    sed -e "s|qa-fixtures|$LIB_NAME|g" -e 's|decoy-frontend|legacy/frontend-services|g' -e 's|decoy-legacy|legacy/scripts|g' -e 's|decoy-worker|legacy/worker-prototype|g' "$p" > "$worktree/prompts/$(basename "$p")"
  done
  if [[ -f "$worktree/Makefile" ]]; then
    sed_inplace '/^scenario:/d' "$worktree/Makefile"
    sed_inplace '/^blind-repo:/d' "$worktree/Makefile"
    sed_inplace 's/qa-fixtures/lib/g' "$worktree/Makefile"
    sed_inplace 's/ blind-repo//g' "$worktree/Makefile"
  fi
  if [[ -f "$worktree/scripts/run-fixture-tests.sh" ]]; then
    sed_inplace "s|qa-fixtures|$LIB_NAME|g" "$worktree/scripts/run-fixture-tests.sh"
    sed_inplace '/expected until fixed/d' "$worktree/scripts/run-fixture-tests.sh"
  fi
  [[ -f "$worktree/docker-compose.yml" ]] && sed_inplace "s|qa-fixtures|$LIB_NAME|g" "$worktree/docker-compose.yml"
  rm -f "$worktree/.github/workflows/agent-scenario-smoke.yml"
}

export_branch() {
  local source_branch="$1"
  local worktree
  worktree=$(mktemp -d)
  git rev-parse --verify "$source_branch" >/dev/null 2>&1 || { echo "Missing branch: $source_branch" >&2; exit 1; }
  echo "==> Exporting $source_branch" >&2
  git archive "$source_branch" | tar -x -C "$worktree"
  process_worktree "$worktree" >&2
  echo "$worktree"
}

commit_branch() {
  local output="$1" blind_branch="$2" source_branch="$3" worktree="$4"
  git -C "$output" checkout -B "$blind_branch"
  find "$output" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
  cp -R "$worktree/." "$output/"
  git -C "$output" add -A
  git -C "$output" commit -m "Blind mirror: $source_branch -> $blind_branch"
  rm -rf "$worktree"
}

if $ALL_BRANCHES; then
  mkdir -p "$(dirname "$OUTPUT")"
  rm -rf "$OUTPUT" && mkdir -p "$OUTPUT"
  git -C "$OUTPUT" init -b main
  PAIRS=(
    "main:main"
    "scenario/01-jwt-expiry:fix/session-timeout"
    "scenario/03-viewer-role:fix/viewer-permissions"
    "scenario/10-cli-export:feature/task-export-cli"
    "qa/viewer-worker-skip:qa/viewer-worker-skip"
    "qa/analytics-copy-fix:qa/analytics-copy-fix"
  )
  echo "==> Building full blind mirror"
  for pair in "${PAIRS[@]}"; do
    source_branch="${pair%%:*}"
    blind_branch="${pair##*:}"
    worktree=$(export_branch "$source_branch")
    commit_branch "$OUTPUT" "$blind_branch" "$source_branch" "$worktree"
    echo "    $source_branch -> $blind_branch"
  done
  git -C "$OUTPUT" checkout main
  echo ""; echo "Full blind mirror ready: $OUTPUT"; git -C "$OUTPUT" branch
  echo ""; echo "Push: git -C $OUTPUT push -u origin --all"
  exit 0
fi

worktree=$(export_branch "$SOURCE_BRANCH")
mkdir -p "$(dirname "$OUTPUT")"
rm -rf "$OUTPUT" && mkdir -p "$OUTPUT"
cp -R "$worktree/." "$OUTPUT/" && rm -rf "$worktree"
if [[ ! -d "$OUTPUT/.git" ]]; then
  git -C "$OUTPUT" init -b main
  git -C "$OUTPUT" add -A
  git -C "$OUTPUT" commit -m "Blind repo generated from meridian ($SOURCE_BRANCH)"
else
  git -C "$OUTPUT" add -A
  git -C "$OUTPUT" commit -m "Regenerate blind repo from meridian ($SOURCE_BRANCH)" || true
fi
[[ -n "$BLIND_BRANCH" && "$BLIND_BRANCH" != "main" ]] && git -C "$OUTPUT" checkout -B "$BLIND_BRANCH"
echo "Blind repo ready: $OUTPUT (from $SOURCE_BRANCH)"
