# MDL (Minecraft Datapack Language) - Simplified Specification

## Overview
MDL is a **SIMPLE** language that compiles to Minecraft datapack `.mcfunction` files. This specification focuses on **CONTROL STRUCTURES** and **SIMPLE VARIABLES** - the core problems that need solving.

## Language Syntax Reference

### 1. Pack and Namespace Declarations
```mdl
pack "pack_name" description "description" pack_format 82;
namespace "namespace_name";
```

### 2. Variable Declarations and Assignments
```mdl
// Only number variables stored in scoreboard
var num counter = 0;
var num health = 20;
var num level = 1;

// Assignment
counter = 42;
health = health - 5;
```

### 3. Variable Substitution
```mdl
// Use $variable$ syntax to read from scoreboard
say "Health: $health$";
if "$health$ < 10" {
    say "Low health!";
}

// Variable substitution in conditions
if "$counter$ > 5" {
    say "Counter is high!";
}

// Note: Functions called via tags (on_tick, on_load) use @a selector
// Functions called directly by players use @s selector
```

### 4. Function Declarations
```mdl
function "main" {
    say "Hello from main function";
    tellraw @a {"text":"Welcome!","color":"green"};
}

function "helper" {
    var num result = 0;
    result = 5 + 3;
    say "Result: $result$";
}
```

### 5. Control Flow Statements
```mdl
// If statements
if "$counter$ > 5" {
    say "Counter is high!";
}

// If-else statements
if "$health$ < 10" {
    say "Health is low!";
} else {
    say "Health is okay";
}

// While loops with method selection
while "$counter$ < 10" {
    counter = $counter$ + 1;
    say "Counter: $counter$";
}

// While loops with explicit method
while "$counter$ < 1000" method="recursion" {
    counter = $counter$ + 1;
    say "Recursion loop: $counter$";
}

// While loops with schedule method (better for long loops)
while "$counter$ < 10000" method="schedule" {
    counter = $counter$ + 1;
    say "Schedule loop: $counter$";
}
```

### 6. Function Calls
```mdl
function "namespace:function_name";
function "helper";
function "utils:calculator";
```

### 7. Built-in Commands
```mdl
say "Hello World";
tellraw @s {"text":"Colored message","color":"green"};
```

### 8. Hooks
```mdl
on_load "namespace:init";
on_tick "namespace:main";
```

### 9. Tags
```mdl
// Function tags
tag function minecraft:load {
    add "namespace:init";
}

tag function minecraft:tick {
    add "namespace:main";
    add "namespace:update";
}
```

## Lexer Specification

### Token Types
The lexer recognizes the following token types:

```python
class TokenType(Enum):
    # Keywords
    PACK = "PACK"
    NAMESPACE = "NAMESPACE"
    FUNCTION = "FUNCTION"
    ON_TICK = "ON_TICK"
    ON_LOAD = "ON_LOAD"
    TAG = "TAG"
    ADD = "ADD"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    VAR = "VAR"
    NUM = "NUM"
    
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUALS = "LESS_EQUALS"
    GREATER_EQUALS = "GREATER_EQUALS"
    
    # Punctuation
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COLON = "COLON"
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
```

### Lexer Rules
1. **Keywords**: Recognized before identifiers (e.g., `function`, `if`, `while`)
2. **Variable Substitution**: `$variable_name$` is tokenized as a special pattern
3. **Strings**: Support both single and double quotes
4. **Numbers**: Support integers and decimals
5. **Identifiers**: Start with letter/underscore, contain alphanumeric/underscore
6. **Whitespace**: Newlines are preserved, other whitespace is ignored

## Parser Specification

### AST Node Types
```python
# Core Nodes
@dataclass
class PackDeclaration:
    name: str
    description: str
    pack_format: int

@dataclass
class NamespaceDeclaration:
    name: str

@dataclass
class FunctionDeclaration:
    name: str
    body: List[Statement]

@dataclass
class VariableDeclaration:
    var_type: str  # "var"
    data_type: str  # "num"
    name: str
    value: Optional[Expression]

@dataclass
class AssignmentStatement:
    name: str
    value: Expression

@dataclass
class IfStatement:
    condition: str  # Minecraft selector condition
    then_body: List[Statement]
    else_body: Optional[List[Statement]]

@dataclass
class WhileStatement:
    condition: str  # Minecraft selector condition
    body: List[Statement]

@dataclass
class ForLoop:
    variable: str
    selector: str  # Minecraft selector
    body: List[Statement]

@dataclass
class FunctionCall:
    name: str

@dataclass
class CommandStatement:
    command: str
    args: List[str]

# Expression Nodes
@dataclass
class LiteralExpression:
    value: Union[int, float, str]

@dataclass
class VariableExpression:
    name: str

@dataclass
class BinaryExpression:
    left: Expression
    operator: str
    right: Expression
```

