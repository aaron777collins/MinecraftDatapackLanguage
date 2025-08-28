# MDL (Minecraft Datapack Language) Specification

## Overview
MDL is a JavaScript-style language that compiles to Minecraft datapack `.mcfunction` files. This specification defines the core MVP features and how they translate to Minecraft commands.

## Language Syntax Reference

### 1. Pack and Namespace Declarations
```mdl
pack "pack_name" description "description" pack_format 82;
namespace "namespace_name";
```

### 2. Variable Declarations and Assignments
```mdl
var num counter = 0;
var str message = "Hello World";
var list items = ["apple", "banana", "cherry"];

counter = 42;
message = "Updated message";
items = ["new", "list", "items"];
```

### 3. Function Declarations
```mdl
function "main" {
    say "Hello from main function";
}

function "helper" {
    var num result = 0;
    result = 5 + 3;
    say "Result: " + result;
}
```

### 4. Control Flow Statements
```mdl
// If statements
if "score @s counter > 5" {
    say "Counter is high!";
}

// If-else statements
if "score @s health < 10" {
    say "Health is low!";
} else {
    say "Health is okay";
}

// While loops
while "score @s counter < 10" {
    counter = counter + 1;
    say "Counter: " + counter;
}

// For loops (entity iteration)
for player in @a {
    say "Hello " + player;
}

// For-in loops (list iteration)
for (var item in items) {
    say "Found: " + item;
}
```

### 5. List Operations
```mdl
var list fruits = ["apple", "banana"];

// List access
var str first = fruits[0];
var str second = fruits[1];

// List length
var num count = length(fruits);

// List append
append fruits "orange";

// List remove
remove fruits[1];

// List insert
insert fruits[1] "grape";

// List pop
var str last = pop fruits;

// List clear
clear fruits;
```

### 6. String Operations
```mdl
var str greeting = "Hello";
var str name = "Player";
var str message = greeting + " " + name;

// String interpolation
var str status = "Health: $health";

// Complex concatenation
var str result = "Found " + item + " at index " + index;
```

### 7. Arithmetic Operations
```mdl
var num a = 10;
var num b = 5;
var num result = 0;

// Basic operations
result = a + b;    // 15
result = a - b;    // 5
result = a * b;    // 50
result = a / b;    // 2

// Complex expressions
result = (a + b) * 2;  // 30
result = a + b * c;    // 10 + (5 * c)

// Unary minus
var num negative = -42;
var num opposite = -a;
```

### 8. Function Calls
```mdl
function "namespace:function_name";
function "helper";
function "utils:calculator";
```

### 9. Built-in Commands
```mdl
say "Hello World";
tellraw @s {"text":"Colored message","color":"green"};
```

### 10. Hooks
```mdl
on_load "namespace:init";
on_tick "namespace:main";
```

### 11. Tags
```mdl
// Function tags
tag function minecraft:load {
    add "namespace:init";
}

tag function minecraft:tick {
    add "namespace:main";
    add "namespace:update";
}

// Item tags
tag item namespace:swords {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

// Block tags
tag block namespace:glassy {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
```

### 12. Error Prevention
```mdl
// Bounds checking
if "score @s index < length(items)" {
    var str item = items[index];
} else {
    say "Index out of bounds";
}

// Division by zero prevention
if "score @s divisor != 0" {
    result = dividend / divisor;
} else {
    say "Division by zero prevented";
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
    LET = "LET"
    CONST = "CONST"
    NUM = "NUM"
    STR = "STR"
    LIST = "LIST"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"
    APPEND = "APPEND"
    REMOVE = "REMOVE"
    INSERT = "INSERT"
    POP = "POP"
    CLEAR = "CLEAR"
    
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
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    DOT = "DOT"
    COLON = "COLON"
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
```

### Lexer Rules
1. **Keywords**: Recognized before identifiers (e.g., `function`, `if`, `while`)
2. **Special Cases**:
   - `tag function` is tokenized as `TAG` + `IDENTIFIER` (not `FUNCTION`)
   - `for` loops are handled specially for entity iteration
   - `else if` is tokenized as `ELSE_IF`
3. **Strings**: Support both single and double quotes
4. **Numbers**: Support integers, decimals, and negative numbers
5. **Identifiers**: Start with letter/underscore, contain alphanumeric/underscore
6. **Whitespace**: Newlines are preserved, other whitespace is ignored

### Lexer Tokenization Examples
```mdl
// Input: var num counter = 0;
// Tokens: VAR, NUM, IDENTIFIER("counter"), ASSIGN, NUMBER("0"), SEMICOLON

// Input: if "score @s counter > 5" {
// Tokens: IF, STRING("score @s counter > 5"), LBRACE

// Input: for (var item in items) {
// Tokens: FOR, LPAREN, VAR, IDENTIFIER("item"), IN, IDENTIFIER("items"), RPAREN, LBRACE

// Input: tag function minecraft:load {
// Tokens: TAG, IDENTIFIER("function"), IDENTIFIER("minecraft:load"), LBRACE
```

## Parser Specification

