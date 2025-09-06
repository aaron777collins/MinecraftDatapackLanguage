---
layout: page
title: Language Reference
permalink: /docs/language-reference/
---

# MDL (Minecraft Datapack Language) - Complete Language Reference

MDL is a simple, scope-aware language that compiles to Minecraft datapack `.mcfunction` files. This document defines the complete language specification.

## Core Language Design

### Philosophy
- **Explicit scoping**: Every variable operation specifies its scope with `<>` brackets
- **Clear reading vs writing**: Use `$variable<scope>$` for reading, `variable<scope>` for writing
- **No scope inheritance**: Each operation uses its own explicitly defined scope
- **Default scope**: When no scope specified, always use `@s` (current player)
- **No return values**: All functions are void - they execute commands and modify state
- **No quotes needed**: Use `$variable<scope>$` syntax directly instead of string literals
- **Function execution**: Use `exec` keyword to execute all functions
- **Tag-based resources**: Use tag syntax to reference datapack resources like recipes, loot tables, etc.
- **User-friendly communication**: `say` commands automatically convert to `tellraw` with proper JSON formatting
- **Real control flow**: If/else if/else statements and while loops that actually work and generate proper Minecraft conditional logic

## Basic Syntax

### Pack Declaration
```mdl
pack "pack_name" "description" pack_format;
```

### Namespace Declaration
```mdl
namespace "namespace_name";
```

### Tag Declarations
```mdl
// Recipe tags
tag recipe "RecipeName" "path/to/recipe.json";
tag recipe "diamond_sword" "recipes/diamond_sword.json";

// Loot table tags
tag loot_table "LootTableName" "path/to/loot_table.json";
tag loot_table "epic_loot" "loot_tables/epic_loot.json";

// Advancement tags
tag advancement "AdvancementName" "path/to/advancement.json";
tag advancement "first_spell" "advancements/first_spell.json";

// Item modifier tags
tag item_modifier "ItemModifierName" "path/to/item_modifier.json";
tag item_modifier "enchant_tool" "item_modifiers/enchant_tool.json";

// Predicate tags
tag predicate "PredicateName" "path/to/predicate.json";
tag predicate "has_mana" "predicates/has_mana.json";

// Structure tags
tag structure "StructureName" "path/to/structure.json";
tag structure "custom_house" "structures/custom_house.json";
```

### Variable Declaration
```mdl
// Declare variables with explicit scope
var num player_score<@a> = 0;                    // Global scope - accessible by all players
var num player_health<@s> = 20;                  // Player-specific scope
var num team_score<@a[team=red]> = 0;            // Team scope
var num entity_data<@e[type=armor_stand,tag=mdl_server,limit=1]> = 0; // Custom entity scope
```

### Variable Assignment
```mdl
// Always specify scope for assignments
player_score<@s> = $player_score<@s>$ + 1;       // Add 1 to current player's score
player_health<@a> = $player_health<@s>$;         // Read from @s, write to @a
team_score<@a[team=red]> = 5;                   // Set red team score to 5

// Default scope is @s when not specified
player_score = 0;                                // Same as player_score<@s> = 0;
```

### Variable Substitution
```mdl
// Use $variable<scope>$ syntax anywhere in the code
tellraw @s {"text":"You have ","extra":[{"score":{"name":"@s","objective":"player_score"}}," points"]};
execute if score @s player_score matches 10.. run game:celebrate;

// In conditions
if $player_score<@s>$ > 10 {
    player_score<@s> = 0;
}
```

### Say Commands (Auto-converted to tellraw)
```mdl
// Simple say commands automatically convert to tellraw with JSON formatting
say "Welcome to the game!";
say "You have $player_score<@s>$ points!";
say "Team score: $team_score<@a[team=red]>$";

// These get converted to:
// tellraw @a {"text":"Welcome to the game!"};
// tellraw @a {"text":"You have ","extra":[{"score":{"name":"@s","objective":"player_score"}}," points!"]};
// tellraw @a {"text":"Team score: ","extra":[{"score":{"name":"@s","objective":"team_score"}}]};
```

### Functions

#### Function Declaration
```mdl
// Basic function
function game:start_game {
    player_score<@s> = 0;
    player_health<@s> = 20;
}

// Function declaration (no scope on definition)
function game:reset_player {
    player_score<@s> = 0;
    player_health<@s> = 20;
}
```

#### Function Calls
```mdl
// Execute function with exec keyword (runs any function, with or without scope)
exec game:reset_player;                          // Execute function
exec game:start_game;                            // Execute any function
exec utils:calculator;                           // Execute from different namespace
exec game:reset_player<@s>;                      // Execute function with scope
exec game:reset_player<@a>;                      // Execute function with different scope
```

#### Function Macros and Arguments (1.21+)

MDL supports Minecraft's Function Macros and new function call argument forms.

1) Define macro lines inside functions using `$` as the first non-space character. Use `$(variable)` placeholders inside the line.

```mdl
function game:say_hello<@s> {
    $ say Hello $(name) x$(times);
}
```

2) Call a function with a data compound (quoted in MDL, unquoted in generated mcfunction). You can use single quotes to avoid escaping:

```mdl
// MDL source (quotes are required; single quotes recommended to reduce escaping)
exec game:say_hello<@s> '{name:"Alex",times:3}';

// Generated mcfunction
// execute as @s run function game:say_hello {name:"Alex",times:3}
```

3) Call a function with a data source (with-clause):

```mdl
// MDL source
exec game:say_hello<@s> with storage my:bag player.info;

// Generated mcfunction
// execute as @s run function game:say_hello with storage my:bag player.info
```

Notes:
- The compound must provide all variables referenced in macro placeholders like `$(name)` and `$(times)`.
- Extra data in the compound is ignored at runtime by Minecraft.
- Calling a non-macro function with a compound is allowed; Minecraft will ignore the data at runtime.
- If substitution produces a syntax error in a line, Minecraft skips the entire function call at runtime.

### Control Structures

#### If Statements
```mdl
if $player_score<@s>$ > 10 {
    exec game:celebrate;
    player_score<@s> = 0;
}

if $player_health<@s>$ < 5 {
    exec game:heal;
} else {
    exec game:check_health;
}
```

