---
layout: page
title: CLI Reference
permalink: /docs/cli-reference/
---

The MDL command-line interface provides tools for building and managing Minecraft datapacks.

## Installation

Install MDL using pipx:

```bash
pipx install minecraft-datapack-language
```

## Basic Commands

### Build Command

Build MDL files into Minecraft datapacks:

```bash
mdl build --mdl <files> -o <output_dir>
```

**Examples:**
```bash
# Build single file
mdl build --mdl hello.mdl -o dist

# Build entire directory
mdl build --mdl myproject/ -o dist

# Build current directory
mdl build --mdl . -o dist
```

**Options:**
- `--mdl <files>`: MDL files or directories to build
- `-o <output_dir>`: Output directory for compiled datapack
- `--verbose`: Show detailed build information
- `--wrapper <name>`: Custom wrapper name for the datapack

### Check Command

Validate MDL files without building:

```bash
mdl check <files>
```

**Examples:**
```bash
# Check single file
mdl check hello.mdl

# Check current directory
mdl check .

# Check entire directory
mdl check myproject/
```

### Check Command

Check MDL files for style and potential issues:

```bash
mdl check <files>
```

**Examples:**
```bash
# Check single file
mdl check hello.mdl

# Check multiple files
mdl check myproject/

# Check multiple files
mdl check .
```

## Command Options

### Build Options

| Option | Description | Example |
|--------|-------------|---------|
| `--mdl <files>` | MDL files or directories to build | `--mdl "main.mdl ui.mdl"` |
| `-o <dir>` | Output directory | `-o dist` |
| `--verbose` | Show detailed output | `--verbose` |
| `--wrapper <name>` | Custom wrapper name | `--wrapper mypack` |

### Check Options

| Option | Description | Example |
|--------|-------------|---------|
| `--json` | Output in JSON format | `--json` |
| `--verbose` | Show detailed output | `--verbose` |

## Examples

### Basic Workflow

1. **Create MDL file:**
```mdl
// hello.mdl
pack "hello" "My first datapack" 82;
namespace "hello";

function "main" {
    say Hello, Minecraft!;
}

on_load "hello:main";
```

2. **Check the file:**
```bash
mdl check hello.mdl
```

3. **Build the datapack:**
```bash
mdl build --mdl hello.mdl -o dist
```

4. **Install in Minecraft:**
- Copy `dist/hello/` to your world's `datapacks/` folder
- Run `/reload` in-game

### Multi-File Project

**Project structure:**
```
my_project/
├── main.mdl
├── ui.mdl
└── game.mdl
```

**Build command:**
```bash
mdl build --mdl . -o dist
```

### Verbose Build

Get detailed information about the build process:

```bash
mdl build --mdl hello.mdl -o dist --verbose
```

Output includes:
- Files being processed
- Functions being generated
- Variables being initialized
- Any warnings or errors

## Error Handling

### Common Errors

**"No .mdl files found"**
```bash
# Make sure you're in the right directory
ls *.mdl

# Use explicit file paths
mdl build --mdl ./myfile.mdl -o dist

# or build the directory itself
mdl build --mdl . -o dist
```

**"Failed to parse MDL files"**
```bash
# Check syntax
mdl check myfile.mdl

# Look for missing semicolons, brackets, etc.
```

**"Duplicate function name"**
```bash
# Check for duplicate function names in the same namespace
mdl check myproject/
```

### Debugging

Use verbose mode to get more information:

```bash
mdl build --mdl myfile.mdl -o dist --verbose
mdl check myfile.mdl --verbose
```

## Output Structure

The build command creates a datapack with this structure:

```
dist/
└── pack_name/
    ├── pack.mcmeta
    └── data/
        └── namespace/
            ├── function/
            │   ├── main.mcfunction
            │   └── other.mcfunction
            └── tags/
                └── function/
                    ├── load.json
                    └── tick.json
```

## Integration

### With Build Tools

**Makefile example:**
```makefile
.PHONY: build clean

build:
	mdl build --mdl . -o dist

clean:
	rm -rf dist/

check:
	mdl check .
```

**npm scripts example:**
```json
{
  "scripts": {
    "build": "mdl build --mdl . -o dist",
    "check": "mdl check .",
    "clean": "rm -rf dist/"
  }
}
```

### With CI/CD

**GitHub Actions example:**
```yaml
name: Build Datapack
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install minecraft-datapack-language
      - run: mdl check .
      - run: mdl build --mdl . -o dist
      - run: mdl check .
```
