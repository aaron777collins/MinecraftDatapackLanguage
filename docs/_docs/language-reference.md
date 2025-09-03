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
- **Default scope**: When no scope is specified, always use `@s` (current player)
- **No return values**: All functions are void - they execute commands and modify state
- **No quotes needed**: Use `$variable<scope>$` syntax directly instead of string literals
- **Scope execution**: Use `exec` keyword to execute functions with specific scopes

## Basic Syntax

### Pack Declaration
```mdl
pack "pack_name" "description" pack_format;
```

### Namespace Declaration
```mdl
namespace "namespace_name";
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
tellraw @s You have $player_score<@s>$ points;
execute if score @s player_score matches 10.. run game:celebrate;

// In conditions
if $player_score<@s>$ > 10 {
    player_score<@s> = 0;
}
```

### Functions

#### Function Declaration
```mdl
// Basic function
function game:start_game {
    player_score<@s> = 0;
    player_health<@s> = 20;
}

// Function declaration (no scope parameters)
function game:reset_player {
    player_score<@s> = 0;
    player_health<@s> = 20;
}
```

#### Function Calls
```mdl
// Call function (runs at current scope)
game:start_game;

// Execute function with specific scope using 'exec' keyword
exec game:reset_player<@s>;                      // Execute as @s
exec game:reset_player<@a>;                      // Execute as @a
exec game:reset_player<@e[type=armor_stand,tag=mdl_server,limit=1]>; // Execute as specific entity
```

### Control Structures

#### If Statements
```mdl
if $player_score<@s>$ > 10 {
    exec game:celebrate<@s>;
    player_score<@s> = 0;
}

if $player_health<@s>$ < 5 {
    exec game:heal<@s>;
} else {
    exec game:check_health<@s>;
}
```

#### While Loops
```mdl
while $counter<@s>$ > 0 {
    counter<@s> = $counter<@s>$ - 1;
    exec game:countdown<@s>;
}
```

### Hooks
```mdl
on_load "game:start_game";                      // Runs when datapack loads
on_tick "game:update_timer";                     // Runs every tick
```

**Note:** Hooks use quoted strings for function references, unlike regular function calls. This is because hooks are processed at datapack load time, not during execution.

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
3. **Function Execution Scope**: Use `exec` keyword to execute functions with specific scopes
4. **No Inheritance**: Functions do not inherit scope from their caller
5. **Default Scope**: When no scope specified, always use `@s` (current player)
6. **No Memory**: The system does not remember a variable's declared scope for subsequent operations

### Scope Usage Examples

```mdl
// VARIABLES: Clear distinction between reading and writing
var num score<@a> = 0;                    // Declare with scope
score<@s> = 5;                            // Write with scope
if $score<@a>$ > 10 { ... }               // Read with scope

// FUNCTIONS: Use exec keyword for scope execution
game:start;                               // Execute at current scope (@s)
exec game:start<@a>;                      // Execute as @a
exec game:reset<@e[type=armor_stand]>;   // Execute as specific entity
```

### Scope Examples

```mdl
// Declare variable with global scope
var num global_counter<@a> = 0;

// Later operations - each specifies its own scope
global_counter<@s> = 5;                         // Set current player's counter to 5
global_counter<@a> = $global_counter<@a>$ + 1;  // Increment global counter
global_counter = 10;                            // Same as global_counter<@s> = 10 (defaults to @s)

// Function calls with different scopes
exec game:increment<@s>;                        // Run increment function as @s
exec game:increment<@a>;                        // Run increment function as @a
game:increment;                                 // Same as game:increment<@s> (defaults to @s)
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
% (modulo)

// Comparison
== (equal)
!= (not equal)
> (greater than)
< (less than)
>= (greater than or equal)
<= (less than or equal)

// Logical
&& (and)
|| (or)
! (not)
```

### Expression Examples
```mdl
// Complex expressions with different scopes
player_score<@s> = $x<@a>$ + $y<@p>$ * $z<@r>$;

// Parentheses for precedence
player_score<@s> = ($x<@s>$ + $y<@s>$) * 2;

// Logical expressions
if $score<@s>$ > 10 && $health<@s>$ > 0 {
    exec game:reward<@s>;
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

### Basic Counter
```mdl
pack "counter" "Counter example" 82;
namespace "counter";

var num global_counter<@a> = 0;
var num player_counter<@s> = 0;

function "increment" {
    global_counter<@a> = $global_counter<@a>$ + 1;
    player_counter<@s> = $player_counter<@s>$ + 1;
    
    tellraw @s Global: $global_counter<@a>$, Player: $player_counter<@s>$;
}

function "reset_player" {
    player_counter<@s> = 0;
    tellraw @s Counter reset!;
}

on_load "counter:increment";
```

### Team Game
```mdl
pack "teamgame" "Team game example" 82;
namespace "teamgame";

var num red_score<@a[team=red]> = 0;
var num blue_score<@a[team=blue]> = 0;
var num player_score<@s> = 0;

