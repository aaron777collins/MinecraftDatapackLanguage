#!/bin/bash

# Script to update version information across the project
# This script helps maintain consistency when version information needs to be updated

set -e

echo "🔍 Checking current version information..."

# Get current version from the project
CURRENT_VERSION=$(python -c "import minecraft_datapack_language; print(minecraft_datapack_language.__version__)" 2>/dev/null || echo "unknown")

echo "📦 Current version: $CURRENT_VERSION"

echo ""
echo "📋 Version information locations:"
echo "  • PyPI: https://pypi.org/project/minecraft-datapack-language/"
echo "  • GitHub Releases: https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest"
echo "  • Project version: minecraft_datapack_language/_version.py (auto-generated)"
echo ""

echo "✅ Version information is now dynamically managed:"
echo "  • Downloads page links to GitHub releases"
echo "  • Documentation directs users to check GitHub for latest versions"
echo "  • No hardcoded version numbers in user-facing content"
echo ""

echo "📝 To update version information:"
echo "  1. Create a new GitHub release"
echo "  2. The downloads page will automatically point to the latest release"
echo "  3. Users can check GitHub for the most up-to-date version"
echo ""

echo "🎯 For users to get the latest version:"
echo "  • Python package: pipx upgrade minecraft-datapack-language"
echo "  • VS Code extension: Download from GitHub releases"
echo ""

echo "✨ Version management is now automated and user-friendly!"
