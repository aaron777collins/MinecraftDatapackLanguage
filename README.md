# <img src="https://github.com/aaron777collins/MinecraftDatapackLanguage/raw/main/icons/icon-128.png" width="32" height="32" alt="MDL Icon"> Minecraft Datapack Language (MDL)

A powerful compiler that lets you write Minecraft datapacks in a modern JavaScript-style language (`.mdl`) or via a clean Python API, and then compiles to the correct 1.21+ datapack folder layout automatically.

📖 **[View Full Documentation](https://aaron777collins.github.io/MinecraftDatapackLanguage/)** - Complete guides, examples, and API reference  
📦 **[View on PyPI](https://pypi.org/project/minecraft-datapack-language/)** - Download and install from PyPI  
🔧 **[VS Code Extension](https://marketplace.visualstudio.com/items?itemName=mdl.minecraft-datapack-language)** - Syntax highlighting, IntelliSense, and snippets

![CI](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/CI/badge.svg)
![Test Examples](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Test%20Examples/badge.svg)
![Documentation](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Build%20and%20Deploy%20Documentation/badge.svg)
![PyPI](https://img.shields.io/pypi/v/minecraft-datapack-language?style=flat-square)
![Release](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Release/badge.svg)

## 🎯 Modern JavaScript-Style MDL Language

**MDL uses a modern JavaScript-style language format** with advanced programming features:

### ✨ Modern Features
- **🎯 JavaScript-style syntax** with curly braces `{}` and semicolons `;`
- **📝 Modern comments** using `//` and `/* */`
- **🔢 Variable system** with `num`, `str`, and `list` types
- **🔄 Advanced control flow** including `if/else`, `while`, `for`, `switch`, `try-catch`, `break`, `continue`
- **📦 Namespace system** for modular code organization
- **🎨 VS Code extension** with full IntelliSense and snippets
- **🧪 Comprehensive testing** with E2E validation
- **📚 Extensive documentation** with examples for every feature

### 🏗️ Core Features
- ✅ Handles the directory renames from snapshots **24w19a** (tag subfolders) and **24w21a** (core registry folders)
- ✅ Easy hooks into `minecraft:tick` and `minecraft:load` via function tags
- ✅ Creates tags for `function`, `item`, `block`, `entity_type`, `fluid`, and `game_event`
- ✅ **Unlimited nesting** support for complex control flow structures
- ✅ **Multi-file projects** with automatic merging and dependency resolution
- ✅ **Error handling** with try-catch blocks and custom error messages
- ✅ **Type system** with number, string, and list variables
- ✅ **Function system** with parameters, return values, and recursion

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

# Multi-file projects
mdl build --mdl my_pack/ -o dist      # Build entire directory
mdl build --mdl "file1.mdl file2.mdl" -o dist  # Build specific files
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

## 📝 Quick Start - Modern JavaScript-style MDL

Create your first modern MDL project:

```mdl
// my_pack.mdl
pack "My First Pack" description "A simple example" pack_format 82;

namespace "example";

// Global variables
var num counter = 0;
var str message = "Hello World";
var list items = ["sword", "shield", "potion"];

function "init" {
    say Initializing...;
    counter = 0;
    message = "Ready!";
    items.append("golden_apple");
}

function "tick" {
    counter = counter + 1;
    
    if "score @s counter matches 10" {
        say Counter reached 10!;
        counter = 0;
    }
    
    for player in @a {
        effect give @s minecraft:speed 1 0;
    }
    
    // List operations
    var num item_count = items.length;
    if "score @s item_count > 5" {
        say Inventory getting full!;
    }
}

// Lifecycle hooks
on_load "example:init";
on_tick "example:tick";
```

Build and test:
```bash
mdl build --mdl my_pack.mdl -o dist
# → dist/my_pack/... and dist/my_pack.zip
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

// Global state
var num system_version = 1;
var str system_status = "online";

function "init" {
    say [core:init] Initializing Adventure Pack...;
    tellraw @a {"text":"Adventure Pack loaded!","color":"green"};
}

function "tick" {
    say [core:tick] Core systems running...;
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1;
}

// Hook into vanilla lifecycle
on_load "core:init";
on_tick "core:tick";
```

**`combat/weapons.mdl`** (combat module):
```mdl
// combat/weapons.mdl - Weapon-related functions
namespace "combat";

function "weapon_effects" {
    say [combat:weapon_effects] Applying weapon effects...;
    execute as @a[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 1 0 true;
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

function "armor_bonus" {
    say [combat:armor_bonus] Checking armor bonuses...;
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] run effect give @s minecraft:resistance 1 0 true;
}

function "update_armor" {
    function combat:armor_bonus;
}
```

**`ui/hud.mdl`** (UI module):
```mdl
// ui/hud.mdl - User interface functions
namespace "ui";

function "show_hud" {
    say [ui:show_hud] Updating HUD...;
    title @a actionbar {"text":"Adventure Pack Active","color":"gold"};
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

## 📝 The Modern `.mdl` Language

### Grammar you can rely on (based on the parser)
- **pack header** (required once):
  ```mdl
  pack "Name" [description "Desc"] [pack_format N] [min_format [major, minor]] [max_format [major, minor]] [min_engine_version "version"];
  ```
- **namespace** (selects a namespace for following blocks):
  ```mdl
  namespace "example";
  ```
- **variable declarations** (with types):
  ```mdl
  var num counter = 0;
  var str message = "Hello";
  var list items = ["sword", "shield"];
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
      if "entity @s[type=minecraft:player]" {
          say Player detected!;
          effect give @s minecraft:glowing 5 1;
      } else if "entity @s[type=minecraft:zombie]" {
          say Zombie detected!;
          effect give @s minecraft:poison 5 1;
      } else {
          say Unknown entity;
      }
  }
  ```
- **while loops** (repetitive execution):
  ```mdl
  function "countdown" {
      var num counter = 5;
      while "score @s counter matches 1.." {
          say Counter: @s counter;
          counter = counter - 1;
      }
  }
  ```
- **for loops** (entity iteration):
  ```mdl
  function "player_effects" {
      for player in @e[type=minecraft:player] {
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

### Variables and Data Types

MDL supports a modern variable system with three data types:

#### Number Variables (`num`)
```mdl
var num counter = 0;
var num health = 20;
var num experience = 100;

// Arithmetic operations
counter = counter + 1;
health = health - 5;
experience = experience * 2;
```

#### String Variables (`str`)
```mdl
var str player_name = "Steve";
var str message = "Hello World";
var str status = "online";

// String concatenation
var str full_message = "Player " + player_name + " is " + status;
```

#### List Variables (`list`)
```mdl
var list items = ["sword", "shield", "potion"];
var list players = ["Alice", "Bob", "Charlie"];

// List operations
items.append("golden_apple");
items.insert(1, "enchanted_sword");
var str first_item = items[0];
var num item_count = items.length;
items.remove("shield");
items.pop();
items.clear();
```

### Control Flow

MDL supports conditional blocks and loops for advanced control flow.

#### Conditional Blocks

MDL supports if/else if/else statements for conditional execution:

```mdl
function "conditional_example" {
    var num player_level = 15;
    var str player_class = "warrior";
    
    if "score @s player_level >= 10" {
        if "score @s player_class == 'warrior'" {
            say Advanced warrior detected!;
            effect give @s minecraft:strength 10 2;
        } else if "score @s player_class == 'mage'" {
            say Advanced mage detected!;
            effect give @s minecraft:night_vision 10 0;
        } else {
            say Unknown advanced class;
        }
    } else if "score @s player_level >= 5" {
        say Intermediate player;
        effect give @s minecraft:speed 10 0;
    } else {
        say Beginner player;
        effect give @s minecraft:jump_boost 10 0;
    }
}
```

**Rules:**
- Conditions must be valid Minecraft selector syntax
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
    while "score @s counter matches 1.." {
        say Counter: @s counter;
        counter = counter - 1;
        say Decremented counter;
    }
}
```

**Rules:**
- Conditions must be valid Minecraft selector syntax
- **Explicit block boundaries**: While loops use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- While loops continue until the condition becomes false
- **Important**: Ensure your loop body modifies the condition to avoid infinite loops

#### For Loops

MDL supports for loops for iterating over entity collections:

```mdl
function "for_example" {
    tag @e[type=minecraft:player] add players;
    for player in @e[tag=players] {
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

#### Break and Continue

MDL supports `break` and `continue` statements in loops:

```mdl
function "break_continue_example" {
    var num counter = 0;
    var num break_sum = 0;
    var num continue_sum = 0;
    
    // Test break
    while "score @s counter < 10" {
        counter = counter + 1;
        
        if "score @s counter == 7" {
            break;
        }
        
        break_sum = break_sum + counter;
    }
    
    // Test continue
    counter = 0;
    while "score @s counter < 10" {
        counter = counter + 1;
        
        if "score @s counter % 2 == 0" {
            continue;
        }
        
        continue_sum = continue_sum + counter;
    }
}
```

### Error Handling

MDL supports try-catch blocks for error handling:

```mdl
function "error_handling_example" {
    var num dividend = 10;
    var num divisor = 0;
    var num result = 0;
    
    try {
        if "score @s divisor != 0" {
            result = dividend / divisor;
        } else {
            throw "Division by zero attempted";
        }
    } catch (error) {
        say Caught error: error;
        result = 0;
        say Division by zero prevented;
    }
}
```

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

## 🎯 FULL example (nested calls + multi-namespace)

```mdl
// mypack.mdl - complete example for Minecraft Datapack Language
pack "Minecraft Datapack Language" description "Example datapack" pack_format 82;

namespace "example";

// Global variables
var num counter = 0;
var str message = "Hello World";
var list items = ["sword", "shield"];

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
    message = "Updated message";
    items.append("potion");
    var num item_count = items.length;
    say Item count: item_count;
}

// Hook the function into load and tick
on_load "example:hello";
on_tick "example:hello";

// Second namespace with a cross-namespace call
namespace "util";

function "helper" {
    say [util:helper] Helping out...;
    var num helper_count = 0;
    helper_count = helper_count + 1;
    say Helper count: helper_count;
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
- **Variable system** with numbers, strings, and lists.
- **Modern syntax** with curly braces and semicolons.

---

## 🐍 Python API equivalent

```python
from minecraft_datapack_language import Pack

def build_pack():
    p = Pack(name="Minecraft Datapack Language",
             description="Example datapack",
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
