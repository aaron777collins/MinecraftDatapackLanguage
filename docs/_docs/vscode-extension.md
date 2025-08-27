---
layout: page
title: VS Code Extension
permalink: /docs/vscode-extension/
---

# VS Code Extension

The MDL VS Code extension provides syntax highlighting, linting, and build commands for `.mdl` files.

## Features

- **Syntax Highlighting**: Color-coded MDL syntax
- **Linting**: Real-time error checking and validation
- **Build Commands**: Quick datapack compilation
- **Workspace Validation**: Check entire projects at once

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
   cd MinecraftDatapackLanguage/vscode-extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the extension:
   ```bash
   npm run compile
   ```

4. Press `F5` to launch the Extension Development Host

### Development Setup

For development and testing:

```bash
cd vscode-extension
npm install
npm run watch  # For continuous compilation
```

Then press `F5` in VS Code to launch the extension in a new window.

## Usage

### Opening MDL Files

1. Open any `.mdl` file in VS Code
2. The extension will automatically activate and provide syntax highlighting
3. You'll see color-coded syntax for:
   - Pack declarations
   - Namespaces
   - Functions
   - Comments
   - Commands

### Syntax Highlighting

The extension highlights the following MDL elements:

- **Pack declarations**: `pack "Name" description "Desc" pack_format 48`
- **Namespaces**: `namespace "example"`
- **Functions**: `function "name":`
- **Lifecycle hooks**: `on_load`, `on_tick`
- **Tags**: `tag function "minecraft:tick":`
- **Comments**: `# This is a comment`
- **Commands**: All lines within function blocks

### Linting

The extension provides real-time validation:

1. **Syntax errors**: Invalid MDL syntax is highlighted
2. **Indentation errors**: Incorrect indentation is flagged
3. **Missing declarations**: Missing pack declarations are detected
4. **Duplicate names**: Duplicate function names are identified

**Error indicators:**
- Red squiggly lines under syntax errors
- Yellow warnings for potential issues
- Hover over errors for detailed explanations

### Build Commands

The extension adds several commands to VS Code:

#### MDL: Build current file

Builds the currently open MDL file:

1. Open an `.mdl` file
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "MDL: Build current file"
4. Select the command
5. Choose an output directory
6. Optionally specify a wrapper name

#### MDL: Check Workspace

Validates all MDL files in the current workspace:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "MDL: Check Workspace"
3. Select the command
4. View results in the Problems panel

### Keyboard Shortcuts

You can add custom keyboard shortcuts for the MDL commands:

1. Open VS Code settings (`Ctrl+,`)
2. Go to "Keyboard Shortcuts"
3. Search for "MDL"
4. Add shortcuts for:
   - `mdl.build` - Build current file
   - `mdl.checkWorkspace` - Check workspace

**Example shortcuts:**
```json
{
  "key": "ctrl+shift+b",
  "command": "mdl.build",
  "when": "resourceExtname == .mdl"
},
{
  "key": "ctrl+shift+c",
  "command": "mdl.checkWorkspace"
}
```

## Configuration

### Extension Settings

The extension can be configured through VS Code settings:

1. Open VS Code settings (`Ctrl+,`)
2. Search for "MDL"
3. Configure the following options:

**`mdl.enableLinting`** (default: `true`)
- Enable or disable real-time linting

**`mdl.lintingMode`** (default: `"onSave"`)
- When to run linting: `"onSave"`, `"onType"`, or `"manual"`

**`mdl.buildOutputDirectory`** (default: `"dist"`)
- Default output directory for builds

### Workspace Settings

You can configure MDL settings per workspace by creating a `.vscode/settings.json` file:

```json
{
  "mdl.enableLinting": true,
  "mdl.lintingMode": "onSave",
  "mdl.buildOutputDirectory": "build",
  "files.associations": {
    "*.mdl": "mdl"
  }
}
```

## Troubleshooting

### Extension Not Working

1. **Check if MDL is installed**: The extension requires MDL to be installed on your system
2. **Verify file association**: Make sure `.mdl` files are associated with the MDL language
3. **Check output panel**: Look for error messages in the Output panel (View → Output → MDL)

### Build Commands Not Available

1. **Ensure MDL is in PATH**: The extension needs to find the `mdl` command
2. **Restart VS Code**: Sometimes a restart is needed after installation
3. **Check command palette**: Commands should appear when typing "MDL"

### Linting Issues

1. **Check MDL installation**: Run `mdl --version` in terminal to verify installation
2. **Verify file syntax**: Use `mdl check filename.mdl` to test manually
3. **Check extension logs**: Look for errors in the Developer Tools (Help → Toggle Developer Tools)

## Development

### Project Structure

```
vscode-extension/
├── src/
│   └── extension.ts          # Main extension code
├── syntaxes/
│   └── mdl.tmLanguage.json   # Syntax highlighting rules
├── language-configuration.json  # Language configuration
├── package.json              # Extension manifest
└── tsconfig.json            # TypeScript configuration
```

### Key Files

**`src/extension.ts`**: Main extension logic
- Command registration
- Linting integration
- Build command handling

**`syntaxes/mdl.tmLanguage.json`**: Syntax highlighting rules
- Token definitions
- Pattern matching
- Color themes

**`language-configuration.json`**: Language behavior
- Comment patterns
- Bracket matching
- Auto-indentation

### Adding Features

To add new features to the extension:

1. **Modify `extension.ts`**: Add new commands or functionality
2. **Update `package.json`**: Register new commands
3. **Test locally**: Use `F5` to test changes
4. **Build**: Run `npm run compile` to build

### Testing

1. **Unit tests**: Add tests in a `test/` directory
2. **Integration tests**: Test with real MDL files
3. **Manual testing**: Test all features in the Extension Development Host

## Contributing

### Development Setup

1. Fork the repository
2. Clone your fork
3. Navigate to `vscode-extension/`
4. Run `npm install`
5. Make your changes
6. Test with `F5`
7. Submit a pull request

### Code Style

- Use TypeScript for all new code
- Follow VS Code extension conventions
- Add comments for complex logic
- Include error handling

### Testing Checklist

Before submitting changes, test:

- [ ] Syntax highlighting works correctly
- [ ] Linting catches errors
- [ ] Build commands work
- [ ] Workspace validation functions
- [ ] Error messages are clear
- [ ] Performance is acceptable

## Future Features

Planned enhancements for the VS Code extension:

- **IntelliSense**: Auto-completion for MDL syntax
- **Snippets**: Code templates for common patterns
- **Debugging**: Step-through debugging for MDL files
- **Multi-file support**: Better handling of multi-file projects
- **Custom themes**: Additional color themes for MDL
- **Formatting**: Auto-formatting of MDL files
- **Refactoring**: Rename functions across files
- **Search**: Search and replace across MDL files

## Support

If you encounter issues with the VS Code extension:

1. **Check the documentation**: This page and the main README
2. **Search issues**: Look for similar problems on GitHub
3. **Create an issue**: Provide detailed information about the problem
4. **Include logs**: Share relevant error messages and logs

## Related Documentation

- **[Getting Started]({{ site.baseurl }}/docs/getting-started/)** - Installation and first steps
- **[Language Reference]({{ site.baseurl }}/docs/language-reference/)** - Complete MDL syntax
- **[CLI Reference]({{ site.baseurl }}/docs/cli-reference/)** - Command-line tools
- **[Examples]({{ site.baseurl }}/docs/examples/)** - Working examples