function "award_points" {
    player_score<@s> = $player_score<@s>$ + 10;
    
    if $player<@s> has team red {
        red_score<@a[team=red]> = $red_score<@a[team=red]>$ + 5;
        tellraw @s Red team score: $red_score<@a[team=red]>$;
    } else if $player<@s> has team blue {
        blue_score<@a[team=blue]> = $blue_score<@a[team=blue]>$ + 5;
        tellraw @s Blue team score: $blue_score<@a[team=blue]>$;
    }
    
    tellraw @s Your score: $player_score<@s>$;
}

function "show_leaderboard" {
    tellraw @s === LEADERBOARD ===;
    tellraw @s Red Team: $red_score<@a[team=red]>$;
    tellraw @s Blue Team: $blue_score<@a[team=blue]>$;
    tellraw @s Your Score: $player_score<@s>$;
}
```

### Complex Game Logic
```mdl
pack "game" "Complex game example" 82;
namespace "game";

var num player_level<@s> = 1;
var num player_exp<@s> = 0;
var num global_high_score<@a> = 0;
var num game_timer<@a> = 0;

function "gain_experience" {
    player_exp<@s> = $player_exp<@s>$ + 10;
    
    if $player_exp<@s>$ >= 100 {
        player_level<@s> = $player_level<@s>$ + 1;
        player_exp<@s> = 0;
        tellraw @s Level up! New level: $player_level<@s>$;
        
        if $player_level<@s>$ > $global_high_score<@a>$ {
            global_high_score<@a> = $player_level<@s>$;
            tellraw @a New high level achieved: $global_high_score<@a>$;
        }
    }
}

function "update_timer" {
    game_timer<@a> = $game_timer<@a>$ + 1;
    
    if $game_timer<@a>$ >= 1200 {
        game_timer<@a> = 0;
        tellraw @s Time's up! Final level: $player_level<@s>$;
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
1. **Scope Execution**: `exec function<@s>` becomes `execute as @s run function namespace:function`
2. **Default Scope**: `function` becomes `execute as @s run function namespace:function`
3. **No Return Values**: Functions compile to a series of Minecraft commands

### Error Handling
- **Undefined Variables**: Compilation error if variable not declared
- **Invalid Scopes**: Compilation error if scope selector is malformed
- **Missing Semicolons**: Compilation error for incomplete statements
- **Unterminated Blocks**: Compilation error for missing braces

## Best Practices

1. **Always specify scopes explicitly** - Makes code clear and prevents bugs
2. **Use consistent syntax** - `$variable<scope>$` for reading, `variable<scope>` for writing
3. **Use meaningful variable names** - `player_score<@s>` is clearer than `score<@s>`
4. **Group related variables** - Keep variables with similar purposes together
5. **Comment complex scopes** - Explain non-standard selectors
6. **Avoid reserved names** - Don't use `load`, `tick`, or other Minecraft keywords
7. **Use consistent naming** - Pick a convention and stick to it
8. **Test scope combinations** - Verify that your scope logic works as expected

## Tokenization Specification

This section defines exactly how MDL source code is broken down into tokens. This specification is critical for maintaining consistency between the lexer, parser, and compiler.

### Core Token Types

#### **Keywords** (Reserved Words)
```
pack, namespace, function, var, num, if, else, while, on_load, on_tick, exec
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
+ (PLUS), - (MINUS), * (MULTIPLY), / (DIVIDE), % (MODULO)

// Comparison
== (EQUAL), != (NOT_EQUAL), > (GREATER), < (LESS), >= (GREATER_EQUAL), <= (LESS_EQUAL)

// Logical
&& (AND), || (OR), ! (NOT)

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
function game:reset_player<@s> {
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

#### **Basic Call**
```
game:start_game;
```
Tokenized as:
1. `IDENTIFIER` (`game`)
2. `COLON` (`:`)
3. `IDENTIFIER` (`start_game`)
4. `SEMICOLON` (`;`)

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

### Example Complete Tokenization

```mdl
var num player_score<@s> = 0;
```

**Tokens Generated:**
1. `VAR` (`var`)
2. `NUM` (`num`)
3. `IDENTIFIER` (`player_score`)
4. `LANGLE` (`<`)
5. `IDENTIFIER` (`@s`)
6. `RANGLE` (`>`)
7. `ASSIGN` (`=`)
8. `NUMBER` (`0`)
9. `SEMICOLON` (`;`)
10. `EOF`

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
function game:level_1_complete<@s> {
    player_score<@s> = player_score<@s> + 100;
}
```

### Error Recovery

The MDL compiler attempts to provide helpful error messages:

1. **Line and Column Information** - Shows exactly where the error occurred
2. **Context** - Displays the problematic line with surrounding context
3. **Suggestions** - Provides specific guidance on how to fix the error
4. **Error Categories** - Groups errors by type (syntax, scope, undefined variables, etc.)

### Performance Considerations

- **Large Selectors**: Very long scope selectors may impact compilation time
- **Deep Nesting**: Excessive nesting of control structures may affect parsing performance
- **Raw Block Size**: Large raw blocks are processed efficiently as they're copied without parsing
