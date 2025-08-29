---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

# Getting Started

This guide will help you install Minecraft Datapack Language (MDL) and create your first **modern JavaScript-style** datapack with control structures, variables, expressions, and multi-file projects.

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
- **Pin a version**: `pipx install "minecraft-datapack-language==12.0.1"`

## Your First **Modern** Datapack

Let's create a modern datapack that demonstrates **control structures, variables, expressions, and multi-file projects**.

### 1. Create the MDL File

Create a file called `hello.mdl` with the following content:

```mdl
// hello.mdl - Your first modern MDL datapack
pack "Hello World" description "A modern example datapack" pack_format 82;

namespace "hello";

// Number variables with expressions
var num counter = 0;
var num health = 20;
var num level = 1;

function "init" {
    say [hello:init] Initializing Hello World datapack...;
    tellraw @a {"text":"Hello World datapack loaded!","color":"green"};
    counter = 0;
    health = 20;
    level = 1;
}

function "tick" {
    counter = counter + 1;
    
    // Full if/else if/else control structure
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
        effect give @a minecraft:regeneration 10 1;
    } else if "$level$ > 5" {
        say High level player!;
        effect give @a minecraft:strength 10 1;
    } else {
        say Normal player;
        effect give @a minecraft:speed 10 0;
    }
    
    // Variable substitution in strings
    say Counter: $counter$;
    
    // While loop with method selection
    while "$counter$ < 10" {
        counter = $counter$ + 1;
        say Counter: $counter$;
    }
    
    // Expressions with arithmetic
    var num experience = $level$ * 100 + $counter$;
    say Experience: $experience$;
}

// Lifecycle hooks
on_load "hello:init";
on_tick "hello:tick";
```

### 2. Build the Datapack

Run the following command to build your datapack:

```bash
mdl build --mdl hello.mdl -o dist
```

This will create a `dist/` folder containing your compiled datapack.

### 3. Install in Minecraft

1. Copy the `dist/hello_world/` folder to your Minecraft world's `datapacks/` folder
2. In Minecraft, run `/reload` to load the datapack
3. You should see the initialization message and the tick function will start running

### 4. What This Demonstrates

This simple example shows:

- **🎯 JavaScript-style syntax**: Curly braces `{}` and semicolons `;`
- **📝 Modern comments**: Using `//` for single-line comments
- **🔢 Variables**: Number variables with `var num` declarations
- **🔄 Control structures**: Full `if/else if/else` statements
- **🔄 Loops**: `while` loops with method selection
- **💲 Variable substitution**: Using `$variable$` syntax in strings and conditions
- **🧮 Expressions**: Arithmetic operations with variables
- **🎯 Selector optimization**: Proper `@a` usage for system commands
- **🎨 Variable optimization**: Automatic load function generation
- **📦 Multi-file support**: Organize code across multiple files with namespaces

## Multi-File Project Example

Let's create a more complex project using multiple files:

### 1. Create Multiple MDL Files

**`core.mdl`** - Core game logic:
```mdl
pack "multi_example" "A multi-file example" 82;

namespace "core";

var num player_count = 0;
var num game_timer = 0;

function "init" {
    say [core:init] Initializing multi-file system...;
    player_count = 0;
    game_timer = 0;
}

function "tick" {
    game_timer = $game_timer$ + 1;
    say [core:tick] Game timer: $game_timer$;
}

on_load "core:init";
on_tick "core:tick";
```

**`ui.mdl`** - User interface:
```mdl
namespace "ui";

var num menu_state = 0;

function "init" {
    say [ui:init] Initializing UI...;
    menu_state = 0;
}

function "show_menu" {
    if "$menu_state$ == 0" {
        say "=== Main Menu ===";
    }
}

on_load "ui:init";
on_tick "ui:show_menu";
```

### 2. Build the Multi-File Project

```bash
mdl build --mdl . -o dist
```

This creates a datapack with:
- **Separate namespaces**: `core` and `ui` functions are in different directories
- **Merged variables**: All variables are initialized together
- **Combined hooks**: All load and tick functions are properly organized

### 3. Generated Structure

```
dist/
├── data/
│   ├── minecraft/tags/function/
│   │   ├── load.json    # Contains core:init, ui:init
│   │   └── tick.json    # Contains core:tick, ui:show_menu
│   ├── core/            # core.mdl namespace
│   │   └── function/
│   │       ├── init.mcfunction
│   │       └── tick.mcfunction
│   └── ui/              # ui.mdl namespace
│       └── function/
│           ├── init.mcfunction
│           └── show_menu.mcfunction
└── pack.mcmeta
```

## Next Steps

Now that you have a basic understanding, explore:

- **[Language Reference]({{ site.baseurl }}/docs/language-reference/)** - Complete syntax guide
- **[Examples]({{ site.baseurl }}/docs/examples/)** - More complex examples
- **[Multi-file Projects]({{ site.baseurl }}/docs/multi-file-projects/)** - Organizing large datapacks
- **[VS Code Extension]({{ site.baseurl }}/docs/vscode-extension/)** - IDE integration

## Troubleshooting

### Common Issues

**"mdl command not found"**
- Make sure you've installed MDL correctly
- Try restarting your terminal
- Check that pipx is in your PATH

**"Pack format not supported"**
- Use `pack_format 82` for modern Minecraft versions
- Older versions may need lower pack formats

**"Function not found"**
- Make sure function names are quoted: `function "name"`
- Check that namespaces are properly declared
- Verify hook syntax: `on_load "namespace:function"`

**"Variable not found"**
- Declare variables with `var num name = value;`
- Use `$variable$` syntax for substitution
- Variables are automatically optimized in load functions

### Getting Help

- **GitHub Issues**: [Report bugs and request features](https://github.com/aaron777collins/MinecraftDatapackLanguage/issues)
- **GitHub Discussions**: [Ask questions and share your datapacks](https://github.com/aaron777collins/MinecraftDatapackLanguage/discussions)
- **Documentation**: Check the [Language Reference]({{ site.baseurl }}/docs/language-reference/) for complete syntax details
