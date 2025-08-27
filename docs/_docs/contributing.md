---
layout: page
title: Contributing
permalink: /docs/contributing/
---

# Contributing to MDL

Thank you for your interest in contributing to Minecraft Datapack Language (MDL)! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic knowledge of Python and Minecraft datapacks

### Development Setup

1. **Fork the repository**:
   ```bash
   git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
   cd MinecraftDatapackLanguage
   ```

2. **Install in development mode**:
   ```bash
   python -m pip install -e .
   ```

3. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt  # if available
   ```

4. **Verify installation**:
   ```bash
   mdl --version
   mdl --help
   ```

## Project Structure

```
MinecraftDatapackLanguage/
├── minecraft_datapack_language/    # Main package
│   ├── __init__.py
│   ├── cli.py                      # Command-line interface
│   ├── mdl_parser.py               # MDL language parser
│   ├── pack.py                     # Pack generation
│   └── utils.py                    # Utility functions
├── vscode-extension/               # VS Code extension
├── scripts/                        # Build and release scripts
├── tools/                          # Development tools
├── docs/                           # Documentation
└── tests/                          # Test files
```

## Areas to Contribute

### 1. Core Language Features

- **Parser improvements**: Enhance the MDL parser
- **New syntax features**: Add new language constructs
- **Error handling**: Improve error messages and validation
- **Performance**: Optimize parsing and compilation

### 2. CLI Tools

- **New commands**: Add useful CLI commands
- **Better output**: Improve user experience
- **Configuration**: Add configuration options
- **Integration**: Better integration with other tools

### 3. Python API

- **API improvements**: Enhance the Python API
- **New features**: Add new capabilities
- **Documentation**: Improve API documentation
- **Examples**: Add more examples

### 4. VS Code Extension

- **Syntax highlighting**: Improve language support
- **IntelliSense**: Add auto-completion
- **Debugging**: Add debugging support
- **Snippets**: Add code snippets

### 5. Documentation

- **User guides**: Improve existing documentation
- **Examples**: Add more examples
- **Tutorials**: Create step-by-step tutorials
- **API docs**: Improve API documentation

### 6. Testing

- **Unit tests**: Add comprehensive tests
- **Integration tests**: Test end-to-end functionality
- **Performance tests**: Ensure good performance
- **Regression tests**: Prevent bugs from returning

## Development Workflow

### 1. Choose an Issue

1. Check the [Issues](https://github.com/aaron777collins/MinecraftDatapackLanguage/issues) page
2. Look for issues labeled `good first issue` for beginners
3. Comment on the issue to let others know you're working on it
4. Fork the repository if you haven't already

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

- Write your code following the coding standards
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 4. Test Your Changes

```bash
# Run the test suite
python -m pytest

# Test the CLI
mdl --help
mdl build --mdl sample.mdl -o test_output

# Test the Python API
python -c "from minecraft_datapack_language import Pack; print('API works!')"
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots if applicable
- Test results

## Coding Standards

### Python Code

- **Style**: Follow PEP 8
- **Type hints**: Use type hints where appropriate
- **Docstrings**: Add docstrings to functions and classes
- **Comments**: Add comments for complex logic

### MDL Language

- **Consistency**: Follow existing language patterns
- **Error messages**: Provide clear, helpful error messages
- **Performance**: Consider performance implications
- **Backward compatibility**: Maintain compatibility when possible

### Documentation

- **Clarity**: Write clear, concise documentation
- **Examples**: Include practical examples
- **Structure**: Use consistent formatting
- **Links**: Link to related documentation

## Testing Guidelines

### Unit Tests

- **Coverage**: Aim for high test coverage
- **Isolation**: Tests should be independent
- **Naming**: Use descriptive test names
- **Assertions**: Use specific assertions

### Integration Tests

- **End-to-end**: Test complete workflows
- **Real scenarios**: Test realistic use cases
- **Error cases**: Test error conditions
- **Performance**: Test performance characteristics

### Example Test

```python
def test_pack_creation():
    """Test basic pack creation functionality."""
    pack = Pack(name="Test Pack", pack_format=48)
    
    # Test namespace creation
    namespace = pack.namespace("test")
    assert namespace is not None
    
    # Test function addition
    namespace.function("hello", 'say Hello!')
    
    # Test build
    pack.build("test_output")
    
    # Verify output files exist
    assert os.path.exists("test_output/test_pack/pack.mcmeta")
    assert os.path.exists("test_output/test_pack/data/test/functions/hello.mcfunction")
```

## Documentation Guidelines

### Writing Documentation

- **Audience**: Write for the target audience
- **Structure**: Use clear headings and sections
- **Examples**: Include working examples
- **Links**: Link to related topics

### Code Examples

- **Complete**: Provide complete, runnable examples
- **Clear**: Use clear, descriptive variable names
- **Commented**: Add comments explaining key parts
- **Tested**: Ensure examples work correctly

### API Documentation

- **Parameters**: Document all parameters
- **Return values**: Document return values
- **Exceptions**: Document exceptions that may be raised
- **Examples**: Include usage examples

## Release Process

### Version Management

MDL uses semantic versioning:
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

### Release Steps

1. **Update version**: Update version in `pyproject.toml`
2. **Update changelog**: Document changes in `CHANGELOG.md`
3. **Test thoroughly**: Run all tests
4. **Create release**: Use GitHub releases
5. **Publish to PyPI**: Upload to Python Package Index

### Release Scripts

Use the provided release scripts:

```bash
# Create a patch release
./scripts/release.sh patch "Bug fixes"

# Create a minor release
./scripts/release.sh minor "New features"

# Create a major release
./scripts/release.sh major "Breaking changes"
```

## Community Guidelines

### Code of Conduct

- **Respect**: Be respectful to all contributors
- **Inclusive**: Welcome contributors from all backgrounds
- **Constructive**: Provide constructive feedback
- **Helpful**: Help others learn and grow

### Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Pull requests**: Provide clear, constructive feedback
- **Documentation**: Help improve documentation

### Recognition

- **Contributors**: All contributors are recognized in the project
- **Credits**: Credit contributors in release notes
- **Thanks**: Thank contributors for their work

## Getting Help

### Questions and Support

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the documentation first
- **Examples**: Look at existing examples

### Mentorship

- **New contributors**: Experienced contributors can help newcomers
- **Code reviews**: Get feedback on your code
- **Pair programming**: Work together on features
- **Documentation**: Help improve documentation

## Future Roadmap

### Planned Features

- **Enhanced syntax**: More language features
- **Better tooling**: Improved development tools
- **Performance**: Better performance
- **Integration**: Better integration with other tools

### Contributing to the Roadmap

- **Suggestions**: Suggest new features
- **Prioritization**: Help prioritize features
- **Implementation**: Implement planned features
- **Testing**: Test new features

## Legal

### License

MDL is licensed under the GPL-3.0 License. By contributing, you agree to license your contributions under the same license.

### Copyright

Contributors retain copyright to their contributions, but grant the project a license to use and distribute them.

## Thank You

Thank you for contributing to MDL! Your contributions help make the project better for everyone in the Minecraft community.

Whether you're fixing a bug, adding a feature, improving documentation, or just asking questions, your involvement is valuable and appreciated.
