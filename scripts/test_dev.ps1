# Test Development Setup Script for MDL (PowerShell)
# This script tests that the development environment is working correctly

Write-Host "🧪 Testing MDL Development Environment..." -ForegroundColor Green

# Test if mdlbeta command exists
try {
    $null = Get-Command mdlbeta -ErrorAction Stop
    Write-Host "✅ mdlbeta command found" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: mdlbeta command not found. Please run dev_setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Test version command
Write-Host "📋 Testing version command..." -ForegroundColor Yellow
try {
    $version = mdlbeta --version 2>&1
    Write-Host "Version: $version" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Version command failed" -ForegroundColor Red
    exit 1
}

# Test help command
Write-Host "📋 Testing help command..." -ForegroundColor Yellow
try {
    $null = mdlbeta --help 2>&1
    Write-Host "✅ Help command works" -ForegroundColor Green
} catch {
    Write-Host "❌ Help command failed" -ForegroundColor Red
    exit 1
}

# Test if we can create a simple test project
Write-Host "📋 Testing project creation..." -ForegroundColor Yellow
$TEST_DIR = "test_dev_project"
if (Test-Path $TEST_DIR) {
    Remove-Item -Recurse -Force $TEST_DIR
}

try {
    mdlbeta new $TEST_DIR --name "Test Project" --pack-format 82
    Write-Host "✅ Project creation command executed" -ForegroundColor Green
} catch {
    Write-Host "❌ Project creation failed" -ForegroundColor Red
    exit 1
}

# Test if the project was created
if (Test-Path "$TEST_DIR/test_project.mdl") {
    Write-Host "✅ Project creation test passed" -ForegroundColor Green
} else {
    Write-Host "❌ Project creation test failed" -ForegroundColor Red
    exit 1
}

# Test if we can check the syntax
Write-Host "📋 Testing syntax check..." -ForegroundColor Yellow
try {
    mdlbeta check "$TEST_DIR/test_project.mdl"
    Write-Host "✅ Syntax check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Syntax check failed" -ForegroundColor Red
    exit 1
}

# Test if we can build the project
Write-Host "📋 Testing build..." -ForegroundColor Yellow
try {
    mdlbeta build --mdl "$TEST_DIR/test_project.mdl" -o "$TEST_DIR/dist"
    Write-Host "✅ Build command executed" -ForegroundColor Green
} catch {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

# Test if the build output exists
if (Test-Path "$TEST_DIR/dist/mdl.zip") {
    Write-Host "✅ Build test passed" -ForegroundColor Green
} else {
    Write-Host "❌ Build test failed" -ForegroundColor Red
    exit 1
}

# Clean up
Write-Host "🧹 Cleaning up test files..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $TEST_DIR

Write-Host ""
Write-Host "🎉 All development tests passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your development environment is working correctly." -ForegroundColor Cyan
Write-Host "You can now use 'mdlbeta' for development and 'mdl' for the stable version." -ForegroundColor Cyan
