#!/bin/bash

# Test Development Setup Script for MDL
# This script tests that the development environment is working correctly

set -e

echo "🧪 Testing MDL Development Environment..."

# Test if mdlbeta command exists
if ! command -v mdlbeta &> /dev/null; then
    echo "❌ Error: mdlbeta command not found. Please run dev_setup.sh first."
    exit 1
fi

echo "✅ mdlbeta command found"

# Test version command
echo "📋 Testing version command..."
mdlbeta --version

# Test help command
echo "📋 Testing help command..."
mdlbeta --help > /dev/null

# Test if we can create a simple test project
echo "📋 Testing project creation..."
TEST_DIR="test_dev_project"
if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
fi

mdlbeta new "$TEST_DIR" --name "Test Project" --pack-format 82

# Test if the project was created
if [ -f "$TEST_DIR/test_project.mdl" ]; then
    echo "✅ Project creation test passed"
else
    echo "❌ Project creation test failed"
    exit 1
fi

# Test if we can check the syntax
echo "📋 Testing syntax check..."
mdlbeta check "$TEST_DIR/test_project.mdl"

# Test if we can build the project
echo "📋 Testing build..."
mdlbeta build --mdl "$TEST_DIR/test_project.mdl" -o "$TEST_DIR/dist"

# Test if the build output exists (support both current and legacy zip locations)
if [ -f "$TEST_DIR/dist.zip" ]; then
    echo "✅ Build test passed (found dist.zip)"
elif [ -f "$TEST_DIR/dist/mdl.zip" ]; then
    echo "✅ Build test passed (found dist/mdl.zip)"
else
    echo "❌ Build test failed (no zip found)"
    echo "Checked: $TEST_DIR/dist.zip and $TEST_DIR/dist/mdl.zip"
    exit 1
fi

# Clean up
echo "🧹 Cleaning up test files..."
rm -rf "$TEST_DIR"

echo ""
echo "🎉 All development tests passed!"
echo ""
echo "Your development environment is working correctly."
echo "You can now use 'mdlbeta' for development and 'mdl' for the stable version."
