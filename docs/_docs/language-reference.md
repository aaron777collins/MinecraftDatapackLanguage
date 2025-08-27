---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

# MDL Language Reference

This is the complete reference for the Minecraft Datapack Language (MDL) syntax.

## Overview

MDL is a simple language designed to make writing Minecraft datapacks easier. It compiles to standard `.mcfunction` files and follows the 1.21+ datapack structure.

## Basic Syntax

### Comments

Comments start with `#` and continue to the end of the line:

```mdl
# This is a comment
pack "My Pack"  # Inline comments are also supported
```

**Important**: Comments inside function bodies are preserved in the output `.mcfunction` files, but full-line comments are stripped.

### Whitespace

- Empty lines are ignored
- Indentation must use **4 spaces** (tabs are not supported)
- Indentation determines block structure

## Pack Declaration

Every MDL file must start with a pack declaration:

```mdl
pack "Pack Name" [description "Description"] [pack_format N]
```

**Parameters:**
- `"Pack Name"` (required): The name of your datapack
- `description "Description"` (optional): A description of your datapack
- `pack_format N` (optional): Minecraft pack format version (default: 48 for 1.21+)

**Examples:**

```mdl
# Basic pack
pack "My Datapack"

# With description
pack "My Datapack" description "A cool datapack"

# With custom pack format
pack "My Datapack" description "For older versions" pack_format 47
```

## Namespaces

Namespaces organize your functions and other resources:

```mdl
namespace "namespace_name"
```

**Rules:**
- Namespace names should be lowercase
- Use underscores or hyphens for multi-word names
- The namespace applies to all following blocks until another namespace is declared

**Example:**

```mdl
namespace "combat"
function "weapon_effects":
    # This function will be combat:weapon_effects

namespace "ui"
function "hud":
    # This function will be ui:hud
```

## Functions

Functions contain Minecraft commands and are the core of your datapack:

```mdl
function "function_name":
    command1
    command2
    command3
```

**Rules:**
- Function names should be descriptive
- Commands must be indented with 4 spaces
- Each non-empty line becomes a Minecraft command
- Comments are stripped from the output

**Example:**

```mdl
function "welcome":
    say Welcome to my datapack!
    tellraw @a {"text":"Hello World!","color":"green"}
    effect give @a minecraft:glowing 10 1
```

## Function Calls

Functions can call other functions using fully qualified names:

```mdl
function "main":
    say Starting main function
    function example:helper
    say Back in main function
```

**Rules:**
- Use the format `namespace:function_name`
- The called function must exist
- Cross-namespace calls are supported

## Lifecycle Hooks

MDL provides easy ways to hook into Minecraft's lifecycle:

### on_load

Runs when the datapack is loaded:

```mdl
on_load "namespace:function_name"
```

### on_tick

Runs every tick (20 times per second):

```mdl
on_tick "namespace:function_name"
```

**Example:**

```mdl
function "init":
    say Datapack loaded!

function "tick":
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

on_load "example:init"
on_tick "example:tick"
```

## Tags

Tags allow your functions to participate in vanilla tag systems:

```mdl
tag registry "tag_name":
    add "namespace:function_name"
    add "another_namespace:another_function"
```

**Supported Registries:**
- `function` - Function tags
- `item` - Item tags
- `block` - Block tags
- `entity_type` - Entity type tags
- `fluid` - Fluid tags
- `game_event` - Game event tags

**Examples:**

```mdl
# Function tags
tag function "minecraft:load":
    add "example:init"

tag function "minecraft:tick":
    add "example:tick"
    add "ui:update_hud"

# Item tags
tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

# Block tags
tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"
```

### Tag Replacement

You can replace existing tags instead of adding to them:

```mdl
tag function "minecraft:tick" replace:
    add "example:my_tick_function"
```

## Multi-line Commands

Long commands can be split across multiple lines using backslashes:

```mdl
function "complex_command":
    tellraw @a \
        {"text":"This is a very long message",\
         "color":"gold",\
         "bold":true}
```

This compiles to a single line in the `.mcfunction` file.

## Complete Example

Here's a complete example showing all the features:

```mdl
# Complete example datapack
pack "Example Pack" description "Shows all MDL features" pack_format 48

namespace "core"

function "init":
    say [core:init] Initializing datapack...
    tellraw @a {"text":"Example Pack loaded!","color":"green"}

function "tick":
    say [core:tick] Running core systems...
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

# Hook into vanilla lifecycle
on_load "core:init"
on_tick "core:tick"

namespace "combat"

function "weapon_effects":
    say [combat:weapon_effects] Applying weapon effects...
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true

function "update_combat":
    function core:tick
    function combat:weapon_effects

namespace "ui"

function "hud":
    say [ui:hud] Updating HUD...
    title @a actionbar {"text":"Example Pack Active","color":"gold"}

function "update_ui":
    function ui:hud
    function combat:update_combat

# Function tags
tag function "minecraft:load":
    add "core:init"

tag function "minecraft:tick":
    add "ui:update_ui"

# Data tags
tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"
```

## Best Practices

### Naming Conventions

- **Namespaces**: Use lowercase with underscores (`combat_system`, `ui_components`)
- **Functions**: Use descriptive names (`weapon_effects`, `update_hud`)
- **Tags**: Use descriptive names that indicate purpose (`my_swords`, `glassy_blocks`)

### Organization

- Group related functions in the same namespace
- Use separate namespaces for different systems (combat, UI, data, etc.)
- Keep functions focused on a single responsibility

### Comments

- Use comments to explain complex logic
- Document the purpose of each function
- Add section headers for organization

### Error Prevention

- Always use fully qualified names for function calls
- Check that function names are unique within each namespace
- Validate your MDL files with `mdl check` before building

## Common Patterns

### Initialization Pattern

```mdl
function "init":
    # Set up global variables
    scoreboard objectives add my_objective dummy
    # Initialize systems
    function example:setup_combat
    function example:setup_ui

on_load "example:init"
```

### Tick Pattern

```mdl
function "tick":
    # Update all systems
    function example:update_combat
    function example:update_ui
    function example:update_data

on_tick "example:tick"
```

### Conditional Execution

```mdl
function "conditional":
    # Check if player has specific item
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run function example:sword_effects
    # Check if player is in specific dimension
    execute as @a[dimension=minecraft:the_nether] \
        run function example:nether_effects
```

## Troubleshooting

### Common Errors

1. **Indentation errors**: Make sure you're using exactly 4 spaces
2. **Missing pack declaration**: Every file must start with a pack declaration
3. **Duplicate function names**: Function names must be unique within each namespace
4. **Invalid namespace names**: Use only lowercase letters, numbers, and underscores

### Validation

Use the `mdl check` command to validate your MDL files:

```bash
mdl check my_file.mdl
mdl check --json my_file.mdl  # For detailed output
```
