#!/usr/bin/env bash
# release.sh — bump version in pyproject.toml, build, tag, push, and publish a GitHub Release with assets.
# Usage:
#   ./scripts/release.sh v0.2.0 "Notes..."         # set exact version
#   ./scripts/release.sh patch "Notes..."          # auto-bump patch
#   ./scripts/release.sh minor "Notes..."          # auto-bump minor
#   ./scripts/release.sh major "Notes..."          # auto-bump major
#
# Requires: git, python, build (python -m pip install build), and GitHub CLI `gh` authenticated (gh auth login).

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <vX.Y.Z|major|minor|patch> [notes]"
  exit 1
fi

BUMP="$1"                    # vX.Y.Z or bump keyword
NOTES="${2:-}"

PYPROJECT="pyproject.toml"

# Extract current version (simple TOML parse)
CURR=$(grep -E '^[[:space:]]*version[[:space:]]*=' "$PYPROJECT" | head -n1 | sed -E 's/.*"([^"]+)".*/\1/')
if [ -z "$CURR" ]; then
  echo "Could not find current version in $PYPROJECT"
  exit 1
fi

function bump() {
  local ver="$1" part="$2"
  IFS='.' read -r MAJ MIN PAT <<<"$ver"
  case "$part" in
    major) MAJ=$((MAJ+1)); MIN=0; PAT=0;;
    minor) MIN=$((MIN+1)); PAT=0;;
    patch) PAT=$((PAT+1));;
    *) echo "Unknown bump part: $part"; exit 1;;
  esac
  echo "${MAJ}.${MIN}.${PAT}"
}

if [[ "$BUMP" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  NEW=${BUMP#v}
elif [[ "$BUMP" =~ ^(major|minor|patch)$ ]]; then
  NEW=$(bump "$CURR" "$BUMP")
else
  echo "First arg must be vX.Y.Z or one of: major, minor, patch"
  exit 1
fi

TAG="v${NEW}"

# Ensure clean working tree
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: Working tree not clean. Commit or stash changes first."
  exit 1
fi

# Update pyproject.toml version
echo "Updating version: $CURR -> $NEW"
# Replace only the first match for version = "x.y.z"
tmpfile="$(mktemp)"
awk -v new="$NEW" '
  found==0 && $0 ~ /^[[:space:]]*version[[:space:]]*=/ {
    sub(/"[^"]+"/, "\"" new "\"")
    found=1
  }
  { print }
' "$PYPROJECT" > "$tmpfile"
mv "$tmpfile" "$PYPROJECT"

# Commit version bump
git add "$PYPROJECT"
git commit -m "chore(release): $TAG"

# Build artifacts
python -m pip install --upgrade pip >/dev/null
python -m pip install build >/dev/null
python -m build

# Create annotated tag & push
git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"
git push

# Create (or update) GitHub Release with assets
if ! command -v gh >/dev/null 2>&1; then
  echo "Warning: GitHub CLI 'gh' not found. Tag was pushed; GitHub Actions release workflow will publish."
  exit 0
fi

if gh release view "$TAG" >/dev/null 2>&1; then
  echo "Release $TAG exists — uploading assets..."
  gh release upload "$TAG" dist/* --clobber
else
  if [ -z "$NOTES" ]; then NOTES="Automated release $TAG"; fi
  gh release create "$TAG" dist/* --notes "$NOTES"
fi

echo "✅ Released $TAG"
