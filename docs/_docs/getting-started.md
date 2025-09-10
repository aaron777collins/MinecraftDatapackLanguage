---
layout: page
title: Getting Started
permalink: /docs/getting-started/
---

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

function hello:main {
    say "Hello, Minecraft!";
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load hello:main;
```

Compile it:

```bash
mdl build --mdl hello.mdl -o dist
```

The compiled datapack will be in the `dist` folder. Copy it to your Minecraft world's `datapacks` folder and run `/reload` in-game.

## Basic Concepts

### Variables

Variables store numbers and can be scoped to different entities. MDL uses an **explicit scope system** where scopes can be specified explicitly, but are optional; when omitted, the scope defaults to `@s` (current entity):

```mdl
// Player-specific variable (default @s)
var num playerScore = 0;

// Server-wide/global variable (singleton armor stand)
var num globalCounter<global> = 0;

// Team-specific variable
var num teamScore<@a[team=red]> = 0;

// Access variables (explicit or default scopes)
playerScore = 42;                         // Defaults to @s
globalCounter<global> = 100;              // Global scope
teamScore<@a[team=red]> = 5;              // Team scope
```

### Variable Substitution

Use `$variable$` or `$variable<scope>$` to read variable values. If the scope is omitted, it defaults to `@s`:

```mdl
say "Your score: $playerScore$";
tellraw @a {"text":"Global counter: $globalCounter<global>$","color":"gold"};

if $playerScore$ > 100 {
    say "High score!";
}
```

### Functions

Functions contain Minecraft commands:

```mdl
function hello:my_function {
    say "This is my function!";
    effect give @s minecraft:speed 10 1;
}

// Call a function
exec hello:my_function<@s>;

// Call a function for all players
exec hello:my_function<@a>;
```

### Control Structures

MDL supports real if/else statements and while loops:

```mdl
// If statement
if $playerScore$ > 50 {
    say "Great job!";
} else {
    say "Keep trying!";
}

// While loop
while $counter$ < 5 {
    say "Counter: $counter$";
    counter = counter + 1;
}
```

### Reading with Explicit Selectors

You can read variables using explicit selectors in conditions without affecting how they were declared:

```mdl
// Check current player's score
if $playerScore<@s>$ > 50 {
    say "Your score is high!";
}

// Check global counter
if $globalCounter<global>$ > 100 {
    say "Global milestone reached!";
}

// Check another player's score
if $playerScore<@p[name=Steve]>$ > 20 {
    say "Steve has a good score!";
}

// Check team score
if $teamScore<@a[team=red]>$ > 50 {
    say "Red team is winning!";
}
```

This allows you to read variables at different selectors without any special linkage to where they were declared.

### Hooks

Automatically run functions:

```mdl
on_load hello:init;    // Runs when datapack loads
on_tick hello:update;  // Runs every tick
```

## Complete Example

Here's a complete example that demonstrates all the basic features:

```mdl
pack "example" "Complete example" 82;
namespace "example";

// Variables
var num playerScore = 0;  // Defaults to player-specific scope (@s)
var num globalTimer<global> = 0;

// Initialize function
function "init" {
    playerScore = 0;
    globalTimer<global> = 0;
    say "Game initialized!";
}

// Update function
function "update" {
    globalTimer<global> = globalTimer<global> + 1;
    
    if $playerScore$ > 100 {
        say "High score!";
        tellraw @a {"text":"Player has a high score!","color":"gold"};
    }
    
    if $globalTimer<global>$ >= 1200 {  // 60 seconds
        globalTimer<global> = 0;
        say "Time's up!";
    }
}

// Score function
function "add_score" {
    playerScore = playerScore + 10;
    say "Score: $playerScore$";
}

// Hooks
on_load example:init;
on_tick example:update;
```

## Building and Testing

### Single File
```bash
mdl build --mdl myfile.mdl -o dist
```

### Build a directory (multiple files)
```bash
mdl build --mdl . -o dist
```

### Directory (explicit path)
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