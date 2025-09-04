---
layout: page
title: MDL Examples
permalink: /docs/examples/
---

This page contains working examples of MDL features.

## Basic Hello World

A simple datapack that says hello when loaded:

```mdl
pack "hello" "A simple hello world datapack" 82;
namespace "hello";

function hello:main<@s> {
    say "Hello, Minecraft!";
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load hello:main<@s>;
```

## Counter with Scoped Variables

Demonstrates variables with different scopes:

```mdl
pack "counter" "Counter example" 82;
namespace "counter";

var num globalCounter<@a> = 0;
var num playerCounter<@s> = 0;  // Defaults to player-specific scope

function counter:increment<@s> {
    globalCounter<@a> = $globalCounter<@a>$ + 1;
    playerCounter<@s> = $playerCounter<@s>$ + 1;
    say "Global: $globalCounter<@a>$, Player: $playerCounter<@s>$";
}

function counter:show_all<@s> {
    exec counter:increment<@a>;
}

on_load counter:increment<@s>;
```

## While Loop Example

A countdown timer using a while loop:

```mdl
pack "loops" "Loop example" 82;
namespace "loops";

var num counter<@a> = 0;

function loops:countdown<@s> {
    counter<@a> = 5;
    while $counter<@a>$ > 0 {
        say "Countdown: $counter<@a>$";
        counter<@a> = $counter<@a>$ - 1;
    }
    say "Blast off!";
}

on_load loops:countdown<@s>;
```

## Raw Commands

Using raw Minecraft commands:

```mdl
pack "raw" "Raw command example" 82;
namespace "raw";

function raw:custom<@s> {
    // Use raw Minecraft commands
    effect give @s minecraft:speed 10 1;
    particle minecraft:explosion ~ ~ ~ 1 1 1 0 10;
    playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1;
}

on_load raw:custom<@s>;
```

## Complete Game Example

A complete game with scoring, levels, and timers:

```mdl
pack "game" "Complete game example" 82;
namespace "game";

// Variables
var num score<@s> = 0;  // Defaults to player-specific scope
var num level<@s> = 1;  // Defaults to player-specific scope
var num globalTimer<@a> = 0;

// Main game function
function "start_game" {
    score<@s> = 0;
    level<@s> = 1;
            say "Game started! Level: $level<@s>$, Score: $score<@s>$";
}

// Level up function
function "level_up" {
    if $score<@s>$ >= 100 {
        level<@s> = level<@s> + 1;
        score<@s> = score<@s> - 100;
        say "Level up! New level: $level<@s>$";
        tellraw @a {"text":"Player leveled up!","color":"gold"};
    }
}

// Timer function
function "update_timer" {
    globalTimer<global> = globalTimer<global> + 1;
    if $globalTimer<@a>$ >= 1200 {  // 60 seconds
        globalTimer<global> = 0;
        say "Time's up! Final score: $score<@s>$";
    }
}

// Add score function
function "add_score" {
    score<@s> = score<@s> + 10;
            say "Score: $score<@s>$";
    function "game:level_up";
}

// Hooks
on_load "game:start_game";
on_tick "game:update_timer";
```

## Team-Based System

A system that tracks team scores:

