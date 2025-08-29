---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

# Getting Started

This guide will help you install Minecraft Datapack Language (MDL) and create your first **simplified** datapack with control structures and number variables.

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

### Development System Setup

MDL includes a comprehensive development system for contributors:

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
2. Run `./scripts/dev_build.sh` to rebuild the development version
3. Test with `mdlbeta build --mdl your_file.mdl -o dist`
4. Compare with `mdl build --mdl your_file.mdl -o dist_stable`

For detailed development information, see [DEVELOPMENT.md](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/DEVELOPMENT.md).

## Updating MDL

- **pipx**: `pipx upgrade minecraft-datapack-language`
- **pip**: `pip install -U minecraft-datapack-language`
- **Pin a version**: `pipx install "minecraft-datapack-language==1.1.0"`

## Your First **Simplified** Datapack

Let's create a simple datapack that demonstrates **control structures and number variables**.

### 1. Create the MDL File

**Option A: Use the `mdl new` command (Recommended)**
```bash
mdl new hello --name "My First Pack"
```
This creates a complete template with modern pack format 82+ metadata.

**Option B: Create manually**
Create a file called `hello.mdl` with the following content:

```mdl
// hello.mdl - My first simplified datapack
pack "My First Pack" description "A simple example datapack" pack_format 82;

namespace "example";

// Number variables only
var num counter = 0;
var num health = 20;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    
    // Variable substitution
    say Counter: $counter$;
    say Health: $health$;
    
    // Control structures
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
    }
    
    while "$counter$ < 5" {
        say Counter: $counter$;
        counter = counter + 1;
    }
    
    for player in @a {
        say Hello $player$;
        effect give @s minecraft:speed 5 0;
    }
}

// Hook the function to run when the world loads
on_load "example:hello";
```

**Important**: Every MDL project must have a file starting with the `pack` declaration when compiled individually. This tells MDL the name, description, and format of your datapack. If you are compiling multiple MDL files together, you only need 1 file to define the pack info.

### 2. Build the Datapack

```bash
mdl build --mdl hello.mdl -o dist
```

This will create a `dist/` folder containing your compiled datapack.

### 3. Install in Minecraft

1. Open your Minecraft world
2. Navigate to the world's `datapacks` folder:
   - **Singleplayer**: `.minecraft/saves/[WorldName]/datapacks/`
   - **Multiplayer**: Copy to the server's `world/datapacks/` folder
3. Copy the folder from `dist/` to the datapacks folder
4. In-game, run `/reload` to load the datapack
5. You should see the welcome message and control structures working!

## Understanding the **Simplified** Code

Let's break down what we just created:

- **`pack "My First Pack"`**: Declares the datapack name and metadata
- **`pack_format 82`**: Specifies compatibility with Minecraft 1.21.4+
- **`namespace "example"`**: Creates a namespace for organizing functions
- **`var num counter = 0`**: Declares a number variable stored in scoreboard
- **`$counter$`**: Variable substitution - reads value from scoreboard
- **`function "hello":`**: Defines a function that contains Minecraft commands
- **`on_load "example:hello"`**: Automatically runs the function when the world loads

## **Simplified** Control Flow

MDL supports **control structures and number variables** for reliable datapack development.

### Number Variables

MDL supports **number variables only** for simplicity and reliability:

```mdl
// Number variables
var num counter = 0;
var num health = 20;
var num level = 1;

// Variable substitution in strings
say Health: $health$;
say Level: $level$;

// Arithmetic operations
counter = counter + 1;
health = health - 5;
level = level * 2;
```

**Variable Substitution**: Use `$variable_name$` to read values from scoreboards in strings and conditions.

### Conditional Logic

Let's create an example that uses conditional blocks with number variables:

