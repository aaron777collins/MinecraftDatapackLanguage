#!/bin/bash

# Development Setup Script for MDL
# This script sets up a local development environment with mdlbeta command

set -e

echo "🔧 Setting up MDL Development Environment..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found. Please install Python 3.9+ first."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip not found. Please install pip first."
    exit 1
fi

echo "📦 Installing development dependencies..."

# Install in development mode with the mdlbeta entry point
echo "Installing local version as 'mdlbeta'..."
pip install -e . --force-reinstall

# Verify installation
if command -v mdlbeta &> /dev/null; then
    echo "✅ mdlbeta command installed successfully!"
    echo "📋 Version info:"
    mdlbeta --version
    echo ""
    echo "🎉 Development setup complete!"
    echo ""
    echo "Usage:"
    echo "  mdlbeta --help          # Show help"
    echo "  mdlbeta --version       # Show version"
    echo "  mdlbeta build --mdl file.mdl -o dist  # Build a datapack"
    echo "  mdlbeta check file.mdl  # Check syntax"
    echo "  mdlbeta new project     # Create new project"
    echo ""
    echo "Note: 'mdl' command remains unchanged (global installation)"
    echo "      'mdlbeta' command uses your local development version"
else
    echo "❌ Error: mdlbeta command not found after installation"
    exit 1
fi
