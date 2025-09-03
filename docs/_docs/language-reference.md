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
var num counter<@a> = 0;           // Global scope - accessible by all players
var num playerScore<@s> = 0;       // Player-specific scope - accessible by current player
var num teamScore<@a[team=red]> = 0; // Team scope - accessible by red team players

// Assignment with scope selectors
counter<@a> = 42;                  // Set global counter
playerScore<@s> = playerScore<@s> + 10; // Access and modify player score
teamScore<@a[team=red]> = 5;      // Set team score

// Access variables with different scopes than declared
counter<@s> = counter<@a>;         // Read global counter, set player counter
playerScore<@a> = playerScore<@s>; // Read player score, set global score
```

### Variable Substitution
```mdl
// In strings and commands - variables are automatically resolved to their declared scopes
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

MDL uses a **flexible scope system** where variables can be declared with one scope and accessed with different scopes. This provides powerful data sharing capabilities while maintaining clear scope semantics.

**Benefits of Flexible Scopes:**
- **Declare once, access anywhere** - Set up data structures at one scope level
- **Flexible data sharing** - Read global data at player level, or player data at global level
- **Efficient data management** - Store data at the most appropriate scope
- **Clear data flow** - Always see exactly what scope you're reading from and writing to
- **No hidden state** - Each access explicitly shows the scope being used

### Variable Declaration Scopes
- **Global scope** - `var num counter<@a> = 0;` - Server-wide storage
- **Player scope** - `var num playerScore<@s> = 0;` - Player-specific storage
- **Team scope** - `var num teamScore<@a[team=red]> = 0;` - Team-specific storage
- **Custom scope** - `var num entityScore<@e[type=armor_stand,tag=scoreboard,limit=1]> = 0;` - Custom entity storage

### Variable Access with Flexible Scopes
```mdl
// Declare variables at appropriate scopes
var num globalCounter<@a> = 0;           // Global counter
var num playerHealth<@s> = 20;           // Player health
var num teamScore<@a[team=red]> = 0;     // Red team score

// Access variables with different scopes than declared
globalCounter<@s> = globalCounter<@a>;   // Read global, set player
playerHealth<@a> = playerHealth<@s>;     // Read player, set global
teamScore<@s> = teamScore<@a[team=red]>; // Read team, set player

// Complex data flow
if "$playerHealth<@s>$ < 10" {
    globalCounter<@a> = globalCounter<@a> + 1;  // Increment global counter
    teamScore<@a[team=red]> = teamScore<@a[team=red]> + 5; // Award team points
}
```

### Function Call Scopes
```mdl
// Execute as specific selector
function "namespace:function_name<@a>";           // All players
function "namespace:function_name<@s>";           // Current player
function "namespace:function_name<@a[team=red]>"; // Red team players
```

## Flexible Scope System Details

### How It Works

The flexible scope system allows you to declare variables at one scope and access them at different scopes:

1. **Declaration**: Variables declare their storage scope when defined
   ```mdl
   var num globalVar<@a> = 0;                    // Stored globally
   var num playerVar<@s> = 0;                    // Stored per player
   var num teamVar<@a[team=red]> = 0;            // Stored per red team
   ```

2. **Access**: Variables can be accessed at any scope, regardless of where they were declared
   ```mdl
   globalVar<@s> = 42;                           // Read global, set player
   playerVar<@a> = playerVar<@s>;                // Read player, set global
   teamVar<@s> = teamVar<@a[team=red]>;          // Read team, set player
   ```

3. **String Substitution**: Variables in strings automatically use their declared scopes
   ```mdl
   say Global: $globalVar$, Player: $playerVar$;  // Automatic scope resolution
   ```

4. **Explicit Scopes in Conditions**: Override declared scopes in if/while conditions
   ```mdl
   if "$playerVar<@s>$ > 10" {                   // Explicit player scope in condition
       say "Player score is high!";
   }
   
   if "$globalVar<@a>$ > 100" {                  // Global scope in condition
       say "Global counter reached!";
   }
   
   if "$teamVar<@a[team=red]>$ > 50" {           // Team scope in condition
       say "Red team is winning!";
   }
   ```

### Scope Mapping

MDL maps scopes to Minecraft selectors:

