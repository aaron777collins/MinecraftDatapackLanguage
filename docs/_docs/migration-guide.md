# Migration Guide: Legacy MDL to JavaScript-style MDL (v10+)

This guide helps you migrate from the legacy MDL format (v9 and below) to the new JavaScript-style MDL format (v10+).

## Overview

The new JavaScript-style MDL format introduces significant improvements:

- **Modern syntax** with curly braces and semicolons
- **Variable system** with types and scoping
- **Advanced control flow** with switch statements and error handling
- **Import system** for modular code
- **Better tooling** with VS Code extension and IntelliSense

## Quick Migration Checklist

- [ ] Update pack format from 48 to 82
- [ ] Convert comments from `#` to `//`
- [ ] Add curly braces `{}` around code blocks
- [ ] Add semicolons `;` after statements
- [ ] Update function declarations
- [ ] Update control flow structures
- [ ] Test the migrated code

## Step-by-Step Migration

### 1. Update Pack Declaration

**Before (Legacy):**
```mdl
pack "My Pack" description "Description" pack_format 48
```

**After (New):**
```mdl
pack "My Pack" description "Description" pack_format 82;
```

### 2. Update Comments

**Before (Legacy):**
```mdl
# This is a comment
# Another comment
```

**After (New):**
```mdl
// This is a comment
// Another comment

/* This is a block comment
   that can span multiple lines */
```

### 3. Update Function Declarations

**Before (Legacy):**
```mdl
function "my_function":
    say Hello World
    effect give @a minecraft:speed 10 1
```

**After (New):**
```mdl
function "my_function" {
    say Hello World;
    effect give @a minecraft:speed 10 1;
}
```

### 4. Update Control Flow

#### If Statements

**Before (Legacy):**
```mdl
if "entity @s[type=minecraft:player]":
    say Player detected
else if "entity @s[type=minecraft:zombie]":
    say Zombie detected
else:
    say Unknown entity
```

**After (New):**
```mdl
if "entity @s[type=minecraft:player]" {
    say Player detected;
} else if "entity @s[type=minecraft:zombie]" {
    say Zombie detected;
} else {
    say Unknown entity;
}
```

#### While Loops

**Before (Legacy):**
```mdl
while "score @s counter matches 1..":
    say Counter: @s counter
    scoreboard players remove @s counter 1
```

**After (New):**
```mdl
while "score @s counter matches 1.." {
    say Counter: @s counter;
    scoreboard players remove @s counter 1;
}
```

#### For Loops

**Before (Legacy):**
```mdl
for player in @a:
    effect give @s minecraft:speed 10 1
    particle minecraft:cloud ~ ~ ~ 0.5 0.5 0.5 0.1 5
```

**After (New):**
```mdl
for player in @a {
    effect give @s minecraft:speed 10 1;
    particle minecraft:cloud ~ ~ ~ 0.5 0.5 0.5 0.1 5;
}
```

### 5. Update Hooks

**Before (Legacy):**
```mdl
on_tick "example:tick_function"
on_load "example:load_function"
```

**After (New):**
```mdl
on_tick "example:tick_function";
on_load "example:load_function";
```

### 6. Update Tags

**Before (Legacy):**
```mdl
tag function "minecraft:tick":
    add "example:tick_function"

tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"
```

**After (New):**
```mdl
tag "function" "minecraft:tick" values ["example:tick_function"];

tag "item" "example:swords" values ["minecraft:diamond_sword", "minecraft:netherite_sword"];
```

## Complete Migration Example

### Before (Legacy MDL)

```mdl
pack "Legacy Example" description "Simple legacy pack" pack_format 48

namespace "example"

# Global tick function
function "tick":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            effect give @s minecraft:speed 5 0
            particle minecraft:cloud ~ ~ ~ 0.3 0.3 0.3 0.1 3
        else:
            effect give @s minecraft:slowness 5 0

# Load function
function "load":
    say Pack loaded
    scoreboard objectives add counter dummy

on_tick "example:tick"
on_load "example:load"
```

### After (JavaScript-style MDL)

