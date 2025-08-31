#! /bin/bash

# MDL Development Cycle Script

set -e

echo "🔧 UPDATE MDL - Git Upload, Release, Wait, Upgrade"

# Git Upload
echo "🔧 Git Upload..."
git add .
git commit -m "MDL Development Cycle"
git push

# Release
echo "🔧 Release..."
./scripts/release.sh patch "MDL Development Cycle"

# Wait
echo "🔧 Wait..."
sleep 5

# Upgrade
echo "🔧 Upgrade..."
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language