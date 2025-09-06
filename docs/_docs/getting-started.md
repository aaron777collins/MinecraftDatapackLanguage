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

function hello:main<@s> {
    say "Hello, Minecraft!";
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load hello:main<@s>;
```

Compile it:

```bash
mdl build --mdl hello.mdl -o dist
```

The compiled datapack will be in the `dist` folder. Copy it to your Minecraft world's `datapacks` folder and run `/reload` in-game.

## Basic Concepts

### Variables

Variables store numbers and can be scoped to different entities. MDL uses an **explicit scope system** where you must specify the scope each time you access a variable:

```mdl
// Player-specific variable (default)
var num playerScore<@s> = 0;

// Server-wide variable
var num globalCounter<@a> = 0;

// Team-specific variable
var num teamScore<@a[team=red]> = 0;

// Access variables with explicit scopes
playerScore<@s> = 42;                    // Player scope
globalCounter<@a> = 100;                 // Global scope
teamScore<@a[team=red]> = 5;            // Team scope
```

### Variable Substitution

Use `$variable$` to read variable values. Variables automatically resolve to their declared scopes:

```mdl
say "Your score: $playerScore<@s>$";
tellraw @a {"text":"Global counter: $globalCounter<@a>$","color":"gold"};

if $playerScore<@s>$ > 100 {
    say "High score!";
}
```

### Functions

Functions contain Minecraft commands:

```mdl
function hello:my_function<@s> {
    say "This is my function!";
    effect give @s minecraft:speed 10 1;
}

// Call a function
exec hello:my_function<@s>;

// Call a function for all players
exec hello:my_function<@a>;

// Function Macros (1.21+)
// Define a macro line using $ and placeholders like $(name)
function hello:greet<@s> {
    $ say Hello $(name)!
}

// Pass arguments via JSON compound (quoted in MDL)
exec hello:greet<@s> "{name:\"Alex\"}";

// Or via data source with 'with'
exec hello:greet<@s> with storage my:data player.name;
```

### Control Structures

MDL supports real if/else statements and while loops:

```mdl
// If statement
if $playerScore<@s>$ > 50 {
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

### Explicit Scopes in Conditions

You can override variable scopes in conditions using explicit scope selectors:

```mdl
// Check current player's score
if "$playerScore<@s>$ > 50" {
    say "Your score is high!";
}

// Check global counter
if "$globalCounter<global>$ > 100" {
    say "Global milestone reached!";
}

// Check another player's score
if "$playerScore<@p[name=Steve]>$ > 20" {
    say "Steve has a good score!";
}

// Check team score
if "$teamScore<@a[team=red]>$ > 50" {
    say "Red team is winning!";
}
```

This allows you to check variables across different scopes without changing their declared scope.

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
var num playerScore = 0;  // Defaults to player-specific scope
var num globalTimer<@a> = 0;

// Initialize function
function "init" {
    playerScore<@s> = 0;
    globalTimer<global> = 0;
    say Game initialized!;
}

// Update function
function "update" {
    globalTimer<global> = globalTimer<global> + 1;
    
    if "$playerScore$ > 100" {
        say High score!;
        tellraw @a {"text":"Player has a high score!","color":"gold"};
    }
    
    if "$globalTimer$ >= 1200" {  // 60 seconds
        globalTimer<global> = 0;
        say Time's up!;
    }
}

// Score function
function "add_score" {
    playerScore<@s> = playerScore<@s> + 10;
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