```mdl
pack "teams" "Team system example" 82;
namespace "teams";

// Team variables
var num redScore<@a[team=red]> = 0;
var num blueScore<@a[team=blue]> = 0;
var num gameTimer<@a> = 0;

// Initialize teams
function "init" {
    redScore<@a[team=red]> = 0;
    blueScore<@a[team=blue]> = 0;
    gameTimer<global> = 0;
    say Team game initialized!;
}

// Update game
function "update" {
    gameTimer<global> = gameTimer<global> + 1;
    
    if $gameTimer<@a>$ >= 2400 {  // 2 minutes
        gameTimer<global> = 0;
        say "Game over! Red: $redScore<@a[team=red]>$, Blue: $blueScore<@a[team=blue]>$";
        
        if $redScore<@a[team=red]>$ > $blueScore<@a[team=blue]>$ {
            tellraw @a {"text":"Red team wins!","color":"red"};
        } else if $blueScore<@a[team=blue]>$ > $redScore<@a[team=red]>$ {
            tellraw @a {"text":"Blue team wins!","color":"blue"};
        } else {
            tellraw @a {"text":"It's a tie!","color":"yellow"};
        }
    }
}

// Add points to red team
function "red_point" {
    redScore<@a[team=red]> = redScore<@a[team=red]> + 1;
            say "Red team score: $redScore<@a[team=red]>$";
}

// Add points to blue team
function "blue_point" {
    blueScore<@a[team=blue]> = blueScore<@a[team=blue]> + 1;
            say "Blue team score: $blueScore<@a[team=blue]>$";
}

// Hooks
on_load "teams:init";
on_tick "teams:update";
```

## Multi-File Example

Organizing code across multiple files:

**`main.mdl`** (with pack declaration):
```mdl
pack "multifile" "Multi-file example" 82;
namespace "core";

var num playerCount<@a> = 0;

function "init" {
    playerCount = 0;
    say Core system initialized!;
}

on_load "core:init";
```

**`ui.mdl`** (no pack declaration needed):
```mdl
namespace "ui";

function "show_hud" {
    tellraw @a {"text":"Players: $playerCount<@a>$","color":"green"};
}

function "update_hud" {
    function "ui:show_hud<@a>";
}
```

**`game.mdl`** (no pack declaration needed):
```mdl
namespace "game";

function "start" {
    say Game started!;
    function "ui:update_hud";
}
```

Build all files together:
```bash
mdl build --mdl "main.mdl ui.mdl game.mdl" -o dist
```

## Explicit Scopes in Conditions

Demonstrates how to use explicit scope selectors in if/while conditions to override declared variable scopes:

```mdl
pack "scopes" "Explicit scope conditions example" 82;
namespace "scopes";

// Variables with different scopes
var num playerScore = 0;                    // Defaults to @s
var num globalCounter<@a> = 0;                  // Global scope
var num teamScore<@a[team=red]> = 0;            // Team scope

function "main" {
    // Test explicit scope overrides in if conditions
    if "$playerScore<@s>$ > 10" {
        say "Current player score is high!";
    }
    
    if "$globalCounter<global>$ > 100" {
        say "Global counter reached milestone!";
    }
    
    if "$teamScore<@a[team=red]>$ > 50" {
        say "Red team is winning!";
    }
    
    // Check another player's score
    if "$playerScore<@p[name=Steve]>$ > 5" {
        say "Steve has a good score!";
    }
    
    // Check if any player has a high score
    if "$playerScore<@a>$ > 20" {
        say "Someone has a very high score!";
    }
    
    // Use explicit scopes in while loops too
    while "$globalCounter<global>$ < 10" {
        globalCounter<global> = globalCounter<global> + 1;
        say "Counter: $globalCounter<@a>$";
    }
}

// Function to test different scopes
function "test_scopes" {
    // Set different values for different scopes
    playerScore<@s> = 15;                    // Current player
    globalCounter<global> = 150;             // Global
    teamScore<@a[team=red]> = 75;           // Red team
    
    // Test conditions with explicit scopes
    if "$playerScore<@s>$ > 10" {
        say "Player score check passed!";
    }
    
    if "$globalCounter<global>$ > 100" {
        say "Global counter check passed!";
    }
    
    if "$teamScore<@a[team=red]>$ > 50" {
        say "Team score check passed!";
    }
}

on_load "scopes:main";
```

**Key Features:**
- **Override declared scopes**: Use `<@s>`, `<global>`, `<@a[team=red]>` in conditions
- **Check other entities**: Compare scores across different players/teams
- **Flexible conditions**: Mix and match scopes as needed
- **Clear intent**: Explicit scope makes code more readable and debuggable