#### Else If Statements
```mdl
if $player_score<@s>$ > 100 {
    exec game:celebrate;
    player_score<@s> = 0;
} else if $player_score<@s>$ > 50 {
    exec game:reward;
    player_score<@s> = $player_score<@s>$ + 10;
} else {
    exec game:encourage;
    player_score<@s>$ = $player_score<@s>$ + 5;
}
```

#### While Loops
```mdl
while $counter<@s>$ > 0 {
    counter<@s> = $counter<@s>$ - 1;
    exec game:countdown;
}
```

**Note:** All control structures generate proper Minecraft conditional logic using `execute if` commands and recursive function calls for loops. The compiler automatically handles nested structures and generates the appropriate Minecraft datapack commands.

### Hooks
```mdl
on_load game:start_game;                         // Runs when datapack loads
on_tick game:update_timer;                       // Runs every tick
```

**Note:** Hooks use the same function reference syntax as regular function calls, but they are processed at datapack load time, not during execution.

### Raw Blocks
```mdl
// Raw blocks pass through unchanged - no MDL processing
$!raw
scoreboard players set @s player_timer_enabled 1
execute as @a run function game:increase_tick_per_player
say "Raw commands bypass MDL syntax checking"
raw!$

// Single-line raw commands
$!raw scoreboard players add @s player_tick_counter 1 raw!$

// Raw blocks can contain any Minecraft commands, including complex execute chains
$!raw
execute as @a[team=red] at @s run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
execute as @a[team=blue] at @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1
raw!$
```

**Important:** Raw blocks are completely ignored by the MDL parser. They get copied directly to the output `.mcfunction` files without any processing. This means you can use any valid Minecraft command syntax inside raw blocks.

## Scope System

### Core Scope Rules

1. **Variable Writing**: Use `variable<scope>` for assignments and declarations
2. **Variable Reading**: Use `$variable<scope>$` for reading values
3. **Function Execution**: Use `exec` keyword to run any function (with or without scope)
4. **No Inheritance**: Functions do not inherit scope from their caller
5. **Default Scope**: When no scope specified, always use `@s` (current player)
6. **No Memory**: The system does not remember a variable's declared scope for subsequent operations

### Scope Usage Examples

```mdl
// VARIABLES: Clear distinction between reading and writing
var num score<@a> = 0;                    // Declare with scope
score<@s> = 5;                            // Write with scope
if $score<@a>$ > 10 { ... }               // Read with scope

// FUNCTIONS: Use exec keyword to run any function (with or without scope)
exec game:start;                          // Execute function
exec utils:helper;                        // Execute from different namespace
exec game:start<@a>;                      // Execute function with scope
```

### Scope Examples

```mdl
// Declare variable with global scope
var num global_counter<@a> = 0;

// Later operations - each specifies its own scope
global_counter<@s> = 5;                         // Set current player's counter to 5
global_counter<@a> = $global_counter<@a>$ + 1;  // Increment global counter
global_counter = 10;                            // Same as global_counter<@s> = 10 (defaults to @s)

// Function calls
exec game:increment;                            // Execute function
exec game:increment<@s>;                        // Execute function with scope
exec utils:helper;                              // Execute from different namespace
```

### Valid Scope Selectors

```mdl
// Basic selectors
<@s>        // Current player
<@a>        // All players
<@p>        // Nearest player
<@r>        // Random player

// Complex selectors
<@a[team=red]>                                    // Red team players
<@e[type=armor_stand,tag=mdl_server,limit=1]>    // Specific entity
<@s[distance=..5]>                                // Current player within 5 blocks

// Global scope (special case)
<global>                                           // Maps to @e[type=armor_stand,tag=mdl_server,limit=1]
```

## Mathematical Expressions

### Operators
```mdl
// Arithmetic
+ (addition)
- (subtraction)
* (multiplication)
/ (division)

// Comparison
== (equal)
!= (not equal)
> (greater than)
< (less than)
>= (greater than or equal)
<= (less than or equal)
```

### Expression Examples
```mdl
// Complex expressions with different scopes
player_score<@s> = $x<@a>$ + $y<@p>$ * $z<@r>$;

// Parentheses for precedence
player_score<@s> = ($x<@s>$ + $y<@s>$) * 2;

// Simple comparisons (no logical operators)
if $score<@s>$ > 10 {
    exec game:reward;
}
```

## Reserved Names

### Function Names to Avoid
- `load` - Conflicts with Minecraft's built-in load function
- `tick` - Conflicts with Minecraft's built-in tick function
- Any other names that might conflict with Minecraft's internal functions

### Alternative Naming
```mdl
// Instead of 'load', use:
function game:initialize { ... }
function game:setup { ... }
function game:start { ... }

// Instead of 'tick', use:
function game:update { ... }
function game:loop { ... }
function game:process { ... }
```

## Complete Examples

### Basic Counter with Tags
```mdl
pack "counter" "Counter example" 82;
namespace "counter";

// Tag declarations
tag recipe "diamond_sword" "recipes/diamond_sword.json";
tag loot_table "sword_loot" "loot_tables/sword_loot.json";
tag advancement "first_sword" "advancements/first_sword.json";

var num global_counter<@a> = 0;
var num player_counter<@s> = 0;

function "increment" {
    global_counter<@a> = $global_counter<@a>$ + 1;
    player_counter<@s> = $player_counter<@s>$ + 1;
    
    // Using tellraw for player-specific messages
    tellraw @s {"text":"Global: ","extra":[{"score":{"name":"@s","objective":"global_counter"}}," Player: ",{"score":{"name":"@s","objective":"player_counter"}}]};
    
    // Using say for broadcast messages (auto-converts to tellraw)
    say "Player $player_counter<@s>$ just incremented the counter!";
}

function "reset_player" {
    player_counter<@s> = 0;
    tellraw @s {"text":"Counter reset!"};
}

on_load "counter:increment";
```