```mdl
// conditional.mdl - Conditional logic example
pack "Conditional Demo" description "Shows if/else if/else functionality" pack_format 82;

namespace "demo";

// Number variables
var num player_level = 15;
var num player_health = 8;

function "check_player" {
    if "$player_level$ >= 10" {
        if "$player_health$ < 10" {
            say Advanced player with low health!;
            effect give @s minecraft:regeneration 10 1;
            player_health = player_health + 5;
        } else {
            say Advanced player with good health;
            effect give @s minecraft:strength 10 1;
        }
    } else if "$player_level$ >= 5" {
        say Intermediate player;
        effect give @s minecraft:speed 10 0;
    } else {
        say Beginner player;
        effect give @s minecraft:jump_boost 10 0;
    }
}

// Run the detection every tick
on_tick "demo:check_player";
```

This example demonstrates:
- **`if "$variable$ condition"`** - Checks if the condition is true using variable substitution
- **`else if "$variable$ condition"`** - Checks another condition if the first was false
- **`else:`** - Runs if none of the above conditions were true
- **Variable substitution** - `$player_level$` and `$player_health$` read from scoreboards

### While Loops

While loops allow you to repeat commands until a condition becomes false:

```mdl
// loops.mdl - Loop examples
pack "Loop Demo" description "Shows while and for loop functionality" pack_format 82;

namespace "demo";

var num counter = 5;

function "countdown" {
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter = counter - 1;
        say Decremented counter;
    }
}

function "health_regeneration" {
    var num regen_count = 0;
    while "$regen_count$ < 3" {
        say Regenerating health...;
        effect give @s minecraft:regeneration 5 0;
        regen_count = regen_count + 1;
    }
}

// Run the loops every tick
on_tick "demo:countdown";
on_tick "demo:health_regeneration";
```

**Important**: Always ensure your while loop body modifies the condition to avoid infinite loops!

### For Loops

For loops allow you to iterate over collections of entities:

```mdl
function "player_effects" {
    for player in @a {
        say Processing player: @s;
        effect give @s minecraft:speed 10 1;
        tellraw @s {"text":"You got speed!","color":"green"};
    }
}

function "item_processing" {
    for item in @e[type=minecraft:item] {
        say Processing item: @s;
        effect give @s minecraft:glowing 5 1;
    }
}

// Run the for loops every tick
on_tick "demo:player_effects";
on_tick "demo:item_processing";
```

For loops are perfect for applying effects to multiple entities or processing collections of items.

## Next Steps

Now that you have the basics, explore:

- **[Language Reference]({{ site.baseurl }}/docs/language-reference/)** - Learn the complete **simplified** MDL syntax
- **[Examples]({{ site.baseurl }}/docs/examples/)** - See more complex examples (all tested and verified!)
- **[CLI Reference]({{ site.baseurl }}/docs/cli-reference/)** - Master the command-line tools
- **[VS Code Extension]({{ site.baseurl }}/docs/vscode-extension/)** - Get syntax highlighting and linting

### Want to See Working Examples?

All examples in the documentation are thoroughly tested and available for download. Check out the **[Tested Examples]({{ site.baseurl }}/docs/examples/#tested-examples)** section for direct links to working MDL and Python API files.

## Troubleshooting

### "mdl command not found"

If you get a "command not found" error after installation:

1. **pipx users**: Make sure you ran `python3 -m pipx ensurepath` and restarted your terminal
2. **pip users**: Make sure your virtual environment is activated
3. **Windows users**: Try using `python -m minecraft_datapack_language.cli` instead of `mdl`

### Build Errors

If you get build errors:

1. Check that your MDL syntax is correct (see [Language Reference]({{ site.baseurl }}/docs/language-reference/))
2. Make sure you have a `pack` declaration at the top of your file
3. Verify that function names are unique within each namespace
4. Use `mdl check hello.mdl` to validate your file before building
5. Remember: **only number variables** are supported (`var num`)

### Datapack Not Working

If your datapack doesn't work in Minecraft:

1. Make sure you copied the entire folder from `dist/` to the datapacks directory
2. Run `/reload` in-game to reload datapacks
3. Check the game logs for error messages
4. Verify that your pack_format is compatible with your Minecraft version
5. Check that variable substitutions (`$variable$`) are working correctly
