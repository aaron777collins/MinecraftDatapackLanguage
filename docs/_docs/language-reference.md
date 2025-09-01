---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

MDL (Minecraft Datapack Language) is a simple language that compiles to Minecraft datapack `.mcfunction` files.

## Basic Syntax

### Pack Declaration
```mdl
pack "pack_name" "description" pack_format;
```

### Namespace Declaration
```mdl
namespace "namespace_name";
```

### Variables
```mdl
// Declare variables with scope
var num counter scope<global> = 0;
var num playerScore = 0;  // Defaults to player-specific scope
var num teamScore scope<@a[team=red]> = 0;

// Assignment
counter = 42;
playerScore = playerScore + 10;
```

### Variable Substitution
```mdl
// In strings and commands
say Counter: $counter$;
tellraw @a {"text":"Score: $playerScore$","color":"gold"};

// In conditions
if "$playerScore$ > 100" {
    say High score!;
}
```

### Functions
```mdl
function "function_name" {
    say Hello World;
    tellraw @a {"text":"Welcome!","color":"green"};
}

// Call functions
function "namespace:function_name";

// Call functions with scope
function "namespace:function_name<@a>";
```

### Control Structures

#### If Statements
```mdl
if "$counter$ > 5" {
    say Counter is high!;
}

if "$health$ < 10" {
    say Health is low!;
} else {
    say Health is good;
}
```

#### While Loops
```mdl
while "$counter$ < 10" {
    counter = counter + 1;
    say Counter: $counter$;
}
```

### Raw Command Blocks
```mdl
// Raw blocks allow direct Minecraft commands without MDL processing
$!raw
scoreboard players set @s player_timer_enabled 1
execute as @a run function mypack:increase_tick_per_player
say "Raw commands bypass MDL syntax checking"
raw!$

// Single-line raw commands
$!raw scoreboard players add @s player_tick_counter 1 raw!$

// Mix MDL and raw commands
say "This is MDL syntax";
$!raw scoreboard players set @s player_timer_enabled 1 raw!$
say "Back to MDL syntax";
```

**Use cases for raw blocks:**
- Complex `execute` commands that MDL doesn't support
- Direct scoreboard operations
- Commands with special syntax that conflicts with MDL
- Legacy Minecraft commands not yet supported by MDL

### Hooks
```mdl
on_load "namespace:function_name";    // Runs when datapack loads
on_tick "namespace:function_name";    // Runs every tick
```

## Scope System

### Variable Scopes
- **No scope specified** - Player-specific (defaults to `@s` in execution context)
- `scope<global>` - Server-wide (stored on server armor stand)
- `scope<@a>` - All players
- `scope<@a[team=red]>` - Team-specific
- `scope<@e[type=armor_stand,tag=something,limit=1]>` - Custom entity

### Function Call Scopes
```mdl
// Execute as specific selector
function "namespace:function_name<@a>";           // All players
function "namespace:function_name<@s>";           // Current player
function "namespace:function_name<@a[team=red]>"; // Red team players
```

## Examples

### Basic Hello World
```mdl
pack "hello" "A simple hello world datapack" 82;
namespace "hello";

function "main" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load "hello:main";
```

### Counter with Scoped Variables
```mdl
pack "counter" "Counter example" 82;
namespace "counter";

var num globalCounter scope<global> = 0;
var num playerCounter = 0;  // Defaults to player-specific scope

function "increment" {
    globalCounter = globalCounter + 1;
    playerCounter = playerCounter + 1;
    say Global: $globalCounter$, Player: $playerCounter$;
}

function "show_all" {
    function "counter:increment<@a>";
}
```

### While Loop Example
```mdl
pack "loops" "Loop example" 82;
namespace "loops";

var num counter scope<global> = 0;

function "countdown" {
    counter = 5;
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter = counter - 1;
    }
    say Blast off!;
}
```

### Raw Commands
```mdl
pack "raw" "Raw command example" 82;
namespace "raw";

function "custom" {
    // Use raw Minecraft commands
    effect give @s minecraft:speed 10 1;
    particle minecraft:explosion ~ ~ ~ 1 1 1 0 10;
    playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1;
}

function "raw_example" {
    // Raw blocks allow direct Minecraft commands without MDL processing
    $!raw
    scoreboard players set @s player_timer_enabled 1
    execute as @a run function raw:increase_tick_per_player
    say "Raw commands bypass MDL syntax checking"
    raw!$
    
    // You can mix MDL and raw commands
    say "This is MDL syntax";
    $!raw scoreboard players add @s player_tick_counter 1 raw!$
    say "Back to MDL syntax";
}
```

### Complete Example
```mdl
pack "game" "Complete game example" 82;
namespace "game";

// Variables
var num score = 0;  // Defaults to player-specific scope
var num level = 1;  // Defaults to player-specific scope
var num globalTimer scope<global> = 0;

// Main game function
function "start_game" {
    score = 0;
    level = 1;
    say Game started! Level: $level$, Score: $score$;
}

// Level up function
function "level_up" {
    if "$score$ >= 100" {
        level = level + 1;
        score = score - 100;
        say Level up! New level: $level$;
        tellraw @a {"text":"Player leveled up!","color":"gold"};
    }
}

// Timer function
function "update_timer" {
    globalTimer = globalTimer + 1;
    if "$globalTimer$ >= 1200" {  // 60 seconds
        globalTimer = 0;
        say Time's up! Final score: $score$;
    }
}

// Hooks
on_load "game:start_game";
on_tick "game:update_timer";
```
