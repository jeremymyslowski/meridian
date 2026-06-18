#!/bin/bash
# Seed GitHub issues, PRs, labels, and tags for MCP connector QA.
# Usage: ./scripts/seed-github-mcp-fixtures.sh --repo OWNER/NAME [--force] [--dry-run]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="${ROOT}/fixtures/github-mcp/manifest.json"
REPO=""
FORCE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --force) FORCE=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: $0 --repo OWNER/NAME [--force] [--dry-run]"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$REPO" ]] || { echo "Missing --repo OWNER/NAME" >&2; exit 1; }
[[ -f "$MANIFEST" ]] || { echo "Missing manifest: $MANIFEST" >&2; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "gh CLI is required" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq is required" >&2; exit 1; }

MARKER_TITLE=$(jq -r '.marker_title' "$MANIFEST")

encode_head_ref() {
  printf 'heads/%s' "${1//\//%2F}"
}

run() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

api() {
  if $DRY_RUN; then
    echo "[dry-run] gh api $*"
  else
    gh api "$@"
  fi
}

marker_exists() {
  gh issue list -R "$REPO" --state all --search "$MARKER_TITLE in:title" --json title --jq '.[].title' 2>/dev/null | grep -qx "$MARKER_TITLE"
}

close_fixture_items() {
  echo "==> Closing existing mcp-fixture items (--force)"
  if $DRY_RUN; then
    echo "[dry-run] would close labeled issues and PRs"
    return 0
  fi

  local issues prs
  issues=$(gh issue list -R "$REPO" --state open --label mcp-fixture --json number --jq '.[].number' 2>/dev/null || true)
  for n in $issues; do
    gh issue close "$n" -R "$REPO" --comment "Reset for MCP fixture re-seed" || true
  done

  prs=$(gh pr list -R "$REPO" --state open --json number,headRefName --jq '.[] | select(.headRefName != null) | .number' 2>/dev/null || true)
  for n in $prs; do
    gh pr close "$n" -R "$REPO" --delete-branch=false || true
  done
}

create_labels() {
  echo "==> Creating labels"
  local count
  count=$(jq '.labels | length' "$MANIFEST")
  for i in $(seq 0 $((count - 1))); do
    local name color desc
    name=$(jq -r ".labels[$i].name" "$MANIFEST")
    color=$(jq -r ".labels[$i].color" "$MANIFEST")
    desc=$(jq -r ".labels[$i].description" "$MANIFEST")
    if $DRY_RUN; then
      echo "[dry-run] label: $name"
      continue
    fi
    if gh label list -R "$REPO" --json name --jq '.[].name' | grep -qx "$name"; then
      echo "  label exists: $name"
    else
      gh label create "$name" -R "$REPO" --color "$color" --description "$desc" || true
      echo "  created label: $name"
    fi
  done
}

create_pull_request_at_index() {
  local i="$1" draft_only="$2"
  local title head base draft body draft_flag
  title=$(jq -r ".pull_requests[$i].title" "$MANIFEST")
  head=$(jq -r ".pull_requests[$i].head" "$MANIFEST")
  base=$(jq -r ".pull_requests[$i].base" "$MANIFEST")
  draft=$(jq -r ".pull_requests[$i].draft" "$MANIFEST")
  body=$(jq -r ".pull_requests[$i].body" "$MANIFEST")

  if [[ "$draft_only" == "true" && "$draft" != "true" ]] || \
     [[ "$draft_only" == "false" && "$draft" == "true" ]]; then
    return 0
  fi

  if $DRY_RUN; then
    echo "[dry-run] pr: $title ($head -> $base, draft=$draft)"
    return 0
  fi

  if ! gh api "repos/${REPO}/git/ref/$(encode_head_ref "$head")" >/dev/null 2>&1; then
    echo "  missing head branch: ${head} — run bootstrap-github-mcp-branches.sh" >&2
    exit 1
  fi

  draft_flag=""
  [[ "$draft" == "true" ]] && draft_flag="--draft"

  # shellcheck disable=SC2086
  gh pr create -R "$REPO" --title "$title" --head "$head" --base "$base" --body "$body" $draft_flag
  echo "  created PR: $title"
}

create_pull_requests() {
  echo "==> Creating open pull requests (order matters for numbering)"
  local count
  count=$(jq '.pull_requests | length' "$MANIFEST")
  for i in $(seq 0 $((count - 1))); do
    create_pull_request_at_index "$i" false
  done
}

create_draft_pull_requests() {
  echo "==> Creating draft pull requests"
  local count
  count=$(jq '.pull_requests | length' "$MANIFEST")
  for i in $(seq 0 $((count - 1))); do
    create_pull_request_at_index "$i" true
  done
}

create_issues() {
  echo "==> Creating issues"
  local count
  count=$(jq '.issues | length' "$MANIFEST")
  for i in $(seq 0 $((count - 1))); do
    local title body labels_arg
    title=$(jq -r ".issues[$i].title" "$MANIFEST")
    body=$(jq -r ".issues[$i].body" "$MANIFEST")
    labels_arg=$(jq -r ".issues[$i].labels | join(\",\")" "$MANIFEST")

    if $DRY_RUN; then
      echo "[dry-run] issue: $title [$labels_arg]"
      continue
    fi

    gh issue create -R "$REPO" --title "$title" --body "$body" --label "$labels_arg"
    echo "  created issue: $title"
  done
}

create_marker() {
  echo "==> Creating seed marker"
  if $DRY_RUN; then
    echo "[dry-run] marker issue: $MARKER_TITLE (closed)"
    return 0
  fi
  local url num
  url=$(gh issue create -R "$REPO" --title "$MARKER_TITLE" --body "Automated MCP fixture seed marker." --label mcp-fixture)
  num="${url##*/}"
  gh issue close "$num" -R "$REPO" --comment "Seed complete."
}

push_tags() {
  echo "==> Pushing git tags"
  local count
  count=$(jq '.tags | length' "$MANIFEST")
  for i in $(seq 0 $((count - 1))); do
    local name message ref
    name=$(jq -r ".tags[$i].name" "$MANIFEST")
    message=$(jq -r ".tags[$i].message" "$MANIFEST")
    ref=$(jq -r ".tags[$i].ref" "$MANIFEST")

    if $DRY_RUN; then
      echo "[dry-run] tag: $name on $ref"
      continue
    fi

    if gh api "repos/${REPO}/git/refs/tags/${name}" >/dev/null 2>&1; then
      echo "  tag exists: $name"
      continue
    fi

    local sha tag_sha
    sha=$(gh api "repos/${REPO}/git/ref/$(encode_head_ref "$ref")" --jq .object.sha)
    tag_sha=$(gh api -X POST "repos/${REPO}/git/tags" \
      -f tag="$name" \
      -f message="$message" \
      -f object="$sha" \
      -f type=commit --jq .sha)
    gh api -X POST "repos/${REPO}/git/refs" \
      -f ref="refs/tags/${name}" \
      -f sha="$tag_sha" >/dev/null
    echo "  created tag: $name"
  done
}

echo "==> Seeding GitHub MCP fixtures on ${REPO}"

if ! $DRY_RUN; then
  gh repo view "$REPO" >/dev/null 2>&1 || { echo "Cannot access repo: $REPO" >&2; exit 1; }
fi

if marker_exists && ! $FORCE; then
  echo "Marker '${MARKER_TITLE}' found. Use --force to re-seed."
  exit 0
fi

$FORCE && close_fixture_items

run bash "${ROOT}/scripts/bootstrap-github-mcp-branches.sh" --repo "$REPO"
create_labels
create_pull_requests
create_issues
create_draft_pull_requests
push_tags
create_marker

echo ""
echo "==> Seed complete for ${REPO}"
jq -r '.expected_numbers | to_entries[] | "  \(.key): #\(.value)"' "$MANIFEST"
echo ""
echo "Verify: gh issue list -R ${REPO} && gh pr list -R ${REPO}"