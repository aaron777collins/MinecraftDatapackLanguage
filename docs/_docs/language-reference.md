---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

# MDL Language Reference

This is the complete reference for the Minecraft Datapack Language (MDL) syntax.

## Overview

MDL is a simple language designed to make writing Minecraft datapacks easier. It compiles to standard `.mcfunction` files and follows the 1.21+ datapack structure. MDL uses JavaScript-style syntax with curly braces and semicolons for explicit block boundaries and unlimited nesting support.

## Basic Syntax

### Comments

Comments start with `//` and continue to the end of the line:

```mdl
// This is a comment
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
// Legacy format (pre-82)
pack "Pack Name" [description "Description"] [pack_format N];

// Modern format (82+)
pack "Pack Name" [description "Description"] [pack_format N] [min_format [major, minor]] [max_format [major, minor]] [min_engine_version "version"];
```

**Parameters:**
- `"Pack Name"` (required): The name of your datapack
- `description "Description"` (optional): A description of your datapack
- `pack_format N` (optional): Minecraft pack format version (default: 82)
- `min_format [major, minor]` (optional, 82+): Minimum supported pack format version
- `max_format [major, minor]` (optional, 82+): Maximum supported pack format version
- `min_engine_version "version"` (optional, 82+): Minimum Minecraft engine version required

**Important Rules:**
- **Single file**: Must have a pack declaration
- **Multi-file projects**: Only the first file should have a pack declaration
- **Module files**: Should NOT have pack declarations
- **Statement termination**: All statements must end with semicolons `;`

**Examples:**

```mdl
// Legacy format (pre-82)
pack "My Datapack";
pack "My Datapack" description "A cool datapack";
pack "My Datapack" description "For older versions" pack_format 47;

// Modern format (82+)
pack "My Datapack" pack_format 82 min_format [82, 0] max_format [82, 1] min_engine_version "1.21.4";
pack "My Datapack" description "A cool datapack" pack_format 82 min_format [82, 0] max_format [82, 1];
pack "My Datapack" description "For newer versions" pack_format 83 min_format [83, 0] max_format [83, 2];
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

## Functions

Functions contain Minecraft commands and are the core of your datapack:

```mdl
function "function_name" {
    command1;
    command2;
    command3;
}
```

**Rules:**
- Function names should be descriptive
- **Explicit block boundaries**: Functions use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- Each non-empty line becomes a Minecraft command
- Comments are stripped from the output
- **Unlimited nesting**: Functions can contain any combination of control structures

**Example:**

```mdl
function "welcome" {
    say Welcome to my datapack!;
    tellraw @a {"text":"Hello World!","color":"green"};
    effect give @a minecraft:glowing 10 1;
}
```

## Conditional Blocks

MDL supports if/else if/else statements for conditional execution with unlimited nesting:

```mdl
function "conditional_example" {
    if "entity @s[type=minecraft:player]" {
        say Player detected!;
        effect give @s minecraft:glowing 5 1;
    } else if "entity @s[type=minecraft:zombie]" {
        say Zombie detected!;
        effect give @s minecraft:poison 5 1;
    } else {
        say Unknown entity;
        effect give @s minecraft:slowness 5 1;
    }
}
```

**Rules:**
- Conditions must be valid Minecraft selector syntax (e.g., `entity @s[type=minecraft:player]`)
- **Explicit block boundaries**: Conditional blocks use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- You can have multiple `else if` blocks
- The `else` block is optional
- **Unlimited nesting**: Conditional blocks can be nested to any depth
- Conditional blocks are compiled to separate functions and called with `execute` commands
- Each conditional block becomes its own function with a generated name

**Example with complex conditions:**

```mdl
function "weapon_effects" {
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
        say Diamond sword detected!;
        effect give @s minecraft:strength 10 1;
    } else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:golden_sword'}}]" {
        say Golden sword detected!;
        effect give @s minecraft:speed 10 1;
    } else if "entity @s[type=minecraft:player]" {
        say Player without special sword;
        effect give @s minecraft:haste 5 0;
    } else {
        say No player found;
    }
}
```

**Advanced conditional examples:**

```mdl
// Multiple conditions with different entity types
function "entity_detection" {
    if "entity @s[type=minecraft:player]" {
        say Player detected!;
        effect give @s minecraft:glowing 5 1;
        tellraw @a {"text":"A player is nearby!","color":"green"};
    } else if "entity @s[type=minecraft:zombie]" {
        say Zombie detected!;
        effect give @s minecraft:poison 5 1;
        tellraw @a {"text":"A zombie is nearby!","color":"red"};
    } else if "entity @s[type=minecraft:creeper]" {
        say Creeper detected!;
        effect give @s minecraft:resistance 5 1;
        tellraw @a {"text":"A creeper is nearby!","color":"dark_red"};
    } else {
        say Unknown entity detected;
        tellraw @a {"text":"Something unknown is nearby...","color":"gray"};
    }
}

