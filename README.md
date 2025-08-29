# <img src="https://github.com/aaron777collins/MinecraftDatapackLanguage/raw/main/icons/icon-128.png" width="32" height="32" alt="MDL Icon"> Minecraft Datapack Language (MDL)

A **simplified** compiler that lets you write Minecraft datapacks in a modern JavaScript-style language (`.mdl`) with **control structures and number variables** that actually work.

📖 **[View Full Documentation](https://aaron777collins.github.io/MinecraftDatapackLanguage/)** - Complete guides, examples, and API reference  
📦 **[View on PyPI](https://pypi.org/project/minecraft-datapack-language/)** - Download and install from PyPI  
🔧 **[VS Code Extension](https://marketplace.visualstudio.com/items?itemName=mdl.minecraft-datapack-language)** - Syntax highlighting, IntelliSense, and snippets

![CI](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/CI/badge.svg)
![Test Examples](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Test%20Examples/badge.svg)
![Documentation](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Build%20and%20Deploy%20Documentation/badge.svg)
![PyPI](https://img.shields.io/pypi/v/minecraft-datapack-language?style=flat-square)
![Release](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Release/badge.svg)

## 🎯 **SIMPLIFIED** JavaScript-Style MDL Language

**MDL uses a simplified JavaScript-style language format** focused on **control structures and number variables**:

### ✨ **SIMPLIFIED** Features
- **🎯 JavaScript-style syntax** with curly braces `{}` and semicolons `;`
- **📝 Modern comments** using `//` and `/* */`
- **🔢 Number variables only** with `var num` type (stored in scoreboards)
- **🔄 Control structures** including `if/else`, `while`, `for` loops
- **💲 Variable substitution** with `$variable$` syntax
- **📦 Namespace system** for modular code organization
- **🎨 VS Code extension** with full IntelliSense and snippets
- **🧪 Comprehensive testing** with E2E validation
- **📚 Extensive documentation** with examples for every feature

### 🏗️ Core Features
- ✅ Handles the directory renames from snapshots **24w19a** (tag subfolders) and **24w21a** (core registry folders)
- ✅ Easy hooks into `minecraft:tick` and `minecraft:load` via function tags
- ✅ Creates tags for `function`, `item`, `block`, `entity_type`, `fluid`, and `game_event`
- ✅ **Control structures** that actually work - `if/else`, `while`, `for` loops
- ✅ **Number variables** stored in scoreboards with `$variable$` substitution
- ✅ **Multi-file projects** with automatic merging and dependency resolution
- ✅ **Simple expressions** with basic arithmetic operations

> **Note**: Version 10 uses **pack_format 82** by default for the modern JavaScript-style syntax.

---

## 🚀 Install

### Option A — from PyPI (recommended for users)
Global, isolated CLI via **pipx**:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath    # reopen terminal
pipx install minecraft-datapack-language

mdl --help
```

Virtualenv (if you prefer):
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install minecraft-datapack-language
```

### Option B — from source (for contributors)
```bash
# inside the repo
python -m pip install -e .
```

---

## 🔄 Update

- **pipx**: `pipx upgrade minecraft-datapack-language`  
- **pip (venv)**: `pip install -U minecraft-datapack-language`  
- Pin a version: `pipx install "minecraft-datapack-language==10.0.0"`

---

## 💻 CLI

### Modern JavaScript-style MDL (v10)
```bash
# Create a new v10 project
mdl new my_pack --name "My Pack" --pack-format 82

# Build JavaScript-style MDL files
mdl build --mdl my_pack/mypack.mdl -o dist --wrapper mypack
mdl check my_pack/mypack.mdl

# Validate generated mcfunction files
mdl check-advanced my_pack/mypack.mdl

# Multi-file projects
mdl build --mdl my_pack/ -o dist      # Build entire directory
mdl build --mdl "file1.mdl file2.mdl" -o dist  # Build specific files
```

### Comments in MDL
MDL supports modern JavaScript-style comments:
```javascript
// Single-line comments
/* Multi-line comments */

pack "My Pack" {
    function example() {
        // This comment will be properly converted to mcfunction
        say Hello World!
    }
}
```

Generated mcfunction files will have proper `#` comments:
```mcfunction
# This is a generated comment
say Hello World!
```

### Build a whole folder of `.mdl` files
```bash
mdl build --mdl src/ -o dist
# Recursively parses src/**/*.mdl, merges into one pack (errors on duplicate functions).
# Only the first file should have a pack declaration - all others are modules.
```

### Build multiple specific `.mdl` files
```bash
mdl build --mdl "src/core.mdl src/features.mdl src/ui.mdl" -o dist
# Parses multiple specific files and merges them into one datapack.
# Only the first file should have a pack declaration - all others are modules.
```

### Validate a folder (JSON diagnostics)
```bash
mdl check --json src/
```

---

## 📝 Quick Start - **SIMPLIFIED** MDL

Create your first simplified MDL project:

```mdl
// simple_pack.mdl
pack "Simple Pack" description "A simple example" pack_format 82;

namespace "example";

// Number variables only
var num counter = 0;
var num health = 20;
var num level = 1;

function "init" {
    say Initializing...;
    counter = 0;
    health = 20;
    level = 1;
}

function "tick" {
    counter = counter + 1;
    
    // Variable substitution in conditions
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
    }
    
    // Variable substitution in strings
    say Counter: $counter$;
    
    // While loop
    while "$counter$ < 10" {
        counter = $counter$ + 1;
        say Counter: $counter$;
    }
    
    // For loop (entity iteration)
    for player in @a {
        say Hello $player$;
    }
}

// Lifecycle hooks
on_load "example:init";
on_tick "example:tick";
```

Build and test:
```bash
mdl build --mdl simple_pack.mdl -o dist
# → dist/simple_pack/... and dist/simple_pack.zip
```

---

## 📁 Multi-file Support

MDL supports building datapacks from multiple `.mdl` files. This is useful for organizing large projects into logical modules.

### How it works
- **Directory scanning**: When you pass a directory to `--mdl`, MDL recursively finds all `.mdl` files
- **File merging**: Each file is parsed into a `Pack` object, then merged into a single datapack
- **Conflict resolution**: Duplicate function names within the same namespace will cause an error
- **Pack metadata**: Only the **first file** should have a pack declaration (name, description, format)
- **Module files**: Subsequent files should **not** have pack declarations - they are treated as modules
- **Single file compilation**: When compiling a single file, it **must** have a pack declaration

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

### Complete Multi-File Example

Here's a complete example showing how to organize a datapack across multiple files:

**`core.mdl`** (main file with pack declaration):
```mdl
// core.mdl - Main pack and core systems
pack "Adventure Pack" description "Multi-file example datapack" pack_format 82;

namespace "core";

// Number variables only
var num system_version = 1;
var num player_count = 0;

function "init" {
    say [core:init] Initializing Adventure Pack...;
    tellraw @a {"text":"Adventure Pack loaded!","color":"green"};
    system_version = 1;
    player_count = 0;
}

function "tick" {
    say [core:tick] Core systems running...;
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1;
    player_count = player_count + 1;
}

// Hook into vanilla lifecycle
on_load "core:init";
on_tick "core:tick";
```

**`combat/weapons.mdl`** (combat module):
```mdl
// combat/weapons.mdl - Weapon-related functions
namespace "combat";

var num weapon_damage = 10;

function "weapon_effects" {
    say [combat:weapon_effects] Applying weapon effects...;
    execute as @a[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 1 0 true;
    weapon_damage = weapon_damage + 2;
}

function "update_combat" {
    function core:tick;
    function combat:weapon_effects;
}
```

**`combat/armor.mdl`** (armor module):
```mdl
// combat/armor.mdl - Armor-related functions
namespace "combat";

var num armor_bonus = 5;

function "armor_bonus" {
    say [combat:armor_bonus] Checking armor bonuses...;
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] run effect give @s minecraft:resistance 1 0 true;
    armor_bonus = armor_bonus + 1;
}

function "update_armor" {
    function combat:armor_bonus;
}
```

**`ui/hud.mdl`** (UI module):
```mdl
// ui/hud.mdl - User interface functions
namespace "ui";

var num hud_version = 1;

function "show_hud" {
    say [ui:show_hud] Updating HUD...;
    title @a actionbar {"text":"Adventure Pack Active","color":"gold"};
    hud_version = hud_version + 1;
}

function "update_ui" {
    function ui:show_hud;
    function combat:update_combat;
    function combat:update_armor;
}
```

**Project structure:**
```
adventure_pack/
├── core.mdl              # ✅ HAS pack declaration
├── combat/
│   ├── weapons.mdl       # ❌ NO pack declaration (module)
│   └── armor.mdl         # ❌ NO pack declaration (module)
└── ui/
    └── hud.mdl           # ❌ NO pack declaration (module)
```

**Build the project:**
```bash
mdl build --mdl adventure_pack/ -o dist --verbose
```

This will create a datapack with:
- **Core systems** (initialization and tick functions)
- **Combat features** (weapon and armor effects)
- **UI elements** (HUD display)
- **Cross-module calls** (UI calls combat functions)

### CLI Options for Multi-file Builds

- `--mdl <path>`: Path to `.mdl` file, directory, or space-separated file list
- `--src <path>`: Alias for `--mdl` (same functionality)
- `-o, --out <dir>`: Output directory for the built datapack
- `--wrapper <name>`: Custom wrapper folder/zip name (default: first namespace or pack name slug)
- `--pack-format <N>`: Minecraft pack format (default: 82 for modern syntax)
- `-v, --verbose`: Show detailed processing information including file merging
- `--py-module <path>`: Alternative: build from Python module with `create_pack()` function

### Error Handling

- **Missing pack declaration**: Single files must have a pack declaration
- **Duplicate pack declarations**: Only the first file in a multi-file project should have a pack declaration
- **Function conflicts**: Duplicate function names within the same namespace will cause an error
- **Clear error messages**: Errors include file paths and line numbers for easy debugging

---

## 📝 The **SIMPLIFIED** `.mdl` Language

### Grammar you can rely on (based on the parser)
- **pack header** (required once):
  ```mdl
  pack "Name" [description "Desc"] [pack_format N];
  ```
- **namespace** (selects a namespace for following blocks):
  ```mdl
  namespace "example";
  ```
- **number variable declarations** (only `num` type supported):
  ```mdl
  var num counter = 0;
  var num health = 20;
  var num level = 1;
  ```
- **function** (curly braces + semicolons):
  ```mdl
  function "hello" {
      say hi;
      tellraw @a {"text":"ok","color":"green"};
  }
  ```
- **conditional blocks** (if/else if/else statements):
  ```mdl
  function "conditional" {
      if "$health$ < 10" {
          say Health is low!;
          effect give @s minecraft:glowing 5 1;
      } else if "$level$ > 5" {
          say High level player!;
          effect give @s minecraft:speed 5 1;
      } else {
          say Normal player;
      }
  }
  ```
- **while loops** (repetitive execution):
  ```mdl
  function "countdown" {
      var num counter = 5;
      while "$counter$ > 0" {
          say Counter: $counter$;
          counter = counter - 1;
      }
  }
  ```
- **for loops** (entity iteration):
  ```mdl
  function "player_effects" {
      for player in @a {
          say Processing player: @s;
          effect give @s minecraft:speed 10 1;
      }
  }
  ```
- **function calls** (one function invoking another with fully qualified ID):
  ```mdl
  function "outer" {
      say I will call another function;
      function example:hello;
  }
  ```
- **hooks** (namespaced ids required):
  ```mdl
  on_load "example:hello";
  on_tick "example:hello";
  ```
- **tags** (supported registries: `function`, `item`, `block`, `entity_type`, `fluid`, `game_event`):
  ```mdl
  tag function "minecraft:tick" {
      add "example:hello";
  }
  ```
- **comments** start with `//` or `/* */`. Hashes inside **quoted strings** are preserved.
- **whitespace**: empty lines are ignored; **explicit block boundaries** using curly braces `{` and `}`; **statement termination** using semicolons `;`.

> Inside a function block, **every non-empty line** is emitted almost verbatim as a Minecraft command. Comments are stripped out and multi-line commands are automatically wrapped. See below for details.

### Comments

MDL supports modern JavaScript-style comments:

- **Full-line comments** (a line starting with `//`) are ignored by the parser.
- **Block comments** (`/* */`) are supported for multi-line comments.
- **Inline `#` characters** are preserved inside function bodies, so you can still use them the way `mcfunction` normally allows.

Example:

```mdl
// Comment Demo - Testing comments
pack "Comment Demo" description "Testing comments";

namespace "demo";

function "comments" {
    // This whole line is ignored by MDL
    say Hello; // This inline comment is preserved
    tellraw @a {"text":"World","color":"blue"}; // Inline too!
    
    /* This is a block comment
       that spans multiple lines
       and is ignored by the parser */
}
```

When compiled, the resulting function looks like:

```mcfunction
say Hello # This inline comment is preserved
tellraw @a {"text":"World","color":"blue"} # Inline too!
```

Notice how the full-line `//` and block comments never make it into the `.mcfunction`, but the inline ones do.

---

### **SIMPLIFIED** Variables and Data Types

MDL supports **number variables only** for simplicity and reliability:

#### Number Variables (`num`)
```mdl
var num counter = 0;
var num health = 20;
var num experience = 100;

// Arithmetic operations
counter = counter + 1;
health = health - 5;
experience = experience * 2;

// Variable substitution in strings
say Health: $health$;
say Experience: $experience$;
```

**Variable Substitution**: Use `$variable_name$` to read values from scoreboards in strings and conditions.

### **SIMPLIFIED** Control Flow

MDL supports conditional blocks and loops for control flow.

#### Conditional Blocks

MDL supports if/else if/else statements for conditional execution:

```mdl
function "conditional_example" {
    var num player_level = 15;
    var num player_health = 8;
    
    if "$player_level$ >= 10" {
        if "$player_health$ < 10" {
            say Advanced player with low health!;
            effect give @s minecraft:regeneration 10 1;
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
```

**Rules:**
- Conditions use `$variable$` syntax for variable substitution
- **Explicit block boundaries**: Conditional blocks use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- You can have multiple `else if` blocks
- The `else` block is optional
- Conditional blocks are compiled to separate functions and called with `execute` commands
- **Proper logic**: `else if` blocks only execute if previous conditions were false

#### While Loops

MDL supports while loops for repetitive execution:

```mdl
function "while_example" {
    var num counter = 5;
    while "$counter$ > 0" {
        say Counter: $counter$;
        counter = counter - 1;
        say Decremented counter;
    }
}
```

**Rules:**
- Conditions use `$variable$` syntax for variable substitution
- **Explicit block boundaries**: While loops use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- While loops continue until the condition becomes false
- **Important**: Ensure your loop body modifies the condition to avoid infinite loops

#### For Loops

MDL supports for loops for iterating over entity collections:

```mdl
function "for_example" {
    for player in @a {
        say Processing player: @s;
        effect give @s minecraft:speed 10 1;
        tellraw @s {"text":"You got speed!","color":"green"};
    }
}
```

**Rules:**
- Collection must be a valid Minecraft entity selector
- **Explicit block boundaries**: For loops use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- For loops iterate over each entity in the collection
- **Efficient execution**: Each conditional block becomes a separate function for optimal performance

---

### Multi-line Commands

Long JSON commands can be split across multiple lines with a trailing backslash `\`.  
MDL will join them back together before writing the final `.mcfunction`.

Example:

```mdl
// Multi-line Demo
pack "Multi-line Demo";

namespace "demo";

function "multiline" {
    tellraw @a \
        {"text":"This text is really, really long so we split it",\
         "color":"gold"};
}
```

When compiled, the function is a single line:

```mcfunction
tellraw @a {"text":"This text is really, really long so we split it","color":"gold"}
```

---

## 🎯 **SIMPLIFIED** example (control structures + number variables)

```mdl
// simple_pack.mdl - simplified example for Minecraft Datapack Language
pack "Simple Pack" description "Simplified example datapack" pack_format 82;

namespace "example";

// Number variables only
var num counter = 0;
var num health = 20;
var num level = 1;

function "inner" {
    say [example:inner] This is the inner function;
    tellraw @a {"text":"Running inner","color":"yellow"};
    counter = counter + 1;
}

function "hello" {
    say [example:hello] Outer says hi;
    function example:inner;
    tellraw @a {"text":"Back in hello","color":"aqua"};
    
    // Variable operations
    health = health + 5;
    level = level + 1;
    
    // Variable substitution
    say Health: $health$;
    say Level: $level$;
    
    // Control structures
    if "$health$ > 15" {
        say High health!;
        effect give @s minecraft:strength 10 1;
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

// Hook the function into load and tick
on_load "example:hello";
on_tick "example:hello";

// Second namespace with a cross-namespace call
namespace "util";

var num helper_count = 0;

function "helper" {
    say [util:helper] Helping out...;
    helper_count = helper_count + 1;
    say Helper count: $helper_count$;
}

function "boss" {
    say [util:boss] Calling example:hello then util:helper;
    function example:hello;
    function util:helper;
}

// Run boss every tick as well
on_tick "util:boss";

// Function tag examples
tag function "minecraft:load" {
    add "example:hello";
}

tag function "minecraft:tick" {
    add "example:hello";
    add "util:boss";
}

// Data tag examples across registries
tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

tag block "example:glassy" {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
```

### What this demonstrates
- **Nested-like function composition** (`function example:inner` inside `function "hello"`).
- **Multiple namespaces** (`example`, `util`) calling each other with fully-qualified IDs.
- **Lifecycle hooks** (`on_load`, `on_tick`) on both `example:hello` and `util:boss`.
- **Function tags** to participate in vanilla tags (`minecraft:load`, `minecraft:tick`).
- **Data tags** (`item`, `block`) in addition to function tags.
- **Number variables** with `$variable$` substitution.
- **Control structures** that actually work - `if/else`, `while`, `for` loops.
- **Modern syntax** with curly braces and semicolons.

---

## 🐍 Python API equivalent

```python
from minecraft_datapack_language import Pack

def build_pack():
    p = Pack(name="Simple Pack",
             description="Simplified example datapack",
             pack_format=82)

    ex = p.namespace("example")
    ex.function("inner",
        'say [example:inner] This is the inner function',
        'tellraw @a {"text":"Running inner","color":"yellow"}'
    )
    ex.function("hello",
        'say [example:hello] Outer says hi',
        'function example:inner',
        'tellraw @a {"text":"Back in hello","color":"aqua"}'
    )

    # Hooks for example namespace
    p.on_load("example:hello")
    p.on_tick("example:hello")

    util = p.namespace("util")
    util.function("helper",
        'say [util:helper] Helping out...'
    )
    util.function("boss",
        'say [util:boss] Calling example:hello then util:helper',
        'function example:hello',
        'function util:helper'
    )

    # Tick hook for util namespace
    p.on_tick("util:boss")

    # Function tags
    p.tag("function", "minecraft:load", values=["example:hello"])
    p.tag("function", "minecraft:tick", values=["example:hello", "util:boss"])

    # Data tags
    p.tag("item",  "example:swords", values=["minecraft:diamond_sword", "minecraft:netherite_sword"])
    p.tag("block", "example:glassy", values=["minecraft:glass", "minecraft:tinted_glass"])

    return p
```

Build it:
```bash
python - <<'PY'
from my_pack_module import build_pack
from minecraft_datapack_language.cli import main as M
# write to dist/ with a wrapper folder name 'mypack'
p = build_pack()
M(['build', '--py-object', 'my_pack_module:build_pack', '-o', 'dist', '--wrapper', 'mypack', '--pack-format', '82'])
PY
```

---

## 🔧 Development System

MDL includes a comprehensive development system that allows you to work with both stable and development versions simultaneously.

### Quick Setup

**Linux/macOS:**
```bash
./scripts/dev_setup.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\dev_setup.ps1
```

### Development Commands

- **`mdl`** - Stable, globally installed version
- **`mdlbeta`** - Local development version for testing changes

### Development Workflow

1. **Make changes** to the code
2. **Rebuild** the development version:
   ```bash
   ./scripts/dev_build.sh
   ```
3. **Test** your changes with `mdlbeta`:
   ```bash
   mdlbeta build --mdl your_file.mdl -o dist
   ```
4. **Compare** with stable version:
   ```bash
   mdl build --mdl your_file.mdl -o dist_stable
   ```

### Testing

**Test the development environment:**
```bash
# Linux/macOS
./scripts/test_dev.sh

# Windows (PowerShell)
.\scripts\test_dev.ps1
```

For more details, see [DEVELOPMENT.md](DEVELOPMENT.md).

## 🔧 VS Code Extension

Get syntax highlighting, linting, and build commands for `.mdl` files in VS Code, Cursor, and other VS Code-based editors.

### Quick Install

1. **Download from [GitHub Releases](https://github.com/aaron777collins/MinecraftDatapackLanguage/releases)**
2. **Install the `.vsix` file**:
   - Open VS Code/Cursor
   - Go to Extensions (Ctrl+Shift+X)
   - Click "..." → "Install from VSIX..."
   - Choose the downloaded `.vsix` file

### Features
- **Syntax highlighting** for `.mdl` files
- **Real-time linting** with error detection
- **Build commands**: `MDL: Build current file` and `MDL: Check Workspace`
- **Workspace validation** for multi-file projects

### Development Setup
```bash
cd vscode-extension/
npm i
# Press F5 to launch the Extension Dev Host
```

---

## 🚀 CI & Releases

- **CI** runs on push/PR across Linux/macOS/Windows and uploads artifacts.
- **Release** is triggered by pushing a tag like `v1.0.0` or via the Release workflow manually.
- Versions are derived from git tags via **setuptools-scm**; tag `vX.Y.Z` → package version `X.Y.Z`.

### Local release helper
```bash
# requires GitHub CLI: gh auth login
./scripts/release.sh patch  "Fixes"
./scripts/release.sh minor  "Features"
./scripts/release.sh major  "Breaking"
./scripts/release.sh v1.2.3 "Exact version"
```
