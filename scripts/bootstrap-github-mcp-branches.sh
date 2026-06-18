#!/bin/bash
# Ensure PR head branches exist on a GitHub repo (for MCP fixtures).
# Usage: ./scripts/bootstrap-github-mcp-branches.sh --repo OWNER/NAME
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="${ROOT}/fixtures/github-mcp/manifest.json"
REPO=""
TEMPLATE_REPO="${MCP_TEMPLATE_REPO:-jeremymyslowski/meridian-blind-public-0618}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 --repo OWNER/NAME"
      echo "Env: MCP_TEMPLATE_REPO (default: ${TEMPLATE_REPO})"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$REPO" ]] || { echo "Missing --repo OWNER/NAME" >&2; exit 1; }
[[ -f "$MANIFEST" ]] || { echo "Missing manifest: $MANIFEST" >&2; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "gh CLI is required" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq is required" >&2; exit 1; }

encode_head_ref() {
  printf 'heads/%s' "${1//\//%2F}"
}

branch_exists() {
  gh api "repos/${REPO}/git/ref/$(encode_head_ref "$1")" >/dev/null 2>&1
}

ref_sha() {
  local source_repo="$1" branch="$2"
  gh api "repos/${source_repo}/git/ref/$(encode_head_ref "$branch")" --jq .object.sha
}

copy_branch_ref() {
  local branch="$1" source_repo="$2"
  local sha
  sha=$(ref_sha "$source_repo" "$branch")
  gh api -X POST "repos/${REPO}/git/refs" \
    -f ref="refs/heads/${branch}" \
    -f sha="$sha" >/dev/null
}

push_branch_from_local() {
  local branch="$1"
  local tmp
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' RETURN

  gh repo clone "$REPO" "$tmp/repo" -- --depth=1 --branch main
  cd "$tmp/repo"
  git remote add src "file://${ROOT}"
  git fetch src "${branch}:${branch}"
  git push origin "${branch}"
}

ensure_branch() {
  local branch="$1"

  if branch_exists "$branch"; then
    echo "  branch exists: ${branch}"
    return 0
  fi

  echo "  creating branch: ${branch}"

  local parent=""
  parent=$(gh api "repos/${REPO}" --jq '.parent.full_name // empty' 2>/dev/null || true)

  if [[ -n "$parent" ]] && ref_sha "$parent" "$branch" >/dev/null 2>&1; then
    copy_branch_ref "$branch" "$parent"
    echo "    copied from parent ${parent}"
    return 0
  fi

  if ref_sha "$TEMPLATE_REPO" "$branch" >/dev/null 2>&1; then
    copy_branch_ref "$branch" "$TEMPLATE_REPO"
    echo "    copied from template ${TEMPLATE_REPO}"
    return 0
  fi

  if git -C "$ROOT" show-ref --verify --quiet "refs/heads/${branch}"; then
    push_branch_from_local "$branch"
    echo "    pushed from local ${ROOT}"
    return 0
  fi

  echo "Cannot find source for branch ${branch}" >&2
  exit 1
}

echo "==> Bootstrapping MCP branches on ${REPO}"
while IFS= read -r branch; do
  [[ -n "$branch" ]] && ensure_branch "$branch"
done < <(jq -r '.pull_requests[].head' "$MANIFEST" | sort -u)
echo "==> Done"