#! /bin/bash

# MDL Development Cycle Script

echo "🔧 UPDATE MDL - Git Upload, Release, Wait, Upgrade"

# Git Upload
echo "🔧 Git Upload..."
git add .
git commit -m "MDL Development Cycle"

echo "🔧 Pull & Rebase..."
git pull --rebase

git push

# Release
echo "🔧 Release..."
./scripts/release.sh patch "MDL Development Cycle"

# Wait
echo "🔧 Wait..."
sleep 15

# Upgrade
echo "🔧 Upgrade..."
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language
pipx upgrade minecraft-datapack-language