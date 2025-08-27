---
layout: page
title: Multi-file Projects
permalink: /docs/multi-file-projects/
---

# Multi-file Projects

MDL supports building datapacks from multiple `.mdl` files, making it easy to organize large projects into logical modules.

## Overview

Multi-file projects allow you to:

- **Organize by feature**: Split your datapack into logical modules
- **Improve maintainability**: Keep related functions together
- **Enable collaboration**: Different team members can work on different modules
- **Reduce complexity**: Break large datapacks into manageable pieces

## How It Works

### File Merging Process

1. **Directory scanning**: When you pass a directory to `--mdl`, MDL recursively finds all `.mdl` files
2. **File parsing**: Each file is parsed into a `Pack` object
3. **Merging**: All packs are merged into a single datapack
4. **Conflict resolution**: Duplicate function names within the same namespace cause errors
5. **Output**: A single datapack is generated

### Pack Declaration Rules

**Important**: Only the **first file** should have a pack declaration. All other files are treated as modules.

- ✅ **First file**: Must have `pack "Name"` declaration
- ❌ **Module files**: Should NOT have pack declarations
- ✅ **Single file compilation**: When compiling a single file, it **must** have a pack declaration

## Project Structure

### Recommended Organization

```
my_datapack/
├── core.mdl              # ✅ HAS pack declaration
├── combat/
│   ├── weapons.mdl       # ❌ NO pack declaration (module)
│   └── armor.mdl         # ❌ NO pack declaration (module)
├── ui/
│   └── hud.mdl           # ❌ NO pack declaration (module)
├── data/
│   └── recipes.mdl       # ❌ NO pack declaration (module)
└── README.md
```

### Alternative Structures

**By namespace:**
```
my_datapack/
├── main.mdl              # ✅ HAS pack declaration
├── combat.mdl            # ❌ NO pack declaration
├── ui.mdl                # ❌ NO pack declaration
└── data.mdl              # ❌ NO pack declaration
```

**By feature:**
```
my_datapack/
├── core.mdl              # ✅ HAS pack declaration
├── magic_system.mdl      # ❌ NO pack declaration
├── economy.mdl           # ❌ NO pack declaration
└── minigames.mdl         # ❌ NO pack declaration
```

## Complete Example

Let's create a complete multi-file adventure pack:

### Project Structure

```
adventure_pack/
├── core.mdl              # Main pack and core systems
├── combat/
│   ├── weapons.mdl       # Weapon-related functions
│   └── armor.mdl         # Armor-related functions
├── ui/
│   └── hud.mdl           # UI and HUD functions
└── data/
    └── tags.mdl          # Data tags and function tags
```

### File Contents

**`core.mdl`** (main file with pack declaration):
```mdl
# core.mdl - Main pack and core systems
pack "Adventure Pack" description "Multi-file example datapack" pack_format 48

namespace "core"

function "init":
    say [core:init] Initializing Adventure Pack...
    tellraw @a {"text":"Adventure Pack loaded!","color":"green"}

function "tick":
    say [core:tick] Core systems running...
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

# Hook into vanilla lifecycle
on_load "core:init"
on_tick "core:tick"
```

**`combat/weapons.mdl`** (combat module):
```mdl
# combat/weapons.mdl - Weapon-related functions
namespace "combat"

function "weapon_effects":
    say [combat:weapon_effects] Applying weapon effects...
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true

function "update_combat":
    function core:tick
    function combat:weapon_effects
```

**`combat/armor.mdl`** (armor module):
```mdl
# combat/armor.mdl - Armor-related functions
namespace "combat"

function "armor_bonus":
    say [combat:armor_bonus] Checking armor bonuses...
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] \
        run effect give @s minecraft:resistance 1 0 true

function "update_armor":
    function combat:armor_bonus
```

**`ui/hud.mdl`** (UI module):
```mdl
# ui/hud.mdl - User interface functions
namespace "ui"

function "show_hud":
    say [ui:show_hud] Updating HUD...
    title @a actionbar {"text":"Adventure Pack Active","color":"gold"}

function "update_ui":
    function ui:show_hud
    function combat:update_combat
    function combat:update_armor
```

**`data/tags.mdl`** (data module):
```mdl
# data/tags.mdl - Data tags and function tags
namespace "data"

# Function tag to run UI updates
tag function "minecraft:tick":
    add "ui:update_ui"

# Item tags
tag item "adventure:weapons":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag item "adventure:armor":
    add "minecraft:diamond_helmet"
    add "minecraft:diamond_chestplate"
    add "minecraft:diamond_leggings"
    add "minecraft:diamond_boots"
```

### Building the Project

```bash
# Build from directory
mdl build --mdl adventure_pack/ -o dist --verbose

# Or build from specific files
mdl build --mdl "core.mdl combat/weapons.mdl combat/armor.mdl ui/hud.mdl data/tags.mdl" -o dist
```

## Best Practices

### File Organization

1. **One pack declaration per project**: Only the first file should have a pack declaration
2. **Module files**: All other files should NOT have pack declarations
3. **Organize by namespace**: Consider splitting files by namespace or feature
4. **Use descriptive filenames**: `core.mdl`, `combat.mdl`, `ui.mdl` etc.
5. **Avoid conflicts**: Ensure function names are unique within each namespace

