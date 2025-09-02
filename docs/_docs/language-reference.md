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

// Assignment with explicit scope
counter<global> = 42;
playerScore<@s> = playerScore<@s> + 10;
teamScore<@a[team=red]> = 5;
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

MDL uses an **explicit scope system** where each variable access must specify its scope. This makes code more readable and eliminates hidden state.

**Benefits of Explicit Scopes:**
- **No hidden state** - You always see exactly what scope you're using
- **No scope tracking bugs** - Each access is self-contained
- **More readable** - `variable<@s>` is clear and explicit
- **Easier to debug** - No need to trace back where a variable was declared
- **Consistent behavior** - Variables always behave the same way regardless of context

### Variable Declaration Scopes
- **No scope specified** - Player-specific (defaults to `@s` in execution context)
- `scope<global>` - Server-wide (stored on server armor stand)
- `scope<@a>` - All players
- `scope<@a[team=red]>` - Team-specific
- `scope<@e[type=armor_stand,tag=something,limit=1]>` - Custom entity

### Variable Access with Explicit Scopes
```mdl
// Each variable access must specify the scope
counter<global> = 42;                    // Access global counter
playerScore<@s> = playerScore<@s> + 10;  // Access player-specific score
teamScore<@a[team=red]> = 5;            // Access team-specific score

// Variables in strings automatically use their declared scopes
say Global: $counter$, Player: $playerScore$, Team: $teamScore$;
```

### Function Call Scopes
```mdl
// Execute as specific selector
function "namespace:function_name<@a>";           // All players
function "namespace:function_name<@s>";           // Current player
function "namespace:function_name<@a[team=red]>"; // Red team players
```

## Explicit Scope System Details

### How It Works

The explicit scope system ensures that every variable access is clear and unambiguous:

1. **Declaration**: Variables declare their scope when defined
   ```mdl
   var num globalVar scope<global> = 0;           // Global scope
   var num playerVar = 0;                         // Player scope (defaults to @s)
   var num teamVar scope<@a[team=red]> = 0;      // Team scope
   ```

2. **Access**: Every variable access must specify the scope
   ```mdl
   globalVar<global> = 42;                        // Access global variable
   playerVar<@s> = playerVar<@s> + 10;           // Access player variable
   teamVar<@a[team=red]> = 5;                    // Access team variable
   ```

3. **String Substitution**: Variables in strings automatically use their declared scopes
   ```mdl
   say Global: $globalVar$, Player: $playerVar$;  // Automatic scope resolution
   ```

4. **Explicit Scopes in Conditions**: Override declared scopes in if/while conditions
   ```mdl
   if "$playerVar<@s>$ > 10" {              // Explicit scope in condition
       say "Player score is high!";
   }
   
   if "$globalVar<global>$ > 100" {         // Global scope in condition
       say "Global counter reached!";
   }
   
   if "$teamVar<@a[team=red]>$ > 50" {      // Team scope in condition
       say "Red team is winning!";
   }
   ```

### Scope Mapping

MDL maps scopes to Minecraft selectors:

| MDL Scope | Minecraft Selector | Description |
|-----------|-------------------|-------------|
| `scope<global>` | `@e[type=armor_stand,tag=mdl_server,limit=1]` | Server-wide storage |
| `scope<@s>` | `@s` | Current player |
| `scope<@a>` | `@a` | All players |
| `scope<@a[team=red]>` | `@a[team=red]` | Red team players |
| `scope<@e[type=armor_stand,tag=something,limit=1]>` | `@e[type=armor_stand,tag=something,limit=1]` | Custom entity |

### Best Practices

- **Be explicit**: Always specify the scope when accessing variables
- **Use meaningful names**: `playerScore<@s>` is clearer than `score<@s>`
- **Group related variables**: Use consistent scopes for related data
- **Document complex scopes**: Add comments for non-standard selectors

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

### Counter with Explicit Scoped Variables
```mdl
pack "counter" "Counter example" 82;
namespace "counter";

var num globalCounter scope<global> = 0;
var num playerCounter = 0;  // Defaults to player-specific scope

function "increment" {
    globalCounter<global> = globalCounter<global> + 1;
    playerCounter<@s> = playerCounter<@s> + 1;
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
    counter<global> = 5;
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter<global> = counter<global> - 1;
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
    }
}

// Timer function
function "update_timer" {
    globalTimer<global> = globalTimer<global> + 1;
    if "$globalTimer$ >= 1200" {  // 60 seconds
        globalTimer<global> = 0;
        say Time's up! Final score: $score$;
    }
}

// Hooks
on_load "game:start_game";
on_tick "game:update_timer";
```
