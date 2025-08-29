---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

# **SIMPLIFIED** MDL Language Reference

This is the complete reference for the **simplified** Minecraft Datapack Language (MDL) syntax.

## Overview

MDL is a **simplified** language designed to make writing Minecraft datapacks easier. It compiles to standard `.mcfunction` files and follows the 1.21+ datapack structure. MDL uses JavaScript-style syntax with curly braces and semicolons for explicit block boundaries and **control structures that actually work**.

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
- Function names should be lowercase
- Use underscores or hyphens for multi-word names
- **Explicit block boundaries**: Functions use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- Functions can call other functions using fully qualified names

**Example:**

```mdl
function "hello" {
    say Hello from the hello function;
}

function "greet" {
    say I will call the hello function;
    function example:hello;
    say Back in the greet function;
}
```

## **SIMPLIFIED** Variables

MDL supports **number variables only** for simplicity and reliability.

### Variable Declarations

```mdl
var num variable_name = initial_value;
```

**Rules:**
- **Only `num` type supported**: All variables are numbers stored in scoreboards
- Variable names should be lowercase
- Use underscores for multi-word names
- **Statement termination**: Variable declarations must end with semicolons `;`

**Examples:**

```mdl
var num counter = 0;
var num health = 20;
var num level = 1;
var num player_score = 100;
```

### Variable Assignment

```mdl
variable_name = expression;
```

**Examples:**

```mdl
counter = 5;
health = health + 10;
level = level * 2;
player_score = player_score - 5;
```

### Variable Substitution

Use `$variable_name$` to read values from scoreboards in strings and conditions:

```mdl
// In strings
say Health: $health$;
tellraw @a {"text":"Level: $level$","color":"gold"};

// In conditions
if "$health$ < 10" {
    say Health is low!;
}

while "$counter$ > 0" {
    say Counter: $counter$;
    counter = counter - 1;
}
```

## **SIMPLIFIED** Control Flow

MDL supports conditional blocks and loops for control flow.

### Conditional Blocks (if/else if/else)

```mdl
if "condition" {
    // commands to run if condition is true
} else if "condition" {
    // commands to run if this condition is true
} else {
    // commands to run if no conditions were true
}
```

**Rules:**
- Conditions use `$variable$` syntax for variable substitution
- **Explicit block boundaries**: Conditional blocks use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- You can have multiple `else if` blocks
- The `else` block is optional
- Conditional blocks are compiled to separate functions and called with `execute` commands

**Examples:**

```mdl
function "check_player" {
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

### While Loops

MDL supports **flexible while loops** with user-choice implementation methods:

```mdl
// Default recursion method
while "condition" {
    // commands to repeat while condition is true
}

// Explicit recursion method
while "condition" method="recursion" {
    // commands to repeat while condition is true
}

// Schedule method for long-running loops
while "condition" method="schedule" {
    // commands to repeat while condition is true
}
```

**Rules:**
- Conditions use `$variable$` syntax for variable substitution
- **Explicit block boundaries**: While loops use curly braces `{` and `}`
- **Statement termination**: All commands must end with semicolons `;`
- While loops continue until the condition becomes false
- **Important**: Ensure your loop body modifies the condition to avoid infinite loops
- **Method selection**: Choose between `recursion` (default) and `schedule` methods

**Implementation Methods:**

**🔄 Recursion Method (Default):**
- Fast execution, immediate results
- Limited by `maxCommandChainLength` (~65,000 commands)
- Good for small loops (< 100 iterations)

**⏰ Schedule Method:**
- No function file limit, better for large loops
- Slightly slower due to tick scheduling
- Good for large loops (> 100 iterations)

**Examples:**

```mdl
function "countdown" {
    var num counter = 5;
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter = counter - 1;
    }
}

function "health_regeneration" {
    var num regen_count = 0;
    while "$regen_count$ < 3" method="recursion" {
        say Regenerating health...;
        effect give @s minecraft:regeneration 5 0;
        regen_count = regen_count + 1;
    }
}

function "large_processing" {
    var num item_count = 0;
    while "$item_count$ < 1000" method="schedule" {
        say Processing item $item_count$;
        item_count = item_count + 10;
    }
}