### Team Game with Resources
```mdl
pack "teamgame" "Team game example" 82;
namespace "teamgame";

// Tag declarations
tag recipe "team_banner" "recipes/team_banner.json";
tag loot_table "team_reward" "loot_tables/team_reward.json";
tag advancement "team_win" "advancements/team_win.json";
tag item_modifier "team_boost" "item_modifiers/team_boost.json";

var num red_score<@a[team=red]> = 0;
var num blue_score<@a[team=blue]> = 0;
var num player_score<@s> = 0;

function "award_points" {
    player_score<@s> = $player_score<@s>$ + 10;
    
    if $player_score<@s>$ > 100 {
        red_score<@a[team=red]> = $red_score<@a[team=red]>$ + 10;
        tellraw @s {"text":"High score bonus! Red team score: ","extra":[{"score":{"name":"@s","objective":"red_score"}}]};
    } else if $player_score<@s>$ > 50 {
        red_score<@a[team=red]> = $red_score<@a[team=red]>$ + 5;
        tellraw @s {"text":"Medium score bonus! Red team score: ","extra":[{"score":{"name":"@s","objective":"red_score"}}]};
    } else {
        red_score<@a[team=red]> = $red_score<@a[team=red]>$ + 1;
        tellraw @s {"text":"Standard bonus! Red team score: ","extra":[{"score":{"name":"@s","objective":"red_score"}}]};
    }
    
    tellraw @s {"text":"Your score: ","extra":[{"score":{"name":"@s","objective":"player_score"}}]};
}

function "show_leaderboard" {
    tellraw @s {"text":"=== LEADERBOARD ==="};
    tellraw @s {"text":"Red Team: ","extra":[{"score":{"name":"@s","objective":"red_score"}}]};
    tellraw @s {"text":"Blue Team: ","extra":[{"score":{"name":"@s","objective":"blue_score"}}]};
    tellraw @s {"text":"Your Score: ","extra":[{"score":{"name":"@s","objective":"player_score"}}]};
}

function "countdown_timer" {
    var num timer<@s> = 10;
    
    while $timer<@s>$ > 0 {
        tellraw @s {"text":"Time remaining: ","extra":[{"score":{"name":"@s","objective":"timer"}}]};
        timer<@s> = $timer<@s>$ - 1;
        exec game:wait_one_second;
    }
    
    tellraw @s {"text":"Time's up!"};
}
```

### Complex Game Logic
```mdl
pack "game" "Complex game example" 82;
namespace "game";

// Tag declarations
tag recipe "magic_wand" "recipes/magic_wand.json";
tag loot_table "magic_loot" "loot_tables/magic_loot.json";
tag advancement "magic_master" "advancements/magic_master.json";
tag predicate "has_mana" "predicates/has_mana.json";
tag structure "magic_tower" "structures/magic_tower.json";

var num player_level<@s> = 1;
var num player_exp<@s> = 0;
var num global_high_score<@a> = 0;
var num game_timer<@a> = 0;

function "gain_experience" {
    player_exp<@s> = $player_exp<@s>$ + 10;
    
    if $player_exp<@s>$ >= 100 {
        player_level<@s> = $player_level<@s>$ + 1;
        player_exp<@s> = 0;
        tellraw @s {"text":"Level up! New level: ","extra":[{"score":{"name":"@s","objective":"player_level"}}]};
        
        if $player_level<@s>$ > $global_high_score<@a>$ {
            global_high_score<@a> = $player_level<@s>$;
            tellraw @a {"text":"New high level achieved: ","extra":[{"score":{"name":"@s","objective":"global_high_score"}}]};
        }
    }
}

function "update_timer" {
    game_timer<@a> = $game_timer<@a>$ + 1;
    
    if $game_timer<@a>$ >= 1200 {
        game_timer<@a> = 0;
        tellraw @s {"text":"Time's up! Final level: ","extra":[{"score":{"name":"@s","objective":"player_level"}}]};
    }
}

on_tick "game:update_timer";
```

## Compilation Rules

### Variable Resolution
1. **Declaration**: Variables declare their storage scope when defined
2. **Reading**: `$variable<scope>$` gets converted to appropriate Minecraft scoreboard commands
3. **Writing**: `variable<scope>` specifies the target scope for assignments
4. **Access**: Variables can be accessed at any scope, regardless of where they were declared

### Function Compilation
1. **Exec Calls**: `exec function` becomes `execute as @s run function namespace:function`
2. **Exec Calls with Scope**: `exec function<@s>` becomes `execute as @s run function namespace:function`
3. **No Return Values**: Functions compile to a series of Minecraft commands

### Control Structure Compilation
1. **If Statements**: Generate `execute if score condition run function namespace:if_function` commands
2. **Else If Statements**: Handle nested if statements recursively, generating proper conditional chains
3. **Else Blocks**: Generate `execute unless score condition run function namespace:else_function` commands
4. **While Loops**: Generate recursive function calls that continue while the condition is true
5. **Nested Structures**: Automatically handle complex nested if/else and while loop combinations

### Say Command Compilation
1. **Simple Text**: `say "message"` becomes `tellraw @a {"text":"message"}`
2. **With Variables**: `say "Score: $score<@s>$"` becomes `tellraw @a {"text":"Score: ","extra":[{"score":{"name":"@s","objective":"score"}}]}`
3. **Multiple Variables**: Complex variable substitutions are automatically formatted into proper JSON structure
4. **Default Target**: All say commands target `@a` (all players) for maximum visibility

### Tag Compilation
1. **Recipe Tags**: `tag recipe "name" "path"` generates appropriate tag files
2. **Loot Table Tags**: `tag loot_table "name" "path"` generates loot table tag files
3. **Advancement Tags**: `tag advancement "name" "path"` generates advancement tag files
4. **Item Modifier Tags**: `tag item_modifier "name" "path"` generates item modifier tag files
5. **Predicate Tags**: `tag predicate "name" "path"` generates predicate tag files
6. **Structure Tags**: `tag structure "name" "path"` generates structure tag files

### Error Handling
- **Undefined Variables**: Compilation error if variable not declared
- **Invalid Scopes**: Compilation error if scope selector is malformed
- **Missing Semicolons**: Compilation error for incomplete statements
- **Unterminated Blocks**: Compilation error for missing braces
- **Invalid Tag Paths**: Compilation error if tag file path is malformed

