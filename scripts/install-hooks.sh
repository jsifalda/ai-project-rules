#!/usr/bin/env bash
# Activate the repo's tracked git hooks (.githooks/) for this clone.
# Idempotent. Uses only git config — no dependencies installed.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

git config core.hooksPath .githooks
echo "hooks installed: core.hooksPath=.githooks"
echo "pre-commit will now run scripts/check-universality.sh on staged files."
echo
echo "next step: create your local denylist"
echo "  cp scripts/universality-denylist.txt.example scripts/universality-denylist.txt"
echo "  # then edit it to include your name, employer, etc."
