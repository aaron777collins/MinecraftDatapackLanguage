---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

# Getting Started

This guide will help you install Minecraft Datapack Language (MDL) and create your first datapack with control structures, variables, expressions, and multi-file projects.

> **📚 Need help with MDL syntax?** Check out the [Language Reference](/docs/language-reference/) for complete syntax documentation.

## Installation

### Option A: Using pipx (Recommended)

pipx installs Python applications in isolated environments, which is perfect for command-line tools like MDL.

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install MDL
pipx install minecraft-datapack-language

# Verify installation
mdl --help
```

**Note**: After installing pipx, you may need to restart your terminal or run `source ~/.bashrc` (Linux/macOS) or restart your PowerShell session (Windows).

### Option B: Using pip in a Virtual Environment

If you prefer using pip directly:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install MDL
pip install minecraft-datapack-language

# Verify installation
mdl --help
```

### Option C: From Source (for Contributors)

```bash
# Clone the repository
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage

# Install in development mode
python -m pip install -e .
```

## Updating MDL

- **pipx**: `pipx upgrade minecraft-datapack-language`
- **pip**: `pip install -U minecraft-datapack-language`
- **Pin a version**: `pipx install "minecraft-datapack-language==12.0.10"`

## Your First Datapack

Let's create a simple datapack that demonstrates MDL's core features.

### 1. Create the MDL File

Create a file called `hello.mdl` with this content:

```mdl
// hello.mdl
pack "My First Pack" "A simple example" 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    say Counter: $counter$;
}

on_load "example:hello";
```

### 2. Build the Datapack

```bash
mdl build --mdl hello.mdl -o dist
```

This creates a `dist/` directory containing your compiled datapack.

### 3. Install in Minecraft

1. Copy the `dist/my_first_pack/` folder to your Minecraft world's `datapacks/` folder
2. In-game, run `/reload` to load the datapack
3. You should see the hello message and counter updates!

## Key Concepts

### Variables

MDL supports number variables that are automatically converted to Minecraft scoreboard objectives:

```mdl
var num player_health = 20;
var num score = 0;
var num level = 1;
```

### Variable Substitution

Use `$variable_name$` to substitute variables in commands:

```mdl
say Player health: $player_health$;
tellraw @a {"text":"Score: $score$","color":"gold"};
```

### Control Structures

MDL supports real if/else statements and while loops:

```mdl
if "$health$ < 10" {
    say Health is low!;
    effect give @s minecraft:regeneration 10 1;
} else {
    say Health is good;
}

while "$counter$ < 5" {
    say Counter: $counter$;
    counter = counter + 1;
}
```

### Functions

Define functions that can be called by hooks or other functions:

```mdl
function "my_function" {
    say This is my function!;
    // Your commands here
}

// Call the function
function "example:my_function";
```

### Hooks

Automatically run functions when the datapack loads or every tick:

```mdl
on_load "example:init";    // Runs when datapack loads
on_tick "example:update";  // Runs every tick
```

## Multi-file Projects

MDL supports organizing code across multiple files. Only the main file needs a pack declaration:

**`main.mdl`** (with pack declaration):
```mdl
pack "My Game" "A multi-file game" 82;

namespace "game";

var num player_count = 0;

function "init" {
    say Game initialized!;
}
```

**`ui.mdl`** (no pack declaration needed):
```mdl
namespace "ui";

function "show_hud" {
    tellraw @a {"text":"Players: $player_count$","color":"green"};
}
```

Build all files together:
```bash
mdl build --mdl . -o dist
```

## Registry Types

MDL supports all Minecraft registry types by referencing JSON files:

```mdl
// Recipes
recipe "custom_sword" "recipes/sword.json";

// Loot tables
loot_table "treasure" "loot_tables/treasure.json";

// Advancements
advancement "first_sword" "advancements/sword.json";

// Predicates
predicate "has_sword" "predicates/sword.json";

// Item modifiers
item_modifier "sword_nbt" "item_modifiers/sword.json";

// Structures
structure "custom_house" "structures/house.json";
```

## Next Steps

- **Language Reference**: Learn the complete MDL syntax
- **Examples**: See working examples of all features
- **Multi-file Projects**: Organize large projects
- **CLI Reference**: Master the command-line tools
- **Python API**: Create datapacks programmatically
- **VS Code Extension**: Get syntax highlighting and linting

## Troubleshooting

### Common Issues

**"mdl: command not found"**
- Make sure pipx is in your PATH
- Try restarting your terminal
- Run `pipx ensurepath` and restart

**"No .mdl files found"**
- Make sure you're in the right directory
- Check that your file has the `.mdl` extension
- Use `mdl build --mdl . -o dist` to build all files in current directory

**"Failed to parse MDL files"**
- Check your syntax (missing semicolons, brackets, etc.)
- Use `mdl lint your_file.mdl` to check for errors
- Make sure all brackets and braces are properly closed

**Datapack not working in-game**
- Make sure you copied the entire folder from `dist/`
- Run `/reload` in-game
- Check the game logs for errors
- Verify the pack format matches your Minecraft version

### Getting Help

- **Documentation**: Check the language reference and examples
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share projects
- **Examples**: Study the working examples in the repository

## Development Setup

For contributors, MDL includes a comprehensive development system:

**Linux/macOS:**
```bash
./scripts/dev_setup.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\dev_setup.ps1
```

This sets up:
- **`mdl`** - Stable, globally installed version
- **`mdlbeta`** - Local development version for testing changes

**Development Workflow:**
1. Make changes to the code
2. Rebuild: `./scripts/dev_build.sh`
3. Test: `mdlbeta build --mdl your_file.mdl -o dist`
4. Validate: `mdl check-advanced your_file.mdl`

For detailed development information, see [DEVELOPMENT.md](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/DEVELOPMENT.md).