```mdl
pack "Modern Example" description "Migrated to v10" pack_format 82;

namespace "example";

// Global variables
var num counter = 0;

// Global tick function
function "tick" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            effect give @s minecraft:speed 5 0;
            particle minecraft:cloud ~ ~ ~ 0.3 0.3 0.3 0.1 3;
        } else {
            effect give @s minecraft:slowness 5 0;
        }
    }
}

// Load function
function "load" {
    say Pack loaded;
    scoreboard objectives add counter dummy;
    counter = 0;
}

// Lifecycle hooks
on_tick "example:tick";
on_load "example:load";
```

## New Features You Can Add

After migration, you can enhance your code with new features:

### Variables

```mdl
// Add variables to your migrated code
var num player_count = 0;
var str welcome_message = "Welcome to the server!";
var list effects = ["speed", "jump_boost", "night_vision"];

function "count_players" {
    player_count = 0;
    for player in @a {
        player_count = player_count + 1;
    }
    say Player count: player_count;
}
```

### Advanced Control Flow

```mdl
// Add switch statements
function "handle_item" {
    switch (item_type) {
        case "sword":
            say You have a sword;
            break;
        case "shield":
            say You have a shield;
            break;
        default:
            say Unknown item;
            break;
    }
}

// Add error handling
function "safe_operation" {
    try {
        say Attempting operation;
        // risky operation here
    } catch (error) {
        say Operation failed: error;
    }
}
```

### Import System

```mdl
// Split your code into modules
import "utils" from "./utils.mdl";
import "combat" as "battle" from "./combat.mdl";

function "main" {
    utils.initialize();
    battle.start_combat();
}
```

## Automated Migration Tools

### Using the MDL CLI

The MDL CLI includes migration tools:

```bash
# Convert a legacy file to new format
mdl migrate --input legacy_file.mdl --output new_file.mdl

# Convert an entire directory
mdl migrate --input legacy_dir/ --output new_dir/

# Preview changes without writing files
mdl migrate --input legacy_file.mdl --preview
```

### Migration Script

You can also use the Python API for custom migration:

```python
from minecraft_datapack_language import migrate_legacy_to_new

# Migrate a single file
migrate_legacy_to_new("legacy_file.mdl", "new_file.mdl")

# Migrate with custom options
migrate_legacy_to_new(
    "legacy_file.mdl", 
    "new_file.mdl",
    add_variables=True,
    add_error_handling=True
)
```

## Testing Your Migration

After migration, test your code thoroughly:

```bash
# Check syntax
mdl check new_file.mdl

# Build the datapack
mdl build --mdl new_file.mdl -o dist

# Run tests
mdl test --mdl new_file.mdl
```

## Common Migration Issues

### Missing Semicolons

**Error:** `Expected semicolon after statement`

**Solution:** Add semicolons after all statements:
```mdl
// Wrong
say Hello
effect give @a minecraft:speed 10 1

// Correct
say Hello;
effect give @a minecraft:speed 10 1;
```

### Missing Curly Braces

**Error:** `Expected opening brace`

**Solution:** Add curly braces around code blocks:
```mdl
// Wrong
if "condition":
    say True

// Correct
if "condition" {
    say True;
}
```

### Incorrect Pack Format

**Error:** `Invalid pack format`

**Solution:** Update pack format to 82:
```mdl
// Wrong
pack "My Pack" pack_format 48

// Correct
pack "My Pack" pack_format 82;
```

## Best Practices

1. **Migrate incrementally**: Convert one file at a time
2. **Test frequently**: Check syntax after each major change
3. **Use version control**: Commit changes regularly
4. **Backup original files**: Keep copies of legacy code
5. **Document changes**: Note what was changed and why
6. **Add new features gradually**: Don't try to add everything at once

## Getting Help

If you encounter issues during migration:

1. Check the [error messages](error-reference.md) for specific solutions
2. Use the `--verbose` flag for detailed error information
3. Report issues on the GitHub repository
4. Ask for help in the community discussions

## Next Steps

After successful migration:

1. **Install the VS Code extension** for better development experience
2. **Explore new features** like variables and advanced control flow
3. **Refactor your code** to take advantage of the new syntax
4. **Add tests** using the new testing framework
5. **Share your experience** with the community

---

**Previous**: [Legacy MDL Language Reference](legacy-mdl-language.md) | **Next**: [Language Reference](language-reference.md)
