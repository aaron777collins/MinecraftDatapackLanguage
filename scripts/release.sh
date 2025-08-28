#!/usr/bin/env bash
# release.sh — tag-driven release (setuptools-scm). No editing pyproject.toml.
# Usage:
#   ./scripts/release.sh v1.2.3 "Notes..."
#   ./scripts/release.sh patch   "Notes..."
#   ./scripts/release.sh minor   "Notes..."
#   ./scripts/release.sh major   "Notes..."

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <vX.Y.Z|major|minor|patch> [notes]"
  exit 1
fi

BUMP="$1"
NOTES="${2:-}"

# Ensure clean working tree
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: working tree not clean. Commit or stash changes first."
  exit 1
fi

# Find latest semver tag (vX.Y.Z). If none, start at v0.0.0
LATEST_TAG=$(git tag --list 'v[0-9]*.[0-9]*.[0-9]*' | sort -V | tail -n1 || true)
[ -z "$LATEST_TAG" ] && LATEST_TAG="v0.0.0"

parse_semver () {
  local v="${1#v}"
  IFS='.' read -r MAJ MIN PAT <<<"$v"
  echo "$MAJ" "$MIN" "$PAT"
}

bump_part () {
  local part="$1" MAJ="$2" MIN="$3" PAT="$4"
  case "$part" in
    major) MAJ=$((MAJ+1)); MIN=0; PAT=0;;
    minor) MIN=$((MIN+1)); PAT=0;;
    patch) PAT=$((PAT+1));;
    *) echo "Unknown bump: $part"; exit 1;;
  esac
  echo "v${MAJ}.${MIN}.${PAT}"
}

if [[ "$BUMP" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  NEW_TAG="$BUMP"
elif [[ "$BUMP" =~ ^(major|minor|patch)$ ]]; then
  read -r MAJ MIN PAT < <(parse_semver "$LATEST_TAG")
  NEW_TAG=$(bump_part "$BUMP" "$MAJ" "$MIN" "$PAT")
else
  echo "First arg must be vX.Y.Z or one of: major, minor, patch"
  exit 1
fi

echo "Latest tag: ${LATEST_TAG:-<none>}"
echo "New tag:    $NEW_TAG"

# Create annotated tag and push
git tag -a "$NEW_TAG" -m "Release $NEW_TAG"
git push origin "$NEW_TAG"
git push || true

# [CLEAN] Clean old local artifacts so we never upload stale files
rm -rf dist

# OPTIONAL local build (handy if you want to attach artifacts right now)
if command -v python >/dev/null 2>&1; then
  python -m pip install --upgrade pip >/dev/null 2>&1 || true
  python -m pip install build >/dev/null 2>&1 || true
  python -m build || true
fi

# Create GitHub Release and attach any local dist/* (CI will also attach its own)
if command -v gh >/dev/null 2>&1; then
  if gh release view "$NEW_TAG" >/dev/null 2>&1; then
    echo "GitHub Release $NEW_TAG exists — uploading local assets (if any)..."
    if ls dist/* >/dev/null 2>&1; then gh release upload "$NEW_TAG" dist/* --clobber; fi
  else
    [ -z "$NOTES" ] && NOTES="Automated release $NEW_TAG"
    if ls dist/* >/dev/null 2>&1; then
      gh release create "$NEW_TAG" dist/* --notes "$NOTES"
    else
      gh release create "$NEW_TAG" --notes "$NOTES"
    fi
  fi
else
  echo "Note: 'gh' not installed — tag pushed. CI will create the GitHub Release."
fi

echo "[+] Tagged and released $NEW_TAG"