## Best Practices

1. **Always specify scopes explicitly** - Makes code clear and prevents bugs
2. **Use consistent syntax** - `$variable<scope>$` for reading, `variable<scope>` for writing
3. **Use meaningful variable names** - `player_score<@s>` is clearer than `score<@s>`
4. **Group related variables** - Keep variables with similar purposes together
5. **Comment complex scopes** - Explain non-standard selectors
6. **Avoid reserved names** - Don't use `load`, `tick`, or other Minecraft keywords
7. **Use consistent naming** - Pick a convention and stick to it
8. **Test scope combinations** - Verify that your scope logic works as expected
9. **Organize tag declarations** - Group related tags together at the top of files
10. **Use descriptive tag names** - Make tag names clear and meaningful

## Tokenization Specification

This section defines exactly how MDL source code is broken down into tokens. This specification is critical for maintaining consistency between the lexer, parser, and compiler.

### Core Token Types

#### **Keywords** (Reserved Words)
```
pack, namespace, function, var, num, if, else, while, on_load, on_tick, exec, tag
```

#### **Tag Types** (Resource Categories)
```
recipe, loot_table, advancement, item_modifier, predicate, structure
```

#### **Identifiers**
```
[a-zA-Z_][a-zA-Z0-9_]*
```
Examples: `player_score`, `game`, `start_game`, `_internal_var`

#### **Numbers**
```
[0-9]+(\.[0-9]+)?
```
Examples: `0`, `42`, `3.14`, `1000`

#### **Operators**
```
// Arithmetic
+ (PLUS), - (MINUS), * (MULTIPLY), / (DIVIDE)

// Comparison
== (EQUAL), != (NOT_EQUAL), > (GREATER), < (LESS), >= (GREATER_EQUAL), <= (LESS_EQUAL)

// Assignment
= (ASSIGN)

// Execution
exec (EXEC)
```

#### **Delimiters**
```
; (SEMICOLON)     - Statement terminator
, (COMMA)         - Parameter separator
: (COLON)         - Namespace separator
```

#### **Brackets and Braces**
```
( (LPAREN), ) (RPAREN)     - Parentheses for expressions and function calls
{ (LBRACE), } (RBRACE)     - Braces for code blocks
[ (LBRACKET), ] (RBRACKET) - Brackets for selectors and arrays
< (LANGLE), > (RANGLE)     - Angle brackets for scope syntax
```

#### **Special Tokens**
```
$ (DOLLAR)        - Variable substitution delimiter
" (QUOTE)         - String literal delimiter
```

### Tag Declaration Tokenization

#### **Basic Tag Declaration**
```
tag recipe "RecipeName" "path/to/recipe.json";
```
Tokenized as:
1. `TAG` (`tag`)
2. `RECIPE` (`recipe`)
3. `QUOTE` (`"`)
4. `IDENTIFIER` (`RecipeName`)
5. `QUOTE` (`"`)
6. `QUOTE` (`"`)
7. `IDENTIFIER` (`path/to/recipe.json`)
8. `QUOTE` (`"`)
9. `SEMICOLON` (`;`)

