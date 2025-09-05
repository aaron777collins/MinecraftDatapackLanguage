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
# Zips by default -> creates <output_dir>.zip
# Use --no-zip to skip archive creation
```

**Examples:**
```bash
# Build single file
mdl build --mdl hello.mdl -o dist

# Build entire directory
mdl build --mdl myproject/ -o dist

# Build current directory
mdl build --mdl . -o dist

# Build with warnings suppressed
mdl build --mdl . -o dist --ignore-warnings
```

**Options:**
- `--mdl <files>`: MDL files or directories to build
- `-o <output_dir>`: Output directory for compiled datapack
- `--verbose`: Show detailed build information
- `--wrapper <name>`: Custom wrapper name for the datapack

### Check Command

Validate MDL files for syntax and semantic errors:

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

# Check with warnings suppressed
mdl check myproject/ --ignore-warnings
```

**Error Reporting:**
The check command provides comprehensive error reporting with:
- Exact file location (line, column)
- Context lines showing the problematic code
- Helpful suggestions for fixing issues
- Multiple error collection (reports all errors, not just the first)

**Example Error Output:**
```
Error 1: MDLSyntaxError in test.mdl:15:8
Missing closing brace for if statement
Context:
  13:   if $score<@s>$ > 10 {
  14:     say "High score!"
  15:     score<@s> = 0
  16:   }

Suggestion: Add closing brace '}' after line 15

Error 2: MDLLexerError in test.mdl:22:12
Unterminated string literal
Context:
  20:   say "Hello world
  21:   score<@s> = 10
  22:   say "Goodbye

Suggestion: Add closing quote '"' at the end of line 20
```

### New Command

Create a new MDL project with template files:

```bash
mdl new <project_name>
```

**Examples:**
```bash
# Create a new project in current directory
mdl new my_awesome_pack

# Create a project with specific name
mdl new adventure_map

# Create a project in a subdirectory
mdl new projects/survival_plus
```

**What it creates:**
The new command generates a complete project structure with:
- `README.md` - Project documentation and setup instructions
- `main.mdl` - Main MDL file with basic template structure
- Proper pack declaration and namespace setup
- Example functions and basic syntax

**Generated project structure:**
```
my_awesome_pack/
├── README.md
└── main.mdl
```

**Template content includes:**
- Pack metadata (name, description, format)
- Namespace declaration
- Sample function definitions
- Basic MDL syntax examples
- Load function setup

## Command Options

### Build Options

| Option | Description | Example |
|--------|-------------|---------|
| `--mdl <files>` | MDL files or directories to build | `--mdl "main.mdl ui.mdl"` |
| `-o <dir>` | Output directory | `-o dist` |
| `--verbose` | Show detailed output | `--verbose` |
| `--wrapper <name>` | Custom wrapper name | `--wrapper mypack` |
| `--no-zip` | Skip creating zip archive (zip is default) | `--no-zip` |
| `--ignore-warnings` | Suppress warning messages | `--ignore-warnings` |

### Check Options

| Option | Description | Example |
|--------|-------------|---------|
| `--verbose` | Show detailed validation information | `--verbose` |
| `--ignore-warnings` | Suppress warning messages | `--ignore-warnings` |

### New Options

| Option | Description | Example |
|--------|-------------|---------|
| `<project_name>` | Name of the new project to create | `mdl new my_pack` |

## Error Handling

MDL provides comprehensive error handling and reporting:

### Error Types

- **MDLSyntaxError**: Basic syntax violations (missing semicolons, braces)
- **MDLLexerError**: Token recognition issues (unterminated strings, invalid characters)
- **MDLParserError**: Parsing and structure problems (malformed statements)
- **MDLValidationError**: Semantic validation failures (undefined variables, invalid references)
- **MDLFileError**: File access and I/O issues
- **MDLBuildError**: Build process failures
- **MDLCompilationError**: Compilation and linking issues
- **MDLConfigurationError**: CLI configuration and argument errors

### Error Features

- **Exact Location**: Errors include precise line and column numbers
- **Context Lines**: Shows surrounding code for better debugging
- **Helpful Suggestions**: Provides specific fix recommendations
- **Multiple Error Collection**: Reports all errors, not just the first one
- **Error Summaries**: Shows total error and warning counts
- **Verbose Mode**: Detailed error information with additional context
- **Warning Suppression**: Use `--ignore-warnings` to hide warning messages and show only errors

### Example Error Output

```
🔍 Checking test.mdl...

Error 1: MDLSyntaxError in test.mdl:15:8
Missing closing brace for if statement
Context:
  13:   if "$score<@s>$ > 10" {
  14:     say "High score!"
  15:     score<@s> = 0
  16:   }

Suggestion: Add closing brace '}' after line 15

Error 2: MDLLexerError in test.mdl:22:12
Unterminated string literal
Context:
  20:   say "Hello world
  21:   score<@s> = 10
  22:   say "Goodbye

Suggestion: Add closing quote '"' at the end of line 20

Error 3: MDLValidationError in test.mdl:8:5
Undefined variable 'player_score'
Context:
   6:   score<@s> = 10
   7:   lives<@s> = 3
   8:   player_score<@s> = 5
   9:   say "Score: $score<@s>$"

Suggestion: Declare the variable first with 'variable player_score = 0'

Summary: 3 errors found
```
| `--verbose` | Show detailed output | `--verbose` |

## Examples

### Basic Workflow

1. **Create a new project:**
```bash
mdl new hello_world
```

2. **Check the generated file:**
```bash
mdl check hello_world/main.mdl
```

3. **Build the datapack:**
```bash
mdl build --mdl hello_world/main.mdl -o dist
```

4. **Install in Minecraft:**
- Copy `dist/hello_world/` to your world's `datapacks/` folder
- Run `/reload` in-game

**Alternative: Manual file creation**
If you prefer to create files manually, you can start with:
```mdl
// hello.mdl
pack "hello" "My first datapack" 82;
namespace "hello";

function hello:main<@s> {
    say "Hello, Minecraft!";
}

on_load hello:main<@s>;
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

### Explicit Scopes in Conditions

MDL supports explicit scope selectors in if/while conditions, allowing you to override declared variable scopes:

```mdl
// Variables with different scopes
var num playerScore<@s> = 0;                    // Defaults to @s
var num globalCounter<@a> = 0;                  // Global scope
var num teamScore<@a[team=red]> = 0;            // Team scope

function hello:main<@s> {
    // Use explicit scope in conditions
    if $playerScore<@s>$ > 10 {
        say "Current player score is high!";
    }
    
    if $globalCounter<@a>$ > 100 {
        say "Global counter reached milestone!";
    }
    
    if $teamScore<@a[team=red]>$ > 50 {
        say "Red team is winning!";
    }
    
    // Check another player's score
    if $playerScore<@p[name=Steve]>$ > 5 {
        say "Steve has a good score!";
    }
}
```

**Benefits:**
- **Override declared scopes**: Use different scopes than what was declared
- **Check other entities**: Compare scores across different players/teams
- **Flexible conditions**: Mix and match scopes as needed
- **Clear intent**: Explicit scope makes code more readable

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
