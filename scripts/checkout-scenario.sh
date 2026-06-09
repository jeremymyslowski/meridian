#!/bin/bash
# Usage: ./scripts/checkout-scenario.sh 01
set -e

NUM="${1:?Usage: checkout-scenario.sh <01|03|10>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

case "$NUM" in
  01) BRANCH="scenario/01-jwt-expiry" ;;
  03) BRANCH="scenario/03-viewer-role" ;;
  10) BRANCH="scenario/10-cli-export" ;;
  *)
    echo "Unknown scenario: $NUM"
    echo "Fixture-only scenarios (04-09, 11-12) use main branch."
    exit 1
    ;;
esac

git checkout "$BRANCH"
echo "Checked out $BRANCH"
echo "See docs/agent-scenarios/${NUM}-*.md for the agent prompt."