### AST Node Types
```python
# Core Nodes
@dataclass
class PackDeclaration:
    name: str
    description: str
    pack_format: int
    min_format: Optional[PackFormat]

@dataclass
class NamespaceDeclaration:
    name: str

@dataclass
class FunctionDeclaration:
    name: str
    body: List[Statement]

@dataclass
class VariableDeclaration:
    var_type: str  # "var", "let", "const"
    data_type: str  # "num", "str", "list"
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
class ForInLoop:
    variable: str
    list_name: str
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
    value: Union[int, float, str, List]

@dataclass
class VariableExpression:
    name: str

@dataclass
class BinaryExpression:
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryExpression:
    operator: str
    operand: Expression

@dataclass
class ListAccessExpression:
    list_name: str
    index: Expression

@dataclass
class ListLengthExpression:
    list_name: str

@dataclass
class ListOperation:
    operation: str  # "append", "remove", "insert", "pop", "clear"
    list_name: str
    args: List[Expression]
```

### Parser Rules
1. **Top-level**: Pack, namespace, function declarations, hooks, tags
2. **Statements**: Variable declarations, assignments, control flow, function calls
3. **Expressions**: Literals, variables, binary operations, list operations
4. **Precedence**: Follows standard arithmetic precedence
5. **Associativity**: Left-to-right for most operators

## Compiler Specification

### Minecraft Command Generation

#### Variable Storage
- **Numbers**: Stored in scoreboard objectives
  ```mcfunction
  scoreboard players set @s variable_name 42
  ```
- **Strings**: Stored in NBT storage `mdl:variables`
  ```mcfunction
  data modify storage mdl:variables variable_name set value "Hello"
  ```
- **Lists**: Stored in NBT storage `mdl:variables` as arrays
  ```mcfunction
  data modify storage mdl:variables list_name append value "item"
  ```

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
- **For-In Loops**: Generate helper functions for iteration
  ```mcfunction
  # Generated helper functions manage loop index and current element
  scoreboard players set @s loop_index 0
  data modify storage mdl:variables current_item set from storage mdl:variables list_name[{loop_index}]
  ```

#### Expression Translation
- **Arithmetic**: Use `execute store result` commands
  ```mcfunction
  execute store result score @s result run data get storage mdl:variables a
  execute store result score @s temp run data get storage mdl:variables b
  scoreboard players operation @s result += @s temp
  ```
- **String Concatenation**: Use `data modify` with string operations
  ```mcfunction
  data modify storage mdl:variables result set value ""
  data modify storage mdl:variables result append value "Hello"
  data modify storage mdl:variables result append value " "
  data modify storage mdl:variables result append from storage mdl:variables name
  ```

#### List Operations Translation
- **Access**: Use NBT path with index
  ```mcfunction
  data modify storage mdl:variables result set from storage mdl:variables list_name[{index}]
  ```
- **Length**: Use `data get` with array length
  ```mcfunction
  execute store result score @s length run data get storage mdl:variables list_name
  ```
- **Modify**: Use `data modify` with append/remove/insert
  ```mcfunction
  data modify storage mdl:variables list_name append value "new_item"
  data remove storage mdl:variables list_name[{index}]
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

## Error Handling

### Compile-time Errors
- Syntax errors (invalid tokens, missing semicolons)
- Type errors (invalid operations on types)
- Undefined variables
- Invalid function calls

### Runtime Safety
- List bounds checking before access
- Division by zero prevention
- Null pointer prevention
- Safe string operations

## Performance Considerations

### Command Optimization
- Minimize temporary variables
- Reuse scoreboard objectives
- Batch operations where possible
- Use efficient NBT paths

### Memory Management
- Automatic garbage collection of temporary variables
- Efficient storage layout
- Minimal NBT nesting

## Example Translation

### MDL Code
```mdl
pack "example" description "Test pack" pack_format 82;

namespace "test";

var num counter = 0;
var list items = ["apple", "banana", "cherry"];

function "main" {
    counter = counter + 1;
    
    if "score @s counter > 5" {
        say "Counter is high!";
    }
    
    for (var item in items) {
        say "Found: " + item;
    }
}

on_tick "test:main";
```

### Generated Minecraft Commands
```mcfunction
# test:main
scoreboard players add @s counter 1

execute if score @s counter matches 6.. run say Counter is high!

# For-in loop helpers generated automatically
scoreboard players set @s loop_index 0
data modify storage mdl:variables current_item set from storage mdl:variables items[{loop_index}]
say Found: apple
scoreboard players add @s loop_index 1
# ... continues for all items
```

## Implementation Status

### ✅ Implemented
- Basic syntax and structure
- Variable declarations and assignments
- Control flow (if/else, while, for loops)
- List operations (append, remove, access, length)
- String concatenation
- Arithmetic operations
- Function declarations and calls
- Hooks (on_load, on_tick)
- Tags (function, item, block)
- Unary minus support
- Error handling and bounds checking

### 🔄 In Progress
- Performance optimizations
- Advanced debugging tools
- Enhanced error recovery

### 📋 Planned
- Advanced control flow optimizations
- IDE integration improvements
- Advanced variable types (objects)
- Module system enhancements

This specification defines the core MVP features of MDL, focusing on practical functionality that translates cleanly to Minecraft datapack commands.
