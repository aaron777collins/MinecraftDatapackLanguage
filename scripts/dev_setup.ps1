# Development Setup Script for MDL (PowerShell)
# This script sets up a local development environment with mdlbeta command

param(
    [switch]$Force
)

Write-Host "🔧 Setting up MDL Development Environment..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Error: pyproject.toml not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found. Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: pip not found. Please install pip first." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing development dependencies..." -ForegroundColor Yellow

# Install in development mode with the mdlbeta entry point
Write-Host "Installing local version as 'mdlbeta'..." -ForegroundColor Yellow
if ($Force) {
    pip install -e . --force-reinstall
} else {
    pip install -e .
}

# Verify installation
try {
    $mdlbetaVersion = mdlbeta --version 2>&1
    Write-Host "✅ mdlbeta command installed successfully!" -ForegroundColor Green
    Write-Host "📋 Version info: $mdlbetaVersion" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Development setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  mdlbeta --help          # Show help" -ForegroundColor White
    Write-Host "  mdlbeta --version       # Show version" -ForegroundColor White
    Write-Host "  mdlbeta build --mdl file.mdl -o dist  # Build a datapack" -ForegroundColor White
    Write-Host "  mdlbeta check file.mdl  # Check syntax" -ForegroundColor White
    Write-Host "  mdlbeta new project     # Create new project" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: 'mdl' command remains unchanged (global installation)" -ForegroundColor Cyan
    Write-Host "      'mdlbeta' command uses your local development version" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error: mdlbeta command not found after installation" -ForegroundColor Red
    exit 1
}
