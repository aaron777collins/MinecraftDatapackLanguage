---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

# **MODERN** MDL Language Reference

This is the complete reference for the **modern JavaScript-style** Minecraft Datapack Language (MDL) syntax.

## Overview

MDL is a **modern JavaScript-style language** designed to make writing Minecraft datapacks easier. It compiles to standard `.mcfunction` files and follows the latest datapack structure. MDL uses JavaScript-style syntax with curly braces and semicolons for explicit block boundaries and **real control structures, variables, expressions, and multi-file projects that actually work**.

## Basic Syntax

### Comments

MDL supports modern JavaScript-style comments:

```mdl
// Single-line comments
/* Multi-line comments */

pack "My Pack";  // Inline comments are also supported
```

**Important**: Comments inside function bodies are preserved in the output `.mcfunction` files, but full-line comments are stripped.

### Whitespace

- Empty lines are ignored
- Indentation is optional (for readability only)
- **Explicit block boundaries** using curly braces `{` and `}`
- **Statement termination** using semicolons `;`

## Pack Declaration

**Single file compilation**: Every MDL file must start with a pack declaration when compiled individually.

**Multi-file compilation**: Only the first file should have a pack declaration. All other files are treated as modules.

```mdl
pack "Pack Name" [description "Description"] [pack_format N];
```

**Parameters:**
- `"Pack Name"` (required): The name of your datapack
- `description "Description"` (optional): A description of your datapack
- `pack_format N` (optional): Minecraft pack format version (default: 82)

**Important Rules:**
- **Single file**: Must have a pack declaration
- **Multi-file projects**: Only the first file should have a pack declaration
- **Module files**: Should NOT have pack declarations
- **Statement termination**: All statements must end with semicolons `;`

**Examples:**

```mdl
pack "My Datapack" pack_format 82;
pack "My Datapack" description "A cool datapack" pack_format 82;
pack "My Datapack" description "For newer versions" pack_format 83;
```

## Namespaces

Namespaces organize your functions and other resources:

```mdl
namespace "namespace_name";
```

**Rules:**
- Namespace names should be lowercase
- Use underscores or hyphens for multi-word names
- The namespace applies to all following blocks until another namespace is declared
- **Statement termination**: Namespace declarations must end with semicolons `;`

**Example:**

```mdl
namespace "combat";
function "weapon_effects" {
    // This function will be combat:weapon_effects
}

namespace "ui";
function "hud" {
    // This function will be ui:hud
}
```

## Variables

MDL supports **number variables** with **expressions, arithmetic operations, and multi-file merging**:

### Variable Declarations

```mdl
var num variable_name = initial_value;
```

**Rules:**
- Only `num` type is supported (stored in scoreboards)
- Variable names should be descriptive
- Initial values are optional (defaults to 0)
- **Statement termination**: Variable declarations must end with semicolons `;`

**Examples:**

```mdl
var num counter = 0;
var num health = 20;
var num level = 1;
var num experience = 0;
```

### Variable Substitution

Use `$variable_name$` to read values from scoreboards in strings and conditions:

```mdl
function "example" {
    say Health: $health$;
    say Level: $level$;
    say Experience: $experience$;
    
    // In conditions
    if "$health$ < 10" {
        say Health is low!;
    }
}
```

### Expressions

MDL supports arithmetic operations with variables:

```mdl
function "expressions" {
    var num a = 10;
    var num b = 5;
    
    // Basic arithmetic
    var num sum = $a$ + $b$;
    var num difference = $a$ - $b$;
    var num product = $a$ * $b$;
    var num quotient = $a$ / $b$;
    
    // Complex expressions
    var num total = $health$ + $experience$;
    var num average = $total$ / 2;
    var num bonus = $level$ * 10 + $counter$;
    
    // Variable assignment with expressions
    counter = $counter$ + 1;
    health = $health$ - 5;
    experience = $level$ * 100 + $counter$;
}
```

**Supported Operations:**
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)

**Order of Operations:**
- Multiplication and division are performed before addition and subtraction
- Use parentheses for explicit grouping (when supported)

## Functions

Functions contain Minecraft commands and are the core of your datapack:

```mdl
function "function_name" {
    // Minecraft commands go here
    say Hello World;
    tellraw @a {"text":"Welcome!","color":"green"};
}
```

**Rules:**
- Function names should be descriptive
- Functions must be quoted: `"function_name"`
- **Explicit block boundaries**: Use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- Functions can call other functions using fully qualified IDs

**Example:**

```mdl
function "inner" {
    say [example:inner] This is the inner function;
    tellraw @a {"text":"Running inner","color":"yellow"};
}

function "outer" {
    say [example:outer] This is the outer function;
    function example:inner;  // Call another function
    tellraw @a {"text":"Back in outer","color":"aqua"};
}
```

## Control Structures

MDL supports **full control structures** with proper logic flow.

### Conditional Blocks (if/else if/else)