#### **Tag Declaration with Complex Path**
```
tag loot_table "EpicLoot" "loot_tables/epic_loot.json";
```
Tokenized as:
1. `TAG` (`tag`)
2. `LOOT_TABLE` (`loot_table`)
3. `QUOTE` (`"`)
4. `IDENTIFIER` (`EpicLoot`)
5. `QUOTE` (`"`)
6. `QUOTE` (`"`)
7. `IDENTIFIER` (`loot_tables/epic_loot.json`)
8. `QUOTE` (`"`)
9. `SEMICOLON` (`;`)
```

### Scope Selector Tokenization

#### **Basic Selectors**
```
@s, @a, @p, @r
```
These are tokenized as single `IDENTIFIER` tokens.

#### **Complex Selectors**
```
@e[type=armor_stand,tag=mdl_server,limit=1]
```
This entire selector is tokenized as a single `IDENTIFIER` token.

#### **Scope Syntax**
```
<@s>, <@a[team=red]>, <global>
```
These are tokenized as:
1. `LANGLE` (`<`)
2. `IDENTIFIER` (the selector content)
3. `RANGLE` (`>`)

### Variable Substitution Tokenization

#### **Basic Substitution**
```
$player_score<@s>$
```
Tokenized as:
1. `DOLLAR` (`$`)
2. `IDENTIFIER` (`player_score`)
3. `LANGLE` (`<`)
4. `IDENTIFIER` (`@s`)
5. `RANGLE` (`>`)
6. `DOLLAR` (`$`)

#### **Complex Substitution**
```
$team_score<@a[team=red]>$
```
Tokenized as:
1. `DOLLAR` (`$`)
2. `IDENTIFIER` (`team_score`)
3. `LANGLE` (`<`)
4. `IDENTIFIER` (`@a[team=red]`)
5. `RANGLE` (`>`)
6. `DOLLAR` (`$`)

### Function Declaration Tokenization

#### **Basic Function**
```
function game:start_game {
```
Tokenized as:
1. `FUNCTION` (`function`)
2. `IDENTIFIER` (`game`)
3. `COLON` (`:`)
4. `IDENTIFIER` (`start_game`)
5. `LBRACE` (`{`)

#### **Function with Scope**
```
function game:reset_player {
```
Tokenized as:
1. `FUNCTION` (`function`)
2. `IDENTIFIER` (`game`)
3. `COLON` (`:`)
4. `IDENTIFIER` (`reset_player`)
5. `LANGLE` (`<`)
6. `IDENTIFIER` (`@s`)
7. `RANGLE` (`>`)
8. `LBRACE` (`{`)

### Function Call Tokenization

#### **Call with Scope**
```
exec game:reset_player<@s>;
```
Tokenized as:
1. `EXEC` (`exec`)
2. `IDENTIFIER` (`game`)
3. `COLON` (`:`)
4. `IDENTIFIER` (`reset_player`)
5. `LANGLE` (`<`)
6. `IDENTIFIER` (`@s`)
7. `RANGLE` (`>`)
8. `SEMICOLON` (`;`)

#### **Exec Call without Scope**
```
exec game:reset_player;
```
Tokenized as:
1. `EXEC` (`exec`)
2. `IDENTIFIER` (`game`)
3. `COLON` (`:`)
4. `IDENTIFIER` (`reset_player`)
5. `SEMICOLON` (`;`)
```

### Variable Declaration Tokenization

#### **Basic Declaration**
```
var num player_score<@s> = 0;
```
Tokenized as:
1. `VAR` (`var`)
2. `NUM` (`num`)
3. `IDENTIFIER` (`player_score`)
4. `LANGLE` (`<`)
5. `IDENTIFIER` (`@s`)
6. `RANGLE` (`>`)
7. `ASSIGN` (`=`)
8. `NUMBER` (`0`)
9. `SEMICOLON` (`;`)

### Variable Assignment Tokenization

#### **Simple Assignment**
```
player_score<@s> = 42;
```
Tokenized as:
1. `IDENTIFIER` (`player_score`)
2. `LANGLE` (`<`)
3. `IDENTIFIER` (`@s`)
4. `RANGLE` (`>`)
5. `ASSIGN` (`=`)
6. `NUMBER` (`42`)
7. `SEMICOLON` (`;`)

#### **Expression Assignment**
```
player_score<@s> = $player_score<@s>$ + 1;
```
Tokenized as:
1. `IDENTIFIER` (`player_score`)
2. `LANGLE` (`<`)
3. `IDENTIFIER` (`@s`)
4. `RANGLE` (`>`)
5. `ASSIGN` (`=`)
6. `DOLLAR` (`$`)
7. `IDENTIFIER` (`player_score`)
8. `LANGLE` (`<`)
9. `IDENTIFIER` (`@s`)
10. `RANGLE` (`>`)
11. `DOLLAR` (`$`)
12. `PLUS` (`+`)
13. `NUMBER` (`1`)
14. `SEMICOLON` (`;`)

### Control Structure Tokenization

#### **If Statement**
```
if $player_score<@s>$ > 10 {
```
Tokenized as:
1. `IF` (`if`)
2. `DOLLAR` (`$`)
3. `IDENTIFIER` (`player_score`)
4. `LANGLE` (`<`)
5. `IDENTIFIER` (`@s`)
6. `RANGLE` (`>`)
7. `DOLLAR` (`$`)
8. `GREATER` (`>`)
9. `NUMBER` (`10`)
10. `LBRACE` (`{`)

#### **While Loop**
```
while $counter<@s>$ > 0 {
```
Tokenized as:
1. `WHILE` (`while`)
2. `DOLLAR` (`$`)
3. `IDENTIFIER` (`counter`)
4. `LANGLE` (`<`)
5. `IDENTIFIER` (`@s`)
6. `RANGLE` (`>`)
7. `DOLLAR` (`$`)
8. `GREATER` (`>`)
9. `NUMBER` (`0`)
10. `LBRACE` (`{`)

### Raw Block Tokenization

#### **Raw Block Start**
```
$!raw
```
Tokenized as:
1. `DOLLAR` (`$`)
2. `EXCLAMATION` (`!`)
3. `IDENTIFIER` (`raw`)

#### **Raw Block End**
```
raw!$
```
Tokenized as:
1. `IDENTIFIER` (`raw`)
2. `EXCLAMATION` (`!`)
3. `DOLLAR` (`$`)

### Whitespace and Comments

#### **Whitespace**
- Spaces, tabs, and newlines are ignored during tokenization
- They serve only to separate tokens
- Multiple consecutive whitespace characters are treated as a single separator

#### **Comments**
```
// Single line comment
/* Multi-line comment */
```
Comments are completely ignored during tokenization and do not generate any tokens.

**Comment Rules:**
- Single-line comments start with `//` and continue to the end of the line
- Multi-line comments start with `/*` and end with `*/`
- Comments can appear anywhere in the code
- Comments are stripped out before processing - they don't affect the generated `.mcfunction` files

### Tokenization Rules

1. **Longest Match**: Always consume the longest possible token (e.g., `>=` not `>` then `=`)
2. **No Ambiguity**: Each character sequence maps to exactly one token type
3. **Scope Priority**: Scope selectors are always tokenized as complete `IDENTIFIER` tokens
4. **No Context**: Tokenization is context-free - the same character sequence always produces the same tokens
5. **Error Handling**: Invalid characters or unterminated sequences generate appropriate error tokens
6. **String Handling**: Quoted strings are tokenized as complete units with their delimiters

### Example Complete Tokenization

```mdl
tag recipe "diamond_sword" "recipes/diamond_sword.json";
var num player_score<@s> = 0;
```

**Tokens Generated:**
1. `TAG` (`tag`)
2. `RECIPE` (`recipe`)
3. `QUOTE` (`"`)
4. `IDENTIFIER` (`diamond_sword`)
5. `QUOTE` (`"`)
6. `QUOTE` (`"`)
7. `IDENTIFIER` (`recipes/diamond_sword.json`)
8. `QUOTE` (`"`)
9. `SEMICOLON` (`;`)
10. `VAR` (`var`)
11. `NUM` (`num`)
12. `IDENTIFIER` (`player_score`)
13. `LANGLE` (`<`)
14. `IDENTIFIER` (`@s`)
15. `RANGLE` (`>`)
16. `ASSIGN` (`=`)
17. `NUMBER` (`0`)
18. `SEMICOLON` (`;`)
19. `EOF`

This tokenization specification ensures that the lexer, parser, and compiler all work with the same understanding of how MDL source code is structured.

## Edge Cases and Error Handling

### Common Error Scenarios

#### **Unterminated Scope Selectors**
```mdl
// ❌ Error: Missing closing >
var num score<@s = 0;

// ✅ Correct
var num score<@s> = 0;
```

#### **Invalid Scope Selectors**
```mdl
// ❌ Error: Invalid selector syntax
var num score<@invalid[type=armor_stand]> = 0;

// ✅ Correct
var num score<@e[type=armor_stand,tag=mdl_server,limit=1]> = 0;
```

#### **Missing Semicolons**
```mdl
// ❌ Error: Missing semicolon
var num score<@s> = 0
player_score<@s> = 5

// ✅ Correct
var num score<@s> = 0;
player_score<@s> = 5;
```

#### **Unterminated Blocks**
```mdl
// ❌ Error: Missing closing brace
function game:test {
    player_score<@s> = 0;
    // Missing }

// ✅ Correct
function game:test {
    player_score<@s> = 0;
}
```

#### **Invalid Variable References**
```mdl
// ❌ Error: Variable not declared
player_score<@s> = 0;
score<@s> = 5;  // 'score' was never declared

// ✅ Correct
var num score<@s> = 0;
player_score<@s> = 0;
score<@s> = 5;
```

#### **Invalid Tag Declarations**
```mdl
// ❌ Error: Missing quotes
tag recipe RecipeName "path/to/recipe.json";

// ❌ Error: Missing semicolon
tag recipe "RecipeName" "path/to/recipe.json"

// ✅ Correct
tag recipe "RecipeName" "path/to/recipe.json";
```

### Complex Edge Cases

#### **Nested Scope Selectors in Raw Blocks**
```mdl
// This is valid - raw blocks pass through unchanged
$!raw
execute if score @s player_score<@s> matches 10.. run function game:celebrate
raw!$
```

#### **Scope Selectors with Special Characters**
```mdl
// Valid - selector with complex parameters
var num data<@e[type=armor_stand,tag=mdl_server,limit=1,nbt={CustomName:'{"text":"Server"}'}]> = 0;
```

#### **Variable Names with Underscores**
```mdl
// Valid - underscores are allowed in variable names
var num player_score_red_team<@a[team=red]> = 0;
var num _internal_counter<@s> = 0;
```

#### **Function Names with Numbers**
```mdl
// Valid - numbers are allowed in function names
function game:level_1_complete {
    player_score<@s> = player_score<@s> + 100;
}
```

#### **Tag Paths with Special Characters**
```mdl
// Valid - paths can contain various characters
tag recipe "complex_recipe" "recipes/complex/recipe_v1.2.json";
tag loot_table "special_loot" "loot_tables/special/loot_#1.json";
```

### Error Recovery

The MDL compiler attempts to provide helpful error messages:

1. **Line and Column Information** - Shows exactly where the error occurred
2. **Context** - Displays the problematic line with surrounding context
3. **Suggestions** - Provides specific guidance on how to fix the error
4. **Error Categories** - Groups errors by type (syntax, scope, undefined variables, invalid tags, etc.)

### Performance Considerations

- **Large Selectors**: Very long scope selectors may impact compilation time
- **Deep Nesting**: Excessive nesting of control structures may affect parsing performance
- **Raw Block Size**: Large raw blocks are processed efficiently as they're copied without parsing
- **Tag Processing**: Tag declarations are processed efficiently as they're simple string operations

## Abstract Syntax Tree (AST) Implementation

The MDL language is implemented using a comprehensive Abstract Syntax Tree (AST) system that represents the parsed code structure. This section explains how the AST works and how it represents all language constructs.

### AST Node Hierarchy

The AST is built using a hierarchy of node classes, each representing a specific language construct:

#### **Root Node: Program**
```python
class Program:
    pack: Optional[PackDeclaration]           # Pack metadata
    namespace: Optional[NamespaceDeclaration] # Default namespace
    tags: List[TagDeclaration]               # Resource tag declarations
    variables: List[VariableDeclaration]     # Variable declarations
    functions: List[FunctionDeclaration]     # Function definitions
    hooks: List[HookDeclaration]            # Event hooks (on_load, on_tick)
    statements: List[ASTNode]               # Top-level statements
```

The `Program` node serves as the root of the AST, containing all top-level declarations and statements. This structure allows the compiler to:
- Generate the `pack.mcmeta` file from pack declarations
- Create the proper directory structure based on namespace
- Process all tag references for resource generation
- Manage variable scoping across the entire program
- Generate function files with proper namespacing
- Set up event hooks for automatic execution

#### **Declaration Nodes**

**PackDeclaration**
```python
class PackDeclaration:
    name: str           # Pack name (e.g., "MyGame")
    description: str    # Pack description
    pack_format: int    # Minecraft pack format version
```

**NamespaceDeclaration**
```python
class NamespaceDeclaration:
    name: str           # Namespace name (e.g., "game")
```

**TagDeclaration**
```python
class TagDeclaration:
    tag_type: str       # Resource type (recipe, loot_table, etc.)
    name: str           # Tag name
    file_path: str      # Path to the JSON file
```

**VariableDeclaration**
```python
class VariableDeclaration:
    var_type: str       # Variable type (currently only "num")
    name: str           # Variable name
    scope: str          # Scope selector (e.g., "<@s>", "<@a[team=red]>")
    initial_value: Any  # Initial value expression
```

**FunctionDeclaration**
```python
class FunctionDeclaration:
    namespace: str      # Function namespace
    name: str           # Function name
    scope: Optional[str] # Optional scope for function execution
    body: List[ASTNode] # Function body statements
```

**HookDeclaration**
```python
class HookDeclaration:
    hook_type: str      # Hook type ("on_load" or "on_tick")
    namespace: str      # Function namespace to call
    name: str           # Function name to call
    scope: Optional[str] # Optional scope for hook execution
```

#### **Statement Nodes**

**VariableAssignment**
```python
class VariableAssignment:
    name: str           # Variable name
    scope: str          # Scope selector
    value: Any          # Value expression
```

**VariableSubstitution**
```python
class VariableSubstitution:
    name: str           # Variable name
    scope: str          # Scope selector
```

**FunctionCall**
```python
class FunctionCall:
    namespace: str      # Function namespace
    name: str           # Function name
    scope: Optional[str] # Optional scope
```

**Control Structures**
```python
class IfStatement:
    condition: Any      # Condition expression
    then_body: List[ASTNode]  # Then block statements
    else_body: Optional[List[ASTNode]]  # Optional else block

class WhileLoop:
    condition: Any      # Loop condition
    body: List[ASTNode] # Loop body statements
```

**Commands**
```python
class SayCommand:
    message: str        # Message text with variable placeholders
    variables: List[VariableSubstitution]  # Extracted variables

class RawBlock:
    content: str        # Raw content (passed through unchanged)
```

#### **Expression Nodes**

**BinaryExpression**
```python
class BinaryExpression:
    left: Any           # Left operand
    operator: str       # Operator (+, -, *, /, >, <, >=, <=, ==, !=)
    right: Any          # Right operand
```

**LiteralExpression**
```python
class LiteralExpression:
    value: Any          # Literal value
    type: str           # Value type ("number", "string", "identifier")
```

**ParenthesizedExpression**
```python
class ParenthesizedExpression:
    expression: Any     # Expression inside parentheses
```

### AST Construction Process

The AST is constructed through a multi-stage process:

1. **Lexical Analysis**: Source code is converted to tokens
2. **Parsing**: Tokens are parsed into AST nodes
3. **Validation**: AST structure is validated for correctness
4. **Compilation**: AST is traversed to generate output

#### **Lexical Analysis (Tokenization)**

The lexer converts source code into a stream of tokens:

```python
# Source: var num score<@s> = 0;
# Tokens: [VAR, NUM, IDENTIFIER('score'), LESS, IDENTIFIER('@s'), 
#          GREATER, ASSIGN, NUMBER('0'), SEMICOLON]
```

**Token Types**
- **Keywords**: `PACK`, `NAMESPACE`, `FUNCTION`, `VAR`, `IF`, `WHILE`, etc.
- **Operators**: `PLUS`, `MINUS`, `MULTIPLY`, `DIVIDE`, `ASSIGN`, `GREATER`, `LESS`, etc.
- **Delimiters**: `SEMICOLON`, `COMMA`, `COLON`, `LPAREN`, `RPAREN`, etc.
- **Literals**: `IDENTIFIER`, `NUMBER`, `QUOTE`
- **Special**: `DOLLAR`, `EXCLAMATION`, `RAW_CONTENT`

#### **Parsing Strategy**

The parser uses a recursive descent approach with operator precedence:

```python
def _parse_expression(self) -> Any:
    """Parse expressions with proper operator precedence."""
    return self._parse_comparison()

def _parse_comparison(self) -> Any:
    """Parse comparison expressions (>, <, >=, <=, ==, !=)."""
    expr = self._parse_term()
    while self._peek().type in [GREATER, LESS, GREATER_EQUAL, LESS_EQUAL, EQUAL, NOT_EQUAL]:
        operator = self._advance().type
        right = self._parse_term()
        expr = BinaryExpression(left=expr, operator=operator, right=right)
    return expr
```

**Operator Precedence** (highest to lowest):
1. **Primary**: Variables, literals, parenthesized expressions
2. **Factors**: Multiplication, division
3. **Terms**: Addition, subtraction
4. **Comparisons**: Greater, less, equal, not equal

### AST Traversal and Code Generation

The AST is designed to support efficient code generation:

#### **Visitor Pattern Support**
```python
class ASTVisitor:
    def visit_program(self, node: Program): pass
    def visit_variable_declaration(self, node: VariableDeclaration): pass
    def visit_function_declaration(self, node: FunctionDeclaration): pass
    # ... other visit methods
```

#### **Code Generation Strategy**
1. **Pack Generation**: Create `pack.mcmeta` from pack declarations
2. **Namespace Setup**: Establish directory structure
3. **Tag Processing**: Generate resource references
4. **Variable Management**: Set up scoreboard objectives
5. **Function Generation**: Create `.mcfunction` files
6. **Hook Integration**: Set up automatic execution

### Error Handling and Recovery

The AST system provides comprehensive error handling:

#### **Parser Error Context**
```python
class MDLParserError:
    message: str        # Error description
    file_path: str      # Source file path
    line: int           # Error line number
    column: int         # Error column number
    line_content: str   # Problematic line content
    suggestion: str     # How to fix the error
```

#### **Error Recovery Strategies**
1. **Graceful Degradation**: Continue parsing when possible
2. **Context Preservation**: Maintain line/column information
3. **Helpful Messages**: Provide specific fix suggestions
4. **Error Aggregation**: Collect multiple errors when possible

### Extensibility Features

The AST system is designed for easy extension:

#### **Adding New Node Types**
```python
class NewNode(ASTNode):
    def __init__(self, new_field: str):
        self.new_field = new_field
```

#### **Adding New Parsers**
```python
def _parse_new_construct(self) -> NewNode:
    # Parse new language construct
    pass
```

#### **Adding New Token Types**
```python
class TokenType:
    # ... existing types ...
    NEW_TYPE = "NEW_TYPE"
```

## Parsing System Implementation

The MDL parser implements a robust, extensible parsing system that handles all language constructs defined in the specification. This section explains how the parsing works and how it processes the language.

### Parser Architecture

The parser uses a **recursive descent** approach with **lookahead** capabilities:

```python
class MDLParser:
    def __init__(self, source_file: str = None):
        self.source_file = source_file
        self.tokens: List[Token] = []
        self.current = 0
        self.current_namespace = "mdl"
```

#### **Core Parsing Methods**

**Program Parsing**
```python
def _parse_program(self) -> Program:
    """Parse the complete program structure."""
    pack = None
    namespace = None
    tags = []
    variables = []
    functions = []
    hooks = []
    statements = []
    
    while not self._is_at_end():
        # Parse top-level constructs based on token type
        if self._peek().type == TokenType.PACK:
            pack = self._parse_pack_declaration()
        elif self._peek().type == TokenType.NAMESPACE:
            namespace = self._parse_namespace_declaration()
        # ... continue with other constructs
```

**Declaration Parsing**
```python
def _parse_pack_declaration(self) -> PackDeclaration:
    """Parse: pack "name" "description" format;"""
    self._expect(TokenType.PACK, "Expected 'pack' keyword")
    self._expect(TokenType.QUOTE, "Expected opening quote for pack name")
    name = self._expect_identifier("Expected pack name")
    # ... continue parsing
```

**Statement Parsing**
```python
def _parse_if_statement(self) -> IfStatement:
    """Parse: if condition { then_body } else { else_body }"""
    self._expect(TokenType.IF, "Expected 'if' keyword")
    condition = self._parse_expression()
    self._expect(TokenType.LBRACE, "Expected '{' to start if body")
    then_body = self._parse_block()
    # ... handle optional else clause
```

### Expression Parsing with Operator Precedence

The parser implements a **Pratt parser** approach for expressions:

```python
def _parse_expression(self) -> Any:
    """Entry point for expression parsing."""
    return self._parse_comparison()

def _parse_comparison(self) -> Any:
    """Parse comparison expressions with left associativity."""
    expr = self._parse_term()
    
    while not self._is_at_end() and self._peek().type in [
        TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, 
        TokenType.LESS_EQUAL, TokenType.EQUAL, TokenType.NOT_EQUAL
    ]:
        operator = self._peek().type
        self._advance()
        right = self._parse_term()
        expr = BinaryExpression(left=expr, operator=operator, right=right)
    
    return expr
```

**Precedence Levels**:
1. **Primary**: Variables, literals, parentheses
2. **Factors**: `*`, `/`
3. **Terms**: `+`, `-`
4. **Comparisons**: `>`, `<`, `>=`, `<=`, `==`, `!=`

### Scope Selector Parsing

Scope selectors are parsed differently based on context:

```python
def _parse_scope_selector(self) -> str:
    """Parse scope selector: <@s>, <@a[team=red]>, etc."""
    self._expect(TokenType.LESS, "Expected '<' for scope selector")
    
    selector_content = ""
    while not self._is_at_end() and self._peek().type != TokenType.GREATER:
        selector_content += self._peek().value
        self._advance()
    
    self._expect(TokenType.GREATER, "Expected '>' to close scope selector")
    return f"<{selector_content}>"
```

**Context-Sensitive Parsing**:
- **Variable Declarations**: Use `LESS`/`GREATER` tokens
- **Variable Substitutions**: Use `LANGLE`/`RANGLE` tokens
- **Function Parameters**: Use `LESS`/`GREATER` tokens

### Raw Block Processing

Raw blocks are handled specially to preserve exact content:

```python
def _parse_raw_block(self) -> RawBlock:
    """Parse: $!raw ... raw!$"""
    # Consume $!raw
    self._expect(TokenType.DOLLAR, "Expected '$' to start raw block")
    self._expect(TokenType.EXCLAMATION, "Expected '!' after '$' in raw block")
    self._expect(TokenType.IDENTIFIER, "Expected 'raw' keyword")
    
    # Look for RAW_CONTENT token (generated by lexer)
    if self._peek().type == TokenType.RAW_CONTENT:
        content = self._peek().value
        self._advance()
    else:
        content = ""
    
    # Consume raw!$ end marker
    self._expect(TokenType.IDENTIFIER, "Expected 'raw' to end raw block")
    self._expect(TokenType.EXCLAMATION, "Expected '!' to end raw block")
    self._expect(TokenType.DOLLAR, "Expected '$' to end raw block")
    
    return RawBlock(content=content)
```

### Variable Substitution in Strings

Variable substitutions within strings are handled through regex extraction:

```python
def _parse_say_command(self) -> SayCommand:
    """Parse: say "message with $variable<scope>$";"""
    self._expect(TokenType.IDENTIFIER, "Expected 'say' keyword")
    self._expect(TokenType.QUOTE, "Expected opening quote for say message")
    
    # Get string content (includes variable substitutions)
    if self._peek().type == TokenType.IDENTIFIER:
        message = self._peek().value
        self._advance()
    else:
        message = ""
    
    # Extract variables using regex pattern
    variables = []
    import re
    var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*<[^>]+>)\$'
    matches = re.findall(var_pattern, message)
    
    for match in matches:
        if '<' in match and '>' in match:
            name = match[:match.index('<')]
            scope = match[match.index('<'):match.index('>')+1]
            variables.append(VariableSubstitution(name=name, scope=scope))
    
    return SayCommand(message=message, variables=variables)
```

### Error Recovery and Context

The parser provides detailed error information:

```python
def _error(self, message: str, suggestion: str):
    """Raise a parser error with full context."""
    if self._is_at_end():
        line = 1
        column = 1
        line_content = "end of file"
    else:
        token = self._peek()
        line = token.line
        column = token.column
        line_content = token.value
    
    raise MDLParserError(
        message=message,
        file_path=self.source_file,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion
    )
```

### Parser Extensibility

The parser is designed for easy extension:

#### **Adding New Constructs**
```python
def _parse_new_construct(self) -> NewNode:
    """Parse new language construct."""
    # Implementation here
    pass

# Add to _parse_program method:
elif self._peek().type == TokenType.NEW_KEYWORD:
    statements.append(self._parse_new_construct())
```

#### **Adding New Expression Types**
```python
def _parse_primary(self) -> Any:
    """Parse primary expressions."""
    if self._peek().type == TokenType.NEW_TYPE:
        return self._parse_new_expression()
    # ... existing cases
```

### Performance Optimizations

The parser includes several performance optimizations:

1. **Token Lookahead**: Efficient `_peek()` method for lookahead
2. **Early Exit**: Quick checks for common token types
3. **Memory Efficiency**: Minimal object creation during parsing
4. **Error Recovery**: Fast error detection and reporting

### Integration with Lexer

The parser works seamlessly with the lexer:

```python
def parse(self, source: str) -> Program:
    """Parse MDL source code into an AST."""
    # Lex the source into tokens
    lexer = MDLLexer(self.source_file)
    self.tokens = lexer.lex(source)
    self.current = 0
    
    # Parse the program
    return self._parse_program()
```

This architecture ensures that:
- **Lexical errors** are caught early with detailed context
- **Parsing errors** provide helpful recovery suggestions
- **AST construction** is robust and handles edge cases
- **Error reporting** is consistent across the entire pipeline

The parsing system provides a solid foundation for the MDL compiler, ensuring that all language constructs are properly understood and can be translated into Minecraft datapack commands.
