# Development Build Script for MDL (PowerShell)
# This script builds the current development version for testing

param(
    [switch]$Clean
)

Write-Host "🔨 Building MDL Development Version..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Error: pyproject.toml not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

# Clean previous builds
if ($Clean -or (Test-Path "dist") -or (Test-Path "build") -or (Test-Path "*.egg-info")) {
    Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    Get-ChildItem -Name "*.egg-info" -Directory | ForEach-Object { Remove-Item -Recurse -Force $_ }
}

# Build the package
Write-Host "📦 Building package..." -ForegroundColor Yellow
python -m build

# Check if build was successful
$wheelFiles = Get-ChildItem "dist" -Name "minecraft_datapack_language-*.whl" -ErrorAction SilentlyContinue
if (-not $wheelFiles) {
    Write-Host "❌ Error: Build failed - no wheel file found in dist/" -ForegroundColor Red
    exit 1
}

# Get the built wheel file
$wheelFile = $wheelFiles[0]
Write-Host "✅ Build successful: $wheelFile" -ForegroundColor Green

# Install the development version
Write-Host "📥 Installing development version as 'mdlbeta'..." -ForegroundColor Yellow
pip install -e . --force-reinstall

# Test the installation
try {
    $mdlbetaVersion = mdlbeta --version 2>&1
    Write-Host "✅ mdlbeta command available!" -ForegroundColor Green
    Write-Host "📋 Version info: $mdlbetaVersion" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Development build complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use:" -ForegroundColor Yellow
    Write-Host "  mdlbeta --help          # Show help" -ForegroundColor White
    Write-Host "  mdlbeta build --mdl file.mdl -o dist  # Build a datapack" -ForegroundColor White
    Write-Host "  mdlbeta check file.mdl  # Check syntax" -ForegroundColor White
    Write-Host ""
    Write-Host "The global 'mdl' command remains unchanged." -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error: mdlbeta command not found after installation" -ForegroundColor Red
    exit 1
}