```mdl
function "conditional_example" {
    var num player_level = 15;
    var num player_health = 8;
    
    if "$player_level$ >= 10" {
        if "$player_health$ < 10" {
            say Advanced player with low health!;
            effect give @s minecraft:regeneration 10 1;
            player_health = $player_health$ + 10;
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
- **Explicit block boundaries**: Use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- You can have multiple `else if` blocks
- The `else` block is optional
- **Proper logic**: `else if` blocks only execute if previous conditions were false
- **Expressions in conditions**: Support for arithmetic operations in conditions

### While Loops

```mdl
function "while_example" {
    var num counter = 5;
    
    // Default recursion method (immediate execution)
    while "$counter$ > 0" {
        say "Counter: $counter$";
        counter = $counter$ - 1;
    }
    
    // Schedule method (spreads across ticks for performance)
    counter = 10;
    while "$counter$ > 0" method="schedule" {
        say "Schedule counter: $counter$";
        counter = $counter$ - 1;
    }
    
    // Expression in loop condition
    var num max_count = 5;
    counter = 0;
    while "$counter$ < $max_count$ * 2" {
        say "Expression counter: $counter$";
        counter = $counter$ + 1;
    }
}
```

**Rules:**
- Conditions use `$variable$` syntax for variable substitution
- **Explicit block boundaries**: Use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- While loops continue until the condition becomes false
- **Method Selection**: Choose `method="recursion"` (default) or `method="schedule"`
- **Recursion method**: Executes all iterations immediately (good for small loops)
- **Schedule method**: Spreads iterations across ticks (better for long loops, prevents lag)
- **Important**: Ensure your loop body modifies the condition to avoid infinite loops
- **Expressions in conditions**: Support for arithmetic operations in loop conditions

## Hooks

Hooks automatically run functions at specific times:

```mdl
on_load "namespace:function_name";
on_tick "namespace:function_name";
```

**Rules:**
- **Namespaced IDs required**: Use `namespace:function_name` format
- `on_load`: Runs when the world loads
- `on_tick`: Runs every tick (20 times per second)
- **Statement termination**: Hook declarations must end with semicolons `;`

**Example:**

```mdl
on_load "example:init";
on_tick "example:tick";
```

## Tags

Tags allow your functions to participate in vanilla Minecraft systems:

```mdl
tag function "minecraft:tick" {
    add "namespace:function_name";
}
```

**Supported Tag Types:**
- `function` - Function tags
- `item` - Item tags
- `block` - Block tags
- `entity_type` - Entity type tags
- `fluid` - Fluid tags
- `game_event` - Game event tags

**Example:**

```mdl
tag function "minecraft:load" {
    add "example:init";
}

tag function "minecraft:tick" {
    add "example:tick";
}

tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}
```

## Multi-line Commands

Long JSON commands can be split across multiple lines with a trailing backslash `\`:

```mdl
function "multiline" {
    tellraw @a \
        {"text":"This text is really, really long so we split it",\
         "color":"gold"};
}
```

When compiled, the function becomes a single line:

```mcfunction
tellraw @a {"text":"This text is really, really long so we split it","color":"gold"}
```

## Multi-File Projects

MDL supports building datapacks from multiple files with proper namespace separation:

### Multi-File Building

```bash
# Build entire directory
mdl build --mdl my_project/ -o dist

# Build specific files
mdl build --mdl "core.mdl ui.mdl combat.mdl" -o dist
```

### Namespace Separation

Each file can have its own namespace, preventing function name conflicts:

```mdl
// core.mdl
namespace "core";
function "main" { ... }

// ui.mdl
namespace "ui";
function "main" { ... }  // Different from core:main!
```

### Variable Merging

Variables from all files are automatically merged and initialized together:

```mdl
// core.mdl
var num player_count = 0;

// ui.mdl
var num menu_state = 0;

// Both variables are initialized in the same load function
```

## Optimizations

MDL includes several automatic optimizations:

### Variable Optimization

Variables are automatically initialized in a global load function for better performance:

```mdl
var num counter = 0;
var num health = 20;
```

This generates a `load.mcfunction` file that:
- Creates all scoreboard objectives
- Initializes all variables to 0
- Sets non-zero initial values
- Creates the server armor stand entity

### Selector Optimization

System commands automatically use proper selectors:

```mdl
function "example" {
    say "Hello World";  // Converts to tellraw @a
    tellraw @a {"text":"Direct command"};  // Preserved as-is
}
```

- `say` commands are converted to `tellraw @a`
- Existing `tellraw @a` commands are preserved
- `tellraw @s` commands are converted to `tellraw @a` for system commands

### Multi-File Optimization

When building multiple files:
- Functions are properly namespaced
- Variables are merged and initialized together
- Hooks are combined into appropriate tag files
- No conflicts between same-named functions in different namespaces

## Complete Example

Here's a complete example showing all the features:

```mdl
// complete_example.mdl
pack "Complete Example" description "Shows all MDL features" pack_format 82;

namespace "example";

// Variables with expressions
var num counter = 0;
var num health = 20;
var num level = 1;
var num experience = 0;

function "init" {
    say [example:init] Initializing Complete Example...;
    tellraw @a {"text":"Complete Example loaded!","color":"green"};
    counter = 0;
    health = 20;
    level = 1;
    experience = 0;
}

function "tick" {
    counter = counter + 1;
    
    // Full control structure
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
    
    // Variable substitution
    say Counter: $counter$;
    
    // While loop
    while "$counter$ < 10" {
        counter = $counter$ + 1;
        say Counter: $counter$;
    }
    
    // Expressions
    experience = $level$ * 100 + $counter$;
    say Experience: $experience$;
}

// Hooks
on_load "example:init";
on_tick "example:tick";

// Tags
tag function "minecraft:load" {
    add "example:init";
}

tag function "minecraft:tick" {
    add "example:tick";
}
```

This example demonstrates:
- **JavaScript-style syntax** with curly braces and semicolons
- **Variables** with expressions and arithmetic
- **Full control structures** with if/else if/else
- **While loops** with method selection
- **Variable substitution** in strings and conditions
- **Hooks** for automatic execution
- **Tags** for vanilla integration
- **Optimizations** for better performance
