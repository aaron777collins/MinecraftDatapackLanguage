#! /bin/bash
set -euo pipefail

# MDL Development Cycle Script

echo "UPDATE MDL - Git Upload, Release, Wait, Upgrade"

# Git Upload
echo "Git Upload..."
git add .
git commit -m "MDL Development Cycle" || true

echo "Pull & Rebase..."
git pull --rebase

git push

# Release
echo "Release..."
./scripts/release.sh patch "MDL Development Cycle"

# Wait for PyPI to propagate
echo "Wait..."
sleep 20

# Upgrade
echo "Upgrade..."
pipx upgrade minecraft-datapack-language || true
pipx upgrade minecraft-datapack-language || true