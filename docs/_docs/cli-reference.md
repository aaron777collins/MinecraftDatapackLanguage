---
layout: page
title: CLI Reference
permalink: /docs/cli-reference/
---

# CLI Reference

The MDL command-line interface provides tools for creating, validating, and building datapacks.

## Overview

```bash
mdl [command] [options]
```

## Commands

### `new` - Create a new datapack project

Creates a new datapack project with the specified structure.

```bash
mdl new <project_name> [options]
```

**Options:**
- `--name "Pack Name"` - Set the datapack name
- `--pack-format N` - Set the pack format (default: 82)
- `--format {legacy,modern}` - Pack format style: 'legacy' (pre-82) or 'modern' (82+) (default: modern)
- `--description "Description"` - Set the datapack description

**Examples:**

**Modern format (default):**
```bash
mdl new my_pack --name "My Adventure Pack"
# Creates pack format 82+ with min_format, max_format, and min_engine_version
```

**Legacy format:**
```bash
mdl new my_pack --name "My Adventure Pack" --format legacy --pack-format 48
# Creates legacy pack format 48
```

This creates:
```
my_pack/
├── mypack.mdl
└── README.md
```

### `check` - Validate MDL files

Validates MDL files for syntax errors and issues.

```bash
mdl check <path> [options]
```

**Arguments:**
- `<path>` - Path to `.mdl` file, directory, or space-separated file list

**Options:**
- `--json` - Output results in JSON format for detailed diagnostics

**Examples:**
```bash
# Check a single file
mdl check my_pack.mdl

# Check an entire directory
mdl check my_pack/

# Check multiple specific files
mdl check "file1.mdl file2.mdl file3.mdl"

# Get detailed JSON output
mdl check --json my_pack/
```

**Output:**
- Success: No output (exit code 0)
- Errors: Error messages with file paths and line numbers (exit code 1)

### `build` - Build datapacks

Compiles MDL files into Minecraft datapacks.

```bash
mdl build [options]
```

**Required Options:**
- `--mdl <path>` or `--src <path>` - Path to `.mdl` file, directory, or space-separated file list
- `-o, --out <dir>` - Output directory for the built datapack

**Optional Options:**
- `--wrapper <name>` - Custom wrapper folder/zip name (default: first namespace or pack name slug)
- `--pack-format <N>` - Minecraft pack format (default: 48 for 1.21+)
- `-v, --verbose` - Show detailed processing information including file merging
- `--py-module <path>` - Alternative: build from Python module with `create_pack()` function

**Examples:**

**Single file build:**
```bash
mdl build --mdl hello.mdl -o dist
```

**Directory build:**
```bash
mdl build --mdl my_pack/ -o dist
```

**Multiple files build:**
```bash
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist
```

**With custom wrapper name:**
```bash
mdl build --mdl my_pack/ -o dist --wrapper mypack
```

**With verbose output:**
```bash
mdl build --mdl my_pack/ -o dist --verbose
```

**From Python module:**
```bash
mdl build --py-module my_module:create_pack -o dist
```

## Global Options

### `--help, -h`

Show help for the command.

```bash
mdl --help
mdl build --help
```

### `--version`

Show the MDL version.

```bash
mdl --version
```

## Multi-file Builds

MDL supports building datapacks from multiple `.mdl` files. This is useful for organizing large projects.

### How it works

1. **Directory scanning**: When you pass a directory to `--mdl`, MDL recursively finds all `.mdl` files
2. **File merging**: Each file is parsed into a `Pack` object, then merged into a single datapack
3. **Conflict resolution**: Duplicate function names within the same namespace will cause an error
4. **Pack metadata**: Only the **first file** should have a pack declaration (name, description, format)
5. **Module files**: Subsequent files should **not** have pack declarations - they are treated as modules
6. **Single file requirement**: When compiling a single file, it **must** have a pack declaration

### Best practices

- **One pack declaration per project**: Only the **first file** should have a pack declaration
- **Module files**: All other files should **not** have pack declarations - they are treated as modules
- **Single file requirement**: When compiling a single file, it **must** have a pack declaration
- **Organize by namespace**: Consider splitting files by namespace or feature
- **Use descriptive filenames**: `core.mdl`, `combat.mdl`, `ui.mdl` etc.
- **Avoid conflicts**: Ensure function names are unique within each namespace

### Example project structure

