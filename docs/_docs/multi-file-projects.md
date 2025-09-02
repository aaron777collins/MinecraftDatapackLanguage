---
layout: page
title: Multi File Projects
permalink: /docs/multi-file-projects/
---

MDL supports organizing code across multiple files for better project structure.

## Basic Multi-File Setup

### Main File (with pack declaration)

Only the first file needs a pack declaration:

```mdl
// main.mdl
pack "my_project" "A multi-file project" 82;
namespace "core";

var num playerCount scope<global> = 0;

function "init" {
    playerCount<global> = 0;
    say Core system initialized!;
}

on_load "core:init";
```

### Additional Files (no pack declaration)

Other files don't need pack declarations:

```mdl
// ui.mdl
namespace "ui";

function "show_hud" {
    tellraw @a {"text":"Players: $playerCount$","color":"green"};
}

function "update_hud" {
    function "ui:show_hud<@a>";
}
```

```mdl
// game.mdl
namespace "game";

function "start" {
    say Game started!;
    function "ui:update_hud";
}
```

## Building Multi-File Projects

### Build All Files Together

```bash
mdl build --mdl "main.mdl ui.mdl game.mdl" -o dist
```

### Build Entire Directory

```bash
mdl build --mdl myproject/ -o dist
```

### Build with Wildcards

```bash
mdl build --mdl "*.mdl" -o dist
```

## Namespace Organization

Each file can have its own namespace to prevent conflicts:

```mdl
// combat.mdl
namespace "combat";

var num damage = 10;  // Defaults to player-specific scope

function "attack" {
    say Attack damage: $damage$;
}
```

```mdl
// magic.mdl
namespace "magic";

var num mana = 100;  // Defaults to player-specific scope

function "cast_spell" {
    if "$mana$ >= 20" {
        mana<@s> = mana<@s> - 20;
        say Spell cast! Mana: $mana$;
    }
}
```

## Variable Sharing

Variables from all files are automatically merged:

```mdl
// core.mdl
var num globalTimer scope<global> = 0;
var num playerScore = 0;  // Defaults to player-specific scope
```

```mdl
// ui.mdl
function "show_stats" {
    tellraw @a {"text":"Timer: $globalTimer$, Score: $playerScore$","color":"gold"};
}
```

## Explicit Scopes in Conditions

When working with multiple files, you can use explicit scope selectors in conditions to check variables across different scopes:

```mdl
// core.mdl
var num globalTimer scope<global> = 0;
var num playerScore = 0;  // Defaults to player-specific scope

function "check_status" {
    // Check global timer
    if "$globalTimer<global>$ > 1000" {
        say "Game has been running for a while!";
    }
    
    // Check current player's score
    if "$playerScore<@s>$ > 50" {
        say "You have a high score!";
    }
    
    // Check if any player has a very high score
    if "$playerScore<@a>$ > 100" {
        say "Someone has an amazing score!";
    }
}
```

```mdl
// ui.mdl
function "show_leaderboard" {
    // Compare scores across different players
    if "$playerScore<@p[name=Alice]>$ > $playerScore<@p[name=Bob]>$" {
        tellraw @a {"text":"Alice is winning!","color":"green"};
    } else {
        tellraw @a {"text":"Bob is winning!","color":"blue"};
    }
}
```

This feature is especially useful in multi-file projects where you need to check variables across different scopes without changing their declared scope.

## Complete Multi-File Example

Here's a complete example with multiple files:

**`main.mdl`**:
```mdl
pack "adventure" "Adventure game" 82;
namespace "core";

var num gameState scope<global> = 0;
var num playerLevel = 1;  // Defaults to player-specific scope

function "init" {
    gameState<global> = 0;
    playerLevel<@s> = 1;
    say Adventure game initialized!;
}

on_load "core:init";
```

**`combat.mdl`**:
```mdl
namespace "combat";

var num playerHealth = 20;  // Defaults to player-specific scope

function "attack" {
    say Attacking! Health: $playerHealth$;
}

function "heal" {
    if "$playerHealth$ < 20" {
        playerHealth<@s> = playerHealth<@s> + 5;
        say Healed! Health: $playerHealth$;
    }
}
```

**`ui.mdl`**:
```mdl
namespace "ui";

function "show_status" {
    tellraw @a {"text":"Level: $playerLevel$, Health: $playerHealth$","color":"aqua"};
}

function "update_ui" {
    function "ui:show_status<@a>";
}
```

**`game.mdl`**:
```mdl
namespace "game";

function "start" {
    gameState<global> = 1;
    say Game started!;
    function "ui:update_ui";
}

function "level_up" {
    if "$playerLevel$ < 10" {
        playerLevel<@s> = playerLevel<@s> + 1;
        say Level up! New level: $playerLevel$;
    }
}
```

Build the project:
```bash
mdl build --mdl "main.mdl combat.mdl ui.mdl game.mdl" -o dist
```

## Best Practices

1. **One namespace per file**: Keep related functionality together
2. **Main file first**: Put the file with pack declaration first
3. **Clear naming**: Use descriptive file and namespace names
4. **Shared variables**: Declare shared variables in the main file
5. **Function organization**: Group related functions in the same file
6. **Proper scoping**: Use `scope<global>` for server-wide variables, no scope for player-specific variables
7. **Explicit scope access**: Always access variables with their scope like `variable<scope>`

## File Structure Example

```
my_project/
├── main.mdl          # Pack declaration, core variables
├── combat.mdl        # Combat system
├── magic.mdl         # Magic system
├── ui.mdl           # User interface
├── game.mdl         # Game logic
└── utils.mdl        # Utility functions
```
