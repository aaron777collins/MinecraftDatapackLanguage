---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

# Getting Started

This guide will help you install Minecraft Datapack Language (MDL) and create your first datapack with control structures, variables, expressions, and multi-file projects.

> **📚 Need help with MDL syntax?** Check out the [Language Reference]({{ site.baseurl }}/docs/language-reference/) for complete syntax documentation.

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
- **Pin a version**: `pipx install "minecraft-datapack-language==<version>"` (replace `<version>` with desired version)

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

### Variable Scoping

MDL supports variable scoping to store data on different entities. By default, variables are stored on the executing entity (`@s`), but you can specify custom scopes.

```mdl
// Player-specific variables (default behavior)
var num player_score = 0;
var num player_level = 1;

// Global variables (stored on server armor stand)
var num global_timer scope<global> = 0;
var num game_state scope<global> = 0;

// Player-scoped variables (explicit)
var num player_health scope<@s> = 20;

// Team-scoped variables
var num team_score scope<@a[team=red]> = 0;

// All-player scoped variables
var num allPlayerCounter scope<@a> = 0;
```

**Key Points:**
- Variables default to `@s` (the executing entity) for player-specific data
- Use `scope<global>` for server-wide variables stored on the `mdl_server` armor stand
- You can scope to any valid Minecraft selector like `@a[team=red]`
- Be careful with broad selectors like `@a` or `@e` as they may affect multiple entities

### Variable Substitution

Use `$variable_name$` to substitute variables in commands. For scoped variables, use `$variable_name<selector>$`:

```mdl
// Basic variable substitution
say Player health: $player_health$;
tellraw @a {"text":"Score: $score$","color":"gold"};

// Scoped variable substitution
say Your health: $player_health<@s>$;
tellraw @a {"text":"Global timer: $global_timer<global>$","color":"blue"};
tellraw @a {"text":"Team score: $team_score<@a[team=red]>$","color":"red"};
```

### Control Structures

MDL supports real if/else statements and while loops:

```mdl
// Basic conditions
if "$health$ < 10" {
    say Health is low!;
    effect give @s minecraft:regeneration 10 1;
} else {
    say Health is good;
}

// Scoped variable conditions
if "$player_health<@s>$ < 5" {
    say Your health is critical!;
    effect give @s minecraft:regeneration 10 2;
}

if "$global_timer<global>$ > 200" {
    say Global timer is high!;
    global_timer<global> = 0;
}

// While loops with scoped variables
while "$counter$ < 5" {
    say Counter: $counter$;
    counter = counter + 1;
}

while "$global_timer<global>$ > 0" {
    global_timer<global> = global_timer<global> - 1;
    say Reducing timer: $global_timer<global>$;
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
- **`