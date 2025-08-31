---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

# Getting Started with MDL

MDL (Minecraft Datapack Language) is a simple language that compiles to Minecraft datapack `.mcfunction` files.

## Installation

Install MDL using pipx:

```bash
pipx install minecraft-datapack-language
```

## Quick Start

Create your first MDL file:

```mdl
// hello.mdl
pack "hello" "My first datapack" 82;
namespace "hello";

function "main" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load "hello:main";
```

Compile it:

```bash
mdl build --mdl hello.mdl -o dist
```

The compiled datapack will be in the `dist` folder. Copy it to your Minecraft world's `datapacks` folder and run `/reload` in-game.

## Basic Concepts

### Variables

Variables store numbers and can be scoped to different entities:

```mdl
// Player-specific variable (default)
var num playerScore = 0;

// Server-wide variable
var num globalCounter scope<global> = 0;

// Team-specific variable
var num teamScore scope<@a[team=red]> = 0;
```

### Variable Substitution

Use `$variable$` to read variable values:

```mdl
say Your score: $playerScore$;
tellraw @a {"text":"Global counter: $globalCounter$","color":"gold"};

if "$playerScore$ > 100" {
    say High score!;
}
```

### Functions

Functions contain Minecraft commands:

```mdl
function "my_function" {
    say This is my function!;
    effect give @s minecraft:speed 10 1;
}

// Call a function
function "hello:my_function";

// Call a function for all players
function "hello:my_function<@a>";
```

### Control Structures

MDL supports real if/else statements and while loops:

```mdl
// If statement
if "$playerScore$ > 50" {
    say Great job!;
} else {
    say Keep trying!;
}

// While loop
while "$counter$ < 5" {
    say Counter: $counter$;
    counter = counter + 1;
}
```

### Hooks

Automatically run functions:

```mdl
on_load "hello:init";    // Runs when datapack loads
on_tick "hello:update";  // Runs every tick
```

## Complete Example

Here's a complete example that demonstrates all the basic features:

```mdl
pack "example" "Complete example" 82;
namespace "example";

// Variables
var num playerScore scope<@s> = 0;
var num globalTimer scope<global> = 0;

// Initialize function
function "init" {
    playerScore = 0;
    globalTimer = 0;
    say Game initialized!;
}

// Update function
function "update" {
    globalTimer = globalTimer + 1;
    
    if "$playerScore$ > 100" {
        say High score!;
        tellraw @a {"text":"Player has a high score!","color":"gold"};
    }
    
    if "$globalTimer$ >= 1200" {  // 60 seconds
        globalTimer = 0;
        say Time's up!;
    }
}

// Score function
function "add_score" {
    playerScore = playerScore + 10;
    say Score: $playerScore$;
}

// Hooks
on_load "example:init";
on_tick "example:update";
```

## Building and Testing

### Single File
```bash
mdl build --mdl myfile.mdl -o dist
```

### Multiple Files
```bash
mdl build --mdl "file1.mdl file2.mdl" -o dist
```

### Directory
```bash
mdl build --mdl myproject/ -o dist
```

### Testing
1. Copy the `dist` folder to your Minecraft world's `datapacks` folder
2. Run `/reload` in-game
3. Test your functions with `/function namespace:function_name`

## Next Steps

- Read the [Language Reference](language-reference.md) for complete syntax
- Check out [Examples](examples.md) for more complex examples
- Learn about [Multi-file Projects](multi-file-projects.md) for larger datapacks