```
```

## Hooks

Hooks automatically run functions at specific times:

```mdl
on_load "namespace:function_name";
on_tick "namespace:function_name";
```

**Rules:**
- Function names must be fully qualified (include namespace)
- **Statement termination**: Hook declarations must end with semicolons `;`
- `on_load` runs when the datapack loads
- `on_tick` runs every game tick

**Examples:**

```mdl
on_load "example:init";
on_tick "example:tick";
on_tick "ui:update_hud";
```

## Tags

Tags allow your functions to participate in vanilla tag systems:

```mdl
tag function "tag_name" {
    add "namespace:function_name";
}
```

**Supported tag types:**
- `function` - Function tags
- `item` - Item tags
- `block` - Block tags
- `entity_type` - Entity type tags
- `fluid` - Fluid tags
- `game_event` - Game event tags

**Examples:**

```mdl
tag function "minecraft:load" {
    add "example:init";
}

tag function "minecraft:tick" {
    add "example:tick";
    add "ui:update_hud";
}

tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

tag block "example:glassy" {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
```

## **SIMPLIFIED** Expressions

MDL supports basic arithmetic operations with number variables:

### Arithmetic Operators

- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division

**Examples:**

```mdl
var num result = 0;
result = 5 + 3;        // result = 8
result = 10 - 4;       // result = 6
result = 3 * 7;        // result = 21
result = 15 / 3;       // result = 5

// With variables
var num a = 10;
var num b = 5;
result = a + b;        // result = 15
result = a * b;        // result = 50
```

### Variable Substitution in Expressions

You can use variable substitution in arithmetic expressions:

```mdl
var num health = 20;
var num bonus = 5;
health = $health$ + $bonus$;  // health = 25
```

## Complete Example

Here's a complete example showing all the **simplified** MDL features:

```mdl
// complete_example.mdl - Complete simplified MDL example
pack "Complete Example" description "Shows all simplified features" pack_format 82;

namespace "example";

// Number variables
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
    
    // Variable substitution
    say Counter: $counter$;
    say Health: $health$;
    say Level: $level$;
    
    // Conditional logic
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
        effect give @s minecraft:regeneration 10 1;
    } else if "$level$ > 5" {
        say High level player!;
        effect give @s minecraft:strength 10 1;
    } else {
        say Normal player;
        effect give @s minecraft:speed 10 0;
    }
    
    // While loop with different methods
    var num loop_count = 0;
    while "$loop_count$ < 3" {
        say Loop iteration: $loop_count$;
        loop_count = loop_count + 1;
    }
    
    // Schedule method for large loops
    var num large_counter = 0;
    while "$large_counter$ < 100" method="schedule" {
        say Processing item $large_counter$;
        large_counter = large_counter + 10;
    }
}

function "helper" {
    say Helper function called;
    level = level + 1;
    say New level: $level$;
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

tag item "example:tools" {
    add "minecraft:diamond_pickaxe";
    add "minecraft:diamond_axe";
}
```

## Best Practices

1. **Use descriptive names**: Choose clear, descriptive names for functions and variables
2. **Organize with namespaces**: Use namespaces to group related functions
3. **Comment your code**: Add comments to explain complex logic
4. **Test incrementally**: Build and test your datapack as you develop
5. **Use variable substitution**: Use `$variable$` syntax for clean, readable code
6. **Keep it simple**: The simplified language is designed to be reliable and easy to understand

## Common Patterns

### Counter Pattern

```mdl
var num counter = 0;

function "increment" {
    counter = counter + 1;
    say Counter: $counter$;
}
```

### Health Management

```mdl
var num health = 20;

function "check_health" {
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
    }
}
```

### Level System

```mdl
var num level = 1;
var num experience = 0;

function "gain_experience" {
    experience = experience + 10;
    if "$experience$ >= 100" {
        level = level + 1;
        experience = 0;
        say Level up! New level: $level$;
    }
}
```

This **simplified** language focuses on **control structures and number variables** that actually work, making it much easier to create reliable Minecraft datapacks.
