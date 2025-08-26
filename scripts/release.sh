#!/usr/bin/env bash
# release.sh — cut a versioned release using GitHub CLI
# Usage:
#   ./scripts/release.sh v0.1.0 "Short release notes..."
# Requires: git, python, build (python -m pip install build), and GitHub CLI `gh` authenticated.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <version-tag> [notes]"
  exit 1
fi

VERSION="$1"           # e.g. v0.1.0
NOTES="${2:-}"

# Safety checks
if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI 'gh' is required. Install from https://cli.github.com/"
  exit 1
fi

# Ensure clean working tree
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: Working tree not clean. Commit or stash changes first."
  exit 1
fi

# Build artifacts
python -m pip install --upgrade pip >/dev/null
python -m pip install build >/dev/null
python -m build

# Create annotated tag if it doesn't exist
if git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "Tag $VERSION already exists, skipping tag creation."
else
  git tag -a "$VERSION" -m "Release $VERSION"
  git push origin "$VERSION"
fi

# Create GitHub Release (idempotent)
if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "GitHub release $VERSION exists. Uploading assets..."
else
  if [ -z "$NOTES" ]; then
    NOTES="Automated release $VERSION"
  fi
  gh release create "$VERSION" dist/* --notes "$NOTES"
fi

echo "✅ Released $VERSION"
