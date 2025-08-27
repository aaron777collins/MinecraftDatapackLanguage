# MDL Examples Test Suite

This directory contains comprehensive tests for all MDL examples from the documentation website. These tests ensure that all examples work correctly and prevent regressions.

## Test Structure

### MDL Files
- `hello_world.mdl` - Basic hello world example
- `particles.mdl` - Particle effects example
- `commands.mdl` - Custom commands example
- `combat_system.mdl` - Combat system example
- `ui_system.mdl` - UI system example
- `adventure_pack.mdl` - Complete adventure pack example

### Python API Equivalents
- `hello_world.py` - Python API version of hello world
- `particles.py` - Python API version of particles
- `commands.py` - Python API version of commands
- `combat_system.py` - Python API version of combat system
- `ui_system.py` - Python API version of UI system
- `adventure_pack.py` - Python API version of adventure pack

### Multi-file Project
- `adventure_pack/` - Multi-file project structure
  - `core.mdl` - Main pack and core systems
  - `combat/weapons.mdl` - Weapon-related functions
  - `combat/armor.mdl` - Armor-related functions
  - `ui/hud.mdl` - User interface functions
  - `data/tags.mdl` - Data tags and function tags

### Test Scripts
- `run_all_tests.py` - Comprehensive test runner

## Running Tests

### Local Testing

1. **Install MDL:**
   ```bash
   pipx install minecraft-datapack-language
   ```

2. **Run all tests:**
   ```bash
   python test_examples/run_all_tests.py
   ```

3. **Test individual examples:**
   ```bash
   # Test MDL files
   mdl check test_examples/hello_world.mdl
   mdl build --mdl test_examples/hello_world.mdl -o test_examples/dist
   
   # Test Python API
   python test_examples/hello_world.py
   
   # Test multi-file project
   mdl check test_examples/adventure_pack/
   mdl build --mdl test_examples/adventure_pack/ -o test_examples/dist
   ```

### CI/CD Testing

The tests are automatically run in CI/CD via GitHub Actions:

- **Trigger:** Push to main branch or pull request affecting test files
- **Workflow:** `.github/workflows/test-examples.yml`
- **Installation:** Uses pipx to install MDL
- **Tests:** Runs all examples and verifies output

## Test Coverage

The test suite covers:

1. **MDL Syntax Validation** - All examples pass `mdl check`
2. **MDL Build Process** - All examples build successfully
3. **Python API** - All Python equivalents work correctly
4. **Multi-file Projects** - Directory-based builds work
5. **CLI Functionality** - Basic CLI commands work
6. **Output Verification** - Generated datapacks have correct structure

## Adding New Examples

When adding new examples to the documentation:

1. **Create MDL file** in `test_examples/`
2. **Create Python equivalent** in `test_examples/`
3. **Update test script** in `run_all_tests.py`
4. **Test locally** to ensure it works
5. **Commit and push** - CI/CD will automatically test

## Test Results

The test suite provides detailed output including:

- ✅ Passed tests
- ❌ Failed tests with error details
- 📊 Summary statistics
- 🎉 Success confirmation

## Troubleshooting

### Common Issues

1. **MDL not found:** Install via `pipx install minecraft-datapack-language`
2. **Python import errors:** Install package with `pip install -e .`
3. **Build failures:** Check MDL syntax with `mdl check`
4. **CI/CD failures:** Check workflow logs for specific errors

### Debugging

- Run individual tests to isolate issues
- Check generated datapacks in `test_examples/dist/`
- Verify CLI commands work manually
- Review CI/CD logs for detailed error information

## Contributing

When contributing to the test suite:

1. Follow the existing structure
2. Add both MDL and Python API versions
3. Update the comprehensive test script
4. Test locally before committing
5. Ensure CI/CD passes

This test suite helps maintain the quality and reliability of MDL examples across all releases.