### Naming Conventions

- **Files**: Use lowercase with underscores (`weapon_effects.mdl`)
- **Namespaces**: Use lowercase with underscores (`combat_system`)
- **Functions**: Use descriptive names (`apply_weapon_effects`)

### Cross-Module Communication

- **Use fully qualified names**: Always use `namespace:function` when calling across modules
- **Document dependencies**: Comment on which modules depend on others
- **Keep modules focused**: Each module should have a single responsibility

### Error Prevention

- **Check before building**: Use `mdl check` to validate your entire project
- **Test modules individually**: Test each module before integrating
- **Use descriptive names**: Avoid generic names that might conflict

## CLI Usage

### Building Multi-file Projects

```bash
# Build entire directory
mdl build --mdl my_datapack/ -o dist

# Build specific files
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist

# Build with verbose output
mdl build --mdl my_datapack/ -o dist --verbose

# Build with custom wrapper name
mdl build --mdl my_datapack/ -o dist --wrapper mypack
```

### Validation

```bash
# Check entire project
mdl check my_datapack/

# Check specific files
mdl check "core.mdl combat.mdl ui.mdl"

# Get detailed JSON output
mdl check --json my_datapack/
```

## Common Patterns

### Module Dependencies

When modules depend on each other, use clear naming and documentation:

```mdl
# combat/weapons.mdl
namespace "combat"

function "weapon_effects":
    # This function depends on core:tick
    function core:tick
    # ... weapon logic
```

### Shared Utilities

Create utility modules for common functionality:

```mdl
# utils/helpers.mdl
namespace "utils"

function "send_message":
    tellraw @a {"text":"[System] ","color":"gray","extra":[{"text":"$1","color":"white"}]}

function "create_particle":
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1
```

### Configuration Modules

Use separate modules for configuration:

```mdl
# config/settings.mdl
namespace "config"

# Game settings
function "set_difficulty":
    difficulty normal

function "set_gamerules":
    gamerule doDaylightCycle false
    gamerule keepInventory true
```

## Troubleshooting

### Common Errors

1. **Multiple pack declarations**: Only the first file should have a pack declaration
2. **Missing pack declaration**: The first file must have a pack declaration
3. **Function conflicts**: Duplicate function names within the same namespace
4. **Missing dependencies**: Functions called before they're defined
5. **File not found**: Check file paths and extensions

### Error Messages

```
Error: [file.mdl:line:column] Duplicate function name 'hello' in namespace 'example'
```

This means you have the same function name in multiple files within the same namespace.

### Debugging Tips

1. **Use verbose mode**: `mdl build --mdl my_datapack/ -o dist --verbose`
2. **Check individual files**: Test each file separately first
3. **Validate before building**: Always run `mdl check` first
4. **Check file order**: Ensure the main file (with pack declaration) is processed first

## Advanced Techniques

### Conditional Modules

You can conditionally include modules based on build scripts:

```bash
# Build with combat module
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist

# Build without combat module
mdl build --mdl "core.mdl ui.mdl" -o dist
```

### Module Templates

Create template modules for common patterns:

```mdl
# templates/effect_system.mdl
namespace "effects"

function "apply_effect":
    # Template for applying effects
    execute as @a[nbt={SelectedItem:{id:"$ITEM_ID"}}] \
        run effect give @s $EFFECT_ID $DURATION $AMPLIFIER true
```

### Build Scripts

Create build scripts for complex projects:

```bash
#!/bin/bash
# build.sh

echo "Building Adventure Pack..."

# Check all files first
mdl check adventure_pack/

if [ $? -eq 0 ]; then
    # Build the project
    mdl build --mdl adventure_pack/ -o dist --verbose --wrapper adventure_pack
    
    if [ $? -eq 0 ]; then
        echo "Build successful!"
        echo "Output: dist/adventure_pack/"
    else
        echo "Build failed!"
        exit 1
    fi
else
    echo "Validation failed!"
    exit 1
fi
```

## Integration with Version Control

### Git Organization

```
my_datapack/
├── .gitignore
├── README.md
├── core.mdl
├── combat/
│   ├── weapons.mdl
│   └── armor.mdl
├── ui/
│   └── hud.mdl
└── data/
    └── tags.mdl
```

### .gitignore Example

```
# Build output
dist/
build/

# Temporary files
*.tmp
*.bak

# IDE files
.vscode/
.idea/
```

## Performance Considerations

### File Size

- **Keep files focused**: Don't put everything in one file
- **Balance granularity**: Don't split too finely
- **Consider loading**: More files mean more parsing time

### Build Performance

- **Use directory builds**: `mdl build --mdl src/` is faster than listing files
- **Check before building**: Use `mdl check` to catch errors early
- **Organize efficiently**: Group related functions together

## Future Enhancements

Planned improvements for multi-file projects:

- **Module dependencies**: Explicit dependency declarations
- **Conditional compilation**: Include/exclude modules based on flags
- **Module templates**: Reusable module patterns
- **Better error reporting**: More detailed conflict resolution
- **Build caching**: Faster incremental builds