| MDL Scope | Minecraft Selector | Description |
|-----------|-------------------|-------------|
| `<@a>` | `@a` | All players (global storage) |
| `<@s>` | `@s` | Current player |
| `<@a[team=red]>` | `@a[team=red]` | Red team players |
| `<@e[type=armor_stand,tag=mdl_server,limit=1]>` | `@e[type=armor_stand,tag=mdl_server,limit=1]` | Custom entity |

### Best Practices

- **Declare at appropriate scope** - Store data where it makes most sense
- **Access flexibly** - Read from one scope, write to another as needed
- **Use meaningful names** - `playerScore<@s>` is clearer than `score<@s>`
- **Document complex scopes** - Add comments for non-standard selectors
- **Consider data flow** - Think about where data originates and where it needs to go

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

### Counter with Flexible Scoped Variables
```mdl
pack "counter" "Counter example" 82;
namespace "counter";

var num globalCounter<@a> = 0;           // Global counter
var num playerCounter<@s> = 0;           // Player-specific counter

function "increment" {
    globalCounter<@a> = globalCounter<@a> + 1;   // Increment global
    playerCounter<@s> = playerCounter<@s> + 1;   // Increment player
    
    // Access global data at player level
    say Global: $globalCounter$, Player: $playerCounter$;
}

function "show_all" {
    function "counter:increment<@a>";    // Run for all players
}

function "reset_player" {
    // Reset player counter to global value
    playerCounter<@s> = globalCounter<@a>;
    say Reset to global value: $playerCounter$;
}
```

### Team-Based Scoring System
```mdl
pack "teamgame" "Team game example" 82;
namespace "teamgame";

var num redTeamScore<@a[team=red]> = 0;     // Red team score
var num blueTeamScore<@a[team=blue]> = 0;   // Blue team score
var num playerScore<@s> = 0;                // Individual player score

function "award_points" {
    // Award points to both player and team
    playerScore<@s> = playerScore<@s> + 10;
    
    // Check team and award team points
    if "$player<@s> has team red" {
        redTeamScore<@a[team=red]> = redTeamScore<@a[team=red]> + 5;
        say Red team score: $redTeamScore$;
    } else if "$player<@s> has team blue" {
        blueTeamScore<@a[team=blue]> = blueTeamScore<@a[team=blue]> + 5;
        say Blue team score: $blueTeamScore$;
    }
    
    say Your score: $playerScore$;
}

function "show_leaderboard" {
    // Display all scores
    say === LEADERBOARD ===;
    say Red Team: $redTeamScore$;
    say Blue Team: $blueTeamScore$;
    say Your Score: $playerScore$;
}
```

### While Loop Example
```mdl
pack "loops" "Loop example" 82;
namespace "loops";

var num counter<@a> = 0;

function "countdown" {
    counter<@a> = 5;
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter<@a> = counter<@a> - 1;
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

// Variables with different scopes
var num score<@s> = 0;                    // Player-specific score
var num level<@s> = 1;                    // Player-specific level
var num globalTimer<@a> = 0;              // Global timer
var num highScore<@a> = 0;                // Global high score

// Main game function
function "start_game" {
    score<@s> = 0;
    level<@s> = 1;
    say Game started! Level: $level$, Score: $score$;
}

// Level up function
function "level_up" {
    if "$score$ >= 100" {
        level<@s> = level<@s> + 1;
        score<@s> = score<@s> - 100;
        say Level up! New level: $level$;
        tellraw @a {"text":"Player leveled up!","color":"gold"};
        
        // Update global high score if this player beats it
        if "$score<@s>$ > $highScore<@a>$" {
            highScore<@a> = score<@s>;     // Read player, set global
            say New high score: $highScore$;
        }
    }
}

// Timer function
function "update_timer" {
    globalTimer<@a> = globalTimer<@a> + 1;
    if "$globalTimer$ >= 1200" {  // 60 seconds
        globalTimer<@a> = 0;
        say Time's up! Final score: $score$;
        
        // Award bonus points based on global timer
        score<@s> = score<@s> + (globalTimer<@a> / 100);
    }
}

// Hooks
on_load "game:start_game";
on_tick "game:update_timer";
```
