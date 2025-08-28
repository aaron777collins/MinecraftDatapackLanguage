#!/bin/bash

# Development Build Script for MDL
# This script builds the current development version for testing

set -e

echo "🔨 Building MDL Development Version..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "📦 Building package..."
python -m build

# Check if build was successful
if [ ! "$(ls -A dist/ 2>/dev/null)" ]; then
    echo "❌ Error: Build failed - no package files found in dist/"
    exit 1
fi

# Get the built wheel file (if exists)
WHEEL_FILE=$(ls dist/minecraft_datapack_language-*.whl 2>/dev/null | head -1)
if [ -z "$WHEEL_FILE" ]; then
    echo "✅ Build successful (source distribution only)"
else
    echo "✅ Build successful: $WHEEL_FILE"
fi

# Install the development version
echo "📥 Installing development version as 'mdlbeta'..."
pip install -e . --force-reinstall

# Test the installation
if command -v mdlbeta &> /dev/null; then
    echo "✅ mdlbeta command available!"
    echo "📋 Version info:"
    mdlbeta --version
    echo ""
    echo "🎉 Development build complete!"
    echo ""
    echo "You can now use:"
    echo "  mdlbeta --help          # Show help"
    echo "  mdlbeta build --mdl file.mdl -o dist  # Build a datapack"
    echo "  mdlbeta check file.mdl  # Check syntax"
    echo ""
    echo "The global 'mdl' command remains unchanged."
else
    echo "❌ Error: mdlbeta command not found after installation"
    exit 1
fi