### Parser Rules
1. **Top-level**: Pack, namespace, function declarations, hooks, tags
2. **Statements**: Variable declarations, assignments, control flow, function calls
3. **Expressions**: Literals, variables, binary operations
4. **Precedence**: Follows standard arithmetic precedence
5. **Associativity**: Left-to-right for most operators

## Compiler Specification

### Minecraft Command Generation

#### Variable Storage
- **All variables**: Stored in scoreboard objectives
  ```mcfunction
  scoreboard players set @s counter 42
  scoreboard players set @s health 20
  ```

#### Variable Substitution
- **Pattern**: `$variable_name$` → `score @s variable_name`
- **In strings**: `"Health: $health$"` → `[{"text":"Health: "},{"score":{"name":"@s","objective":"health"}}]`
- **In conditions**: `"$health$ < 10"` → `"score @s health matches ..9"`

#### Control Flow Translation
- **If Statements**: Use `execute if` commands
  ```mcfunction
  execute if score @s condition matches 1.. run function namespace:then_function
  execute unless score @s condition matches 1.. run function namespace:else_function
  ```
- **While Loops**: Use `execute while` commands
  ```mcfunction
  execute while score @s condition matches 1.. run function namespace:loop_body
  ```
- **For Loops**: Use `execute as` commands
  ```mcfunction
  execute as @e[type=player] run function namespace:loop_body
  ```

#### Expression Translation
- **Arithmetic**: Use `execute store result` commands
  ```mcfunction
  execute store result score @s result run data get storage mdl:variables a
  execute store result score @s temp run data get storage mdl:variables b
  scoreboard players operation @s result += @s temp
  ```

### Output Structure
```
datapack/
├── pack.mcmeta
└── data/
    ├── namespace/
    │   ├── functions/
    │   │   ├── main.mcfunction
    │   │   └── helper.mcfunction
    │   └── tags/
    │       └── functions/
    │           ├── load.json
    │           └── tick.json
    └── mdl/
        └── functions/
            └── garbage_collect.mcfunction
```

### Registry JSON Files

- Declarations like `recipe "name" "relative/path.json";` reference external JSON files.
- In multi-file projects, the JSON path is resolved relative to the MDL file containing the declaration, not the first file.
- Missing or invalid JSON produces a warning and compilation continues with an empty object for that registry entry.

## Example Translation

### MDL Code
```mdl
pack "example" description "Test pack" pack_format 82;

namespace "test";

var num counter = 0;

function "main" {
    counter = counter + 1;
    
    if "$counter$ > 5" {
        say "Counter is high!";
    }
    
    while "$counter$ < 10" {
        counter = $counter$ + 1;
        say "Counter: $counter$";
    }
}

on_tick "test:main";
```

### Generated Minecraft Commands
```mcfunction
# test:main
scoreboard players add @s counter 1

execute if score @s counter matches 6.. run say Counter is high!

# While loop
execute while score @s counter matches ..9 run function test:loop_body

# test:loop_body
scoreboard players add @s counter 1
tellraw @s [{"text":"Counter: "},{"score":{"name":"@s","objective":"counter"}}]
```

## Implementation Status

### ✅ Implemented
- Basic syntax and structure
- Number variable declarations and assignments
- Variable substitution (`$variable$` syntax)
- Control flow (if/else, while, for loops)
- Function declarations and calls
- Hooks (on_load, on_tick)
- Tags (function)

### ❌ Removed
- String variables (too complex)
- List variables (overkill)
- Complex expressions (unnecessary)
- Module system (not needed)
- Import/export (not needed)
- Advanced error handling (keep it simple)

### 🔄 In Progress
- Control structure optimization
- Variable substitution optimization

### 📋 Planned
- Enhanced debugging tools
- Performance optimizations

This specification defines the **SIMPLIFIED** core features of MDL, focusing on **CONTROL STRUCTURES** and **SIMPLE VARIABLES** that actually work in Minecraft.