```
my_datapack/
├── core.mdl          # ✅ HAS pack declaration
├── combat/
│   ├── weapons.mdl   # ❌ NO pack declaration (module)
│   └── armor.mdl     # ❌ NO pack declaration (module)
├── ui/
│   └── hud.mdl       # ❌ NO pack declaration (module)
└── data/
    └── recipes.mdl   # ❌ NO pack declaration (module)
```

**Important**: Only `core.mdl` should have a `pack "Name"` declaration. All other files are modules that merge into the main pack.

### Usage Examples

**Build from directory:**
```bash
mdl build --mdl my_datapack/ -o dist
```

**Build from specific files:**
```bash
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist
```

**Check entire project:**
```bash
mdl check my_datapack/
```

**Check with verbose output:**
```bash
mdl build --mdl my_datapack/ -o dist --verbose
```

## Error Handling

### Common Error Types

1. **Missing pack declaration**: Single files must have a pack declaration
2. **Duplicate pack declarations**: Only the first file in a multi-file project should have a pack declaration
3. **Single file compilation**: When compiling a single file, it must have a pack declaration
3. **Function conflicts**: Duplicate function names within the same namespace will cause an error
4. **Clear error messages**: Errors include file paths and line numbers for easy debugging

### Error Message Format

```
Error: [file.mdl:line:column] Description of the error
```

**Example:**
```
Error: [core.mdl:5:1] Duplicate function name 'hello' in namespace 'example'
```

### Troubleshooting

1. **Use `mdl check` first**: Always validate your files before building
2. **Check file structure**: Ensure only the first file has a pack declaration in multi-file projects
3. **Verify function names**: Make sure function names are unique within each namespace
4. **Check syntax**: Ensure proper indentation (4 spaces) and valid MDL syntax

## Output Structure

When you build a datapack, MDL creates the following structure:

```
dist/
├── mypack/                    # Wrapper folder (customizable)
│   ├── pack.mcmeta           # Pack metadata
│   └── data/
│       ├── minecraft/
│       │   └── tags/
│       │       └── functions/
│       │           ├── load.json
│       │           └── tick.json
│       └── example/          # Your namespace
│           └── functions/
│               └── hello.mcfunction
└── mypack.zip               # Optional zip file
```

### Pack Metadata

The `pack.mcmeta` file contains:

```json
{
  "pack": {
    "pack_format": 48,
    "description": "My Datapack"
  }
}
```

### Function Tags

Function tags are automatically created for `on_load` and `on_tick` hooks:

**`data/minecraft/tags/functions/load.json`:**
```json
{
  "values": [
    "example:init"
  ]
}
```

**`data/minecraft/tags/functions/tick.json`:**
```json
{
  "values": [
    "example:tick"
  ]
}
```

## Integration Examples

### Build Scripts

**Simple build script:**
```bash
#!/bin/bash
# build.sh

echo "Building datapack..."
mdl build --mdl src/ -o dist --verbose

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Output: dist/"
else
    echo "Build failed!"
    exit 1
fi
```

**Python integration:**
```python
import subprocess
import sys

def build_datapack():
    try:
        result = subprocess.run([
            'mdl', 'build',
            '--mdl', 'src/',
            '-o', 'dist',
            '--verbose'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Build successful!")
            print(result.stdout)
        else:
            print("Build failed!")
            print(result.stderr)
            sys.exit(1)
            
    except FileNotFoundError:
        print("Error: mdl command not found. Make sure MDL is installed.")
        sys.exit(1)

if __name__ == "__main__":
    build_datapack()
```

### CI/CD Integration

**GitHub Actions example:**
```yaml
name: Build Datapack

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install MDL
      run: |
        python -m pip install --upgrade pip
        pip install minecraft-datapack-language
    
    - name: Check MDL files
      run: mdl check src/
    
    - name: Build datapack
      run: mdl build --mdl src/ -o dist --verbose
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: datapack
        path: dist/
```

## Performance Tips

1. **Use directory builds**: For large projects, use `mdl build --mdl src/` instead of listing individual files
2. **Check before building**: Use `mdl check` to catch errors early
3. **Use verbose mode sparingly**: Only use `--verbose` when debugging
4. **Organize files**: Group related functions in the same files to reduce parsing overhead

## Exit Codes

- `0` - Success
- `1` - Error (syntax error, build failure, etc.)
- `2` - Usage error (invalid arguments, missing required options)