// Conditional with function calls
function "main_logic" {
    if "entity @s[type=minecraft:player]" {
        say Executing player logic;
        function example:player_effects;
        function example:player_ui;
    } else if "entity @s[type=minecraft:zombie]" {
        say Executing zombie logic;
        function example:zombie_ai;
        function example:zombie_effects;
    } else {
        say Executing default logic;
        function example:default_behavior;
    }
}

// Conditional with complex NBT data
function "item_detection" {
    if "entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:diamond_sword\",Count:1b}]}]" {
        say Player has diamond sword in first slot!;
        effect give @s minecraft:strength 10 1;
    } else if "entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:golden_sword\",Count:1b}]}]" {
        say Player has golden sword in first slot!;
        effect give @s minecraft:speed 10 1;
    } else if "entity @s[type=minecraft:player]" {
        say Player has no special sword;
        effect give @s minecraft:haste 5 0;
    }
}
```

**How conditionals work:**

When you write conditional blocks in MDL, they are automatically converted to separate functions and called using Minecraft's `execute` command. The system ensures proper logical flow where `else if` blocks only execute if all previous conditions were false, and `else` blocks only execute if all conditions were false.

For example, the above `weapon_effects` function generates:

**Main function (`weapon_effects.mcfunction`):**
```mcfunction
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run function example:weapon_effects_if_1
execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] if entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:golden_sword"}}] run function example:weapon_effects_elif_2
execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:golden_sword"}}] if entity @s[type=minecraft:player] run function example:weapon_effects_elif_3
execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:"minecraft:golden_sword"}}] unless entity @s[type=minecraft:player] run function example:weapon_effects_else
```

**Generated conditional functions:**
- `weapon_effects_if_1.mcfunction` - Diamond sword effects
- `weapon_effects_elif_2.mcfunction` - Golden sword effects  
- `weapon_effects_elif_3.mcfunction` - Default player effects
- `weapon_effects_else.mcfunction` - No player found

### While Loops

MDL supports while loops for repetitive execution based on conditions with unlimited nesting:

```mdl
function "while_example" {
    scoreboard players set @s counter 5;
    while "score @s counter matches 1.." {
        say Counter: @s counter;
        scoreboard players remove @s counter 1;
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
- **Unlimited nesting**: While loops can be nested to any depth
- While loops are compiled to separate functions and use recursive calls

**Example with entity condition:**

```mdl
function "entity_while" {
    while "entity @e[type=minecraft:zombie,distance=..10]" {
        say Zombie nearby!;
        effect give @e[type=minecraft:zombie,distance=..10,limit=1] minecraft:glowing 5 1;
        say Applied effect to zombie;
    }
}
```

### For Loops

MDL supports for loops for iterating over entity collections with unlimited nesting:

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
- Variable name (e.g., `player`) is used for reference but doesn't affect execution
- Collection must be a valid Minecraft entity selector
- **Explicit block boundaries**: For loops use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- For loops iterate over each entity in the collection
- **Unlimited nesting**: For loops can be nested to any depth
- For loops are compiled to separate functions using `execute as` commands

**Example with complex selector:**

```mdl
function "complex_for" {
    for player in @a[gamemode=survival] {
        say Processing survival player: @s;
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
            say Player has diamond sword!;
            effect give @s minecraft:strength 10 1;
        } else {
            say Player has no diamond sword;
            effect give @s minecraft:haste 5 0;
        }
    }
}
```

**How loops work:**

Loops in MDL are implemented using recursive function calls:

**While loops** generate:
- A main function that starts the loop
- A loop body function containing the commands
- A control function that calls the body and then calls itself if the condition is still true

**For loops** generate:
- A main function that starts the iteration
- A loop body function containing the commands
- A control function that uses `execute as` to iterate through entities

This approach ensures proper execution flow and prevents infinite loops while maintaining compatibility with Minecraft's function system.

## Function Calls

Functions can call other functions using fully qualified names:

```mdl
function "main" {
    say Starting main function;
    function example:helper;
    say Back in main function;
}
```

**Rules:**
- Use the format `namespace:function_name`
- The called function must exist
- Cross-namespace calls are supported
- **Statement termination**: Function calls must end with semicolons `;`

## Lifecycle Hooks

MDL provides easy ways to hook into Minecraft's lifecycle:

### on_load

Runs when the datapack is loaded:

```mdl
on_load "namespace:function_name";
```

### on_tick

Runs every tick (20 times per second):

```mdl
on_tick "namespace:function_name";
```

**Example:**

```mdl
function "init" {
    say Datapack loaded!;
}

function "tick" {
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1;
}

on_load "example:init";
on_tick "example:tick";
```

## Tags

Tags allow your functions to participate in vanilla tag systems:

```mdl
tag registry "tag_name" {
    add "namespace:function_name";
    add "another_namespace:another_function";
}
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
// Function tags
tag function "minecraft:load" {
    add "example:init";
}

tag function "minecraft:tick" {
    add "example:tick";
    add "ui:update_hud";
}

// Item tags
tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

// Block tags
tag block "example:glassy" {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
```

### Tag Replacement

You can replace existing tags instead of adding to them:

```mdl
tag function "minecraft:tick" replace {
    add "example:my_tick_function";
}
```

## Multi-line Commands

Long commands can be split across multiple lines using backslashes:

```mdl
function "complex_command" {
    tellraw @a \
        {"text":"This is a very long message",\
         "color":"gold",\
         "bold":true};
}
```

This compiles to a single line in the `.mcfunction` file.

## Complete Example

Here's a complete example showing all the features:

```mdl
// Complete example datapack
pack "Example Pack" description "Shows all MDL features" pack_format 48;

namespace "core";

function "init" {
    say [core:init] Initializing datapack...;
    tellraw @a {"text":"Example Pack loaded!","color":"green"};
}

function "tick" {
    say [core:tick] Running core systems...;
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1;
}

// Hook into vanilla lifecycle
on_load "core:init";
on_tick "core:tick";

namespace "combat";

function "weapon_effects" {
    say [combat:weapon_effects] Applying weapon effects...;
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true;
}

function "update_combat" {
    function core:tick;
    function combat:weapon_effects;
}

namespace "ui";

function "hud" {
    say [ui:hud] Updating HUD...;
    title @a actionbar {"text":"Example Pack Active","color":"gold"};
}

function "update_ui" {
    function ui:hud;
    function combat:update_combat;
}

// Function tags
tag function "minecraft:load" {
    add "core:init";
}

tag function "minecraft:tick" {
    add "ui:update_ui";
}

// Data tags
tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

tag block "example:glassy" {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
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
function "init" {
    // Set up global variables
    scoreboard objectives add my_objective dummy;
    // Initialize systems
    function example:setup_combat;
    function example:setup_ui;
}

on_load "example:init";
```

### Tick Pattern

```mdl
function "tick" {
    // Update all systems
    function example:update_combat;
    function example:update_ui;
    function example:update_data;
}

on_tick "example:tick";
```

### Conditional Execution

MDL provides built-in support for if/else if/else statements with unlimited nesting:

```mdl
function "weapon_effects" {
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
        say Diamond sword detected!;
        effect give @s minecraft:strength 10 1;
    } else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:golden_sword'}}]" {
        say Golden sword detected!;
        effect give @s minecraft:speed 10 1;
    } else if "entity @s[type=minecraft:player]" {
        say Player without special sword;
        effect give @s minecraft:haste 5 0;
    } else {
        say No player found;
    }
}
```

This is equivalent to the traditional approach:

```mdl
function "weapon_effects_traditional" {
    // Check if player has specific item
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run function example:sword_effects;
    // Check if player is in specific dimension
    execute as @a[dimension=minecraft:the_nether] \
        run function example:nether_effects;
}
```

## Language Implementation

MDL uses a robust JavaScript-style lexer and parser for unlimited nesting support:

### Lexer Features
- **Token-based parsing**: Converts source code into structured tokens
- **Explicit boundaries**: Handles curly braces, semicolons, and keywords
- **Quoted string support**: Properly handles strings with spaces and special characters
- **Comment handling**: Supports `//` style comments
- **Keyword recognition**: Identifies all MDL keywords and control structures

### Parser Features
- **Recursive descent**: Handles unlimited nesting depth
- **AST generation**: Creates structured Abstract Syntax Trees
- **Error recovery**: Provides detailed error messages for debugging
- **Block parsing**: Correctly parses nested blocks and control structures

### Unlimited Nesting Support
The JavaScript-style parser supports unlimited nesting of:
- **Conditional blocks**: `if`, `else if`, `else` statements
- **Loop structures**: `for` and `while` loops
- **Function calls**: Nested function invocations
- **Mixed structures**: Any combination of the above

**Example of extreme nesting (29 levels deep):**
```mdl
function "extreme_nesting" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            for item in @s {
                while "entity @s[type=minecraft:item]" {
                    if "entity @s[nbt={Item:{id:'minecraft:diamond'}}]" {
                        // ... 25 more levels of nesting ...
                        say This is the deepest level!;
                    }
                }
            }
        }
    }
}
```

## Troubleshooting

### Common Errors

1. **Missing semicolons**: All statements must end with semicolons `;`
2. **Missing curly braces**: All blocks must use explicit curly braces `{` and `}`
3. **Missing pack declaration**: Single files must have a pack declaration; multi-file projects only need one in the first file
4. **Duplicate function names**: Function names must be unique within each namespace
5. **Invalid namespace names**: Use only lowercase letters, numbers, and underscores

### Validation

Use the `mdl check` command to validate your MDL files:

```bash
mdl check my_file.mdl
mdl check --json my_file.mdl  # For detailed output
```
