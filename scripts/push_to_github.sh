#!/usr/bin/env bash
# Push current branch to GitHub. Run from repo root.
# One-time: set up credentials (see docs/SETUP_GITHUB_PUSH.md) so push works without prompts.

set -e
cd "$(dirname "$0")/.."

if ! git remote get-url origin &>/dev/null; then
  echo "No remote 'origin' set. Example:"
  echo "  git remote add origin https://github.com/YOUR_USERNAME/dqm-framework.git"
  exit 1
fi

echo "Pushing to origin $(git branch --show-current)..."
git push -u origin "$(git branch --show-current)"
