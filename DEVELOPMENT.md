# MDL Development Guide

This guide explains how to set up and use the MDL development environment.

## Overview

The development system provides two separate commands:
- `mdl` - The stable, globally installed version
- `mdlbeta` - Your local development version for testing changes

## Quick Start

### 1. Initial Setup

**Linux/macOS:**
```bash
./scripts/dev_setup.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\dev_setup.ps1
```

This will install your local development version as `mdlbeta`.

### 2. Test Your Setup

**Linux/macOS:**
```bash
./scripts/test_dev.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\test_dev.ps1
```

### 3. Development Workflow

1. **Make changes** to the code
2. **Rebuild** the development version:
   ```bash
   ./scripts/dev_build.sh
   ```
3. **Test** your changes with `mdlbeta`:
   ```bash
   mdlbeta build --mdl your_file.mdl -o dist
   ```
4. **Compare** with stable version:
   ```bash
   mdl build --mdl your_file.mdl -o dist_stable
   ```

## Commands

### Development Commands (`mdlbeta`)

```bash
mdlbeta --version       # Show development version
mdlbeta --help          # Show help
mdlbeta new project     # Create new project
mdlbeta build --mdl file.mdl -o dist  # Build datapack
mdlbeta check file.mdl  # Check syntax
```

### Stable Commands (`mdl`)

```bash
mdl --version       # Show stable version
mdl --help          # Show help
mdl new project     # Create new project
mdl build --mdl file.mdl -o dist  # Build datapack
mdl check file.mdl  # Check syntax
```

## Scripts

### Setup Scripts

- `scripts/dev_setup.sh` / `scripts/dev_setup.ps1` - Initial development setup
- `scripts/dev_build.sh` / `scripts/dev_build.ps1` - Build and install development version
- `scripts/test_dev.sh` / `scripts/test_dev.ps1` - Test development environment

### Build Scripts

- `scripts/dev_build.sh` - Clean build and install development version
- `scripts/dev_build.ps1` - PowerShell version of build script

### Test Scripts

- `scripts/test_dev.sh` - Comprehensive test of development environment
- `scripts/test_dev.ps1` - PowerShell version of test script

## Development Workflow

### 1. Making Changes

1. Edit the source code in `minecraft_datapack_language/`
2. Test your changes with `mdlbeta`
3. Compare with the stable `mdl` version

### 2. Testing Changes

```bash
# Test with development version
mdlbeta build --mdl test_examples/hello_world.mdl -o test_output_beta

# Compare with stable version
mdl build --mdl test_examples/hello_world.mdl -o test_output_stable

# Compare outputs
diff -r test_output_beta test_output_stable
```

### 3. Rebuilding After Changes

```bash
# Quick rebuild
./scripts/dev_build.sh

# Or force clean rebuild
./scripts/dev_build.sh --clean
```

## Troubleshooting

### mdlbeta Command Not Found

```bash
# Reinstall development version
pip install -e . --force-reinstall
```

### Build Errors

```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info/
./scripts/dev_build.sh
```

### Version Conflicts

If you have issues with version conflicts:

```bash
# Uninstall and reinstall
pip uninstall minecraft-datapack-language -y
pip install -e .
```

## File Structure

```
MinecraftDatapackLanguage/
├── minecraft_datapack_language/    # Main package
│   ├── cli.py                      # CLI interface
│   ├── mdl_parser_js.py            # JavaScript-style parser
│   ├── mdl_lexer_js.py             # JavaScript-style lexer
│   ├── expression_processor.py     # Expression processing
│   ├── pack.py                     # Pack building
│   └── utils.py                    # Utilities
├── scripts/                        # Development scripts
│   ├── dev_setup.sh               # Setup script (Linux/macOS)
│   ├── dev_setup.ps1              # Setup script (Windows)
│   ├── dev_build.sh               # Build script (Linux/macOS)
│   ├── dev_build.ps1              # Build script (Windows)
│   ├── test_dev.sh                # Test script (Linux/macOS)
│   └── test_dev.ps1               # Test script (Windows)
├── test_examples/                  # Test files
└── pyproject.toml                  # Package configuration
```

## Best Practices

1. **Always test with `mdlbeta`** before committing changes
2. **Compare outputs** between `mdl` and `mdlbeta` to ensure compatibility
3. **Use the test scripts** to verify your development environment
4. **Keep the stable `mdl`** installation for comparison
5. **Rebuild after changes** to ensure your changes are active

## Release Process

When ready to release:

1. Test thoroughly with `mdlbeta`
2. Update version in `pyproject.toml`
3. Run the release script: `./scripts/release.sh patch`
4. The new version will be available as `mdl` after installation

## Support

If you encounter issues:

1. Check that both `mdl` and `mdlbeta` commands are available
2. Run the test scripts to verify your setup
3. Check the troubleshooting section above
4. Reinstall the development version if needed
