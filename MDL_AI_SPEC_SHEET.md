# MDL (Minecraft Datapack Language) - Simplified AI Specification

## Overview
MDL is a **SIMPLE** language that compiles to Minecraft datapack `.mcfunction` files. This specification focuses on **CONTROL STRUCTURES** and **SIMPLE VARIABLES** - the core problems that need solving.

All manual testing (making temp files, builds, etc.) needs to happen in .tmp

## Core Language Features (SIMPLIFIED)

### ✅ **IMPLEMENTED** - Basic Syntax Structure  
- **Pack Declaration**: `pack "pack_name" description "description" pack_format 82;`
- **Namespace Declaration**: `namespace "namespace_name";`
- **Function Declaration**: `function "function_name" { ... }`
- **Curly Brace Blocks**: All code blocks use `{ }` syntax
- **Semicolons**: Required at the end of statements
- **No Indentation Requirements**: Uses explicit block boundaries

### ✅ **IMPLEMENTED** - Simple Variable System
- **Variable Type**: Only `num` (numbers stored in scoreboard objectives)
- **Declaration**: `var num variable_name = value;`
- **Assignment**: `variable_name = new_value;`
- **Variable Substitution**: `$variable_name$` in strings and conditions

### ✅ **IMPLEMENTED** - Control Flow (THE MAIN FOCUS)
- **If Statements**: `if "condition" { ... }` ✅ (WORKING)
- **If-Else**: `if "condition" { ... } else { ... }` ✅ (WORKING)
- **While Loops**: `while "condition" { ... }` ✅ (WORKING)
- **For Loops**: `for variable in selector { ... }` ✅ (WORKING)

### ✅ **IMPLEMENTED** - Simple Commands
- **Built-in Commands**: `say "message"`, `tellraw @s {"text":"message"}`
- **Custom Functions**: `function "my_function" { ... }`
- **Function Calls**: `function "namespace:function_name"`

### ✅ **IMPLEMENTED** - Hooks and Tags
- **Load Hook**: `on_load "namespace:function_name"`
- **Tick Hook**: `on_tick "namespace:function_name"`
- **Function Tags**: `tag function minecraft:load { add "namespace:function_name"; }`

## Language Syntax (SIMPLIFIED)

### Variable System
```mdl
// Only number variables stored in scoreboard
var num counter = 0;
var num health = 20;
var num level = 1;

// Assignment
counter = 42;
health = health - 5;

// Variable substitution in strings and conditions
say "Health: $health$";
if "$health$ < 10" {
    say "Low health!";
}
```

### Control Structures
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

// While loops
while "$counter$ < 10" {
    counter = $counter$ + 1;
    say "Counter: $counter$";
}

// For loops (entity iteration)
for player in @a {
    say "Hello $player$";
}
```

### Functions and Commands
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

// Function calls
function "namespace:helper";

// Selector on function calls (executes as selector)
// Compiles to: execute as @a run function test:hello
function "test:hello<@a>";
```

## Compilation Strategy (SIMPLIFIED)

### Variable Storage
- **All variables**: Stored in scoreboard objectives
  ```mcfunction
  scoreboard players set @s counter 42
  scoreboard players set @s health 20
  ```

### Variable Substitution
- **Pattern**: `$variable_name$` → `score @s variable_name`
- **In strings**: `"Health: $health$"` → `[{"text":"Health: "},{"score":{"name":"@s","objective":"health"}}]`
- **In conditions**: `"$health$ < 10"` → `"score @s health matches ..9"`

### Control Flow Translation
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

## Implementation Status

### ✅ **CORE FEATURES WORKING**
- Basic pack/namespace/function structure
- Number variables (scoreboard storage)
- Variable substitution (`$variable$` syntax)
- If/else statements
- While loops
- For loops (entity iteration)
- Function calls
- Hooks (on_load, on_tick)
- Tags (function)

### ❌ **REMOVED COMPLEXITY**
- String variables (removed)
- List variables (removed)
- Complex expressions (removed)
- List operations (removed)
- Module system (removed)
- Import/export (removed)
- Complex arithmetic (simplified)
- String concatenation (simplified)

## Development System

### ✅ **IMPLEMENTED** - Dual Command System
- **Stable Command**: `mdl` - Globally installed stable version
- **Development Command**: `mdlbeta` - Local development version for testing
- **Setup Scripts**: `scripts/dev_setup.sh` and `scripts/dev_setup.ps1`
- **Build Scripts**: `scripts/dev_build.sh` and `scripts/dev_build.ps1`
- **Test Scripts**: `scripts/test_dev.sh` and `scripts/test_dev.ps1`

### Project Scaffolding (mdl new)
- Generates main `.mdl` file and `README.md`
- Now also generates `LANGUAGE_REFERENCE.md` in the project root
- README includes a link to the website docs: https://aaron777collins.github.io/MinecraftDatapackLanguage/docs/

JSON registry handling:
- Recipe, loot_table, advancement, predicate, item_modifier, structure declarations now resolve `"json_file"` paths relative to the MDL file where they are declared (multi-file safe).
- Missing or invalid JSON emits a warning and compiles with an empty object.

## Compilation Architecture (SIMPLIFIED)

### ✅ **IMPLEMENTED** - Lexer (`mdl_lexer_js.py`)
- **Token Recognition**: Keywords, operators, and literals
- **Variable Substitution**: Recognition of `$variable$` patterns
- **Error Recovery**: Graceful handling of invalid tokens

### ✅ **IMPLEMENTED** - Parser (`mdl_parser_js.py`)  
- **AST Generation**: Simplified Abstract Syntax Tree construction
- **Grammar Rules**: Focus on control structures and simple variables
- **Error Reporting**: Clear syntax error messages

### ✅ **IMPLEMENTED** - Compiler (`cli.py`)
- **AST to Commands**: Translation from AST to Minecraft commands
- **Variable Substitution**: `$variable$` → scoreboard operations
- **Control Flow**: Proper if/else/while/for generation
- **Function Generation**: Proper function creation and management

## Testing Status

### **Comprehensive Test Coverage**
- ✅ Basic hello world examples
- ✅ Variable declarations and assignments
- ✅ Variable substitution in strings and conditions
- ✅ If/else statements
- ✅ While loops
- ✅ For loops
- ✅ Function calls and hooks
- ✅ Tag declarations

### **Test Files Available**
- `test_examples/hello_world.mdl` ✅
- `test_examples/variables.mdl` ✅
- `test_examples/conditionals.mdl` ✅
- `test_examples/loops.mdl` ✅

### 2025-08-30 Cleanup
- Removed generated debug/test dist folders and zip artifacts at repo root (dist_debug*, dist_multi*, dist_test*, dist_old*, dist_*_run, dist_final, test_output*, etc.). None are referenced by CI/docs/runtime.
- Removed root-level MDL test files: `test.mdl`, `test_linter_errors.mdl`, `test_old_format.mdl`, `test_very_old_format.mdl`, and stray `other.mdl`. CI uses `test_examples/**` instead.
- Trimmed `test_new_pack/dist_test_new` and related zip artifacts. Kept the actual example sources.
- Fixed dead code in `minecraft_datapack_language/pack.py`: removed unused import `ns_path` and dropped unused parameter `cmd_index` from `_process_list_access_in_condition`; updated callsite accordingly. Recompiled; static scan clean.
- Verified functionality: dev build installed `mdlbeta`; `mdlbeta check` and `check-advanced` on `test_examples/hello_world.mdl` passed; `mdlbeta build` produced a valid `dist/`.

## Current Version Status

**Latest Version**: Sourced dynamically on website via GitHub Releases
**Status**: Simplified MDL compiler focused on control structures
**Known Issues**: All major complexity removed!
**Next Priority**: Ensure control structures work perfectly

The MDL language implementation is now **SIMPLIFIED** and focused on the core problem: **CONTROL STRUCTURES**. We've removed all the complexity that was causing issues and focused on making if/else, while, and for loops work correctly with simple number variables.

## Known Issues and Limitations

### ✅ **SIMPLIFIED APPROACH**
- **Variables**: Only numbers stored in scoreboard (no strings, no lists)
- **Variable Substitution**: `$variable$` syntax for reading from scoreboard
- **Control Structures**: Assembly-like jumps when conditions are false
- **Commands**: Simple Minecraft commands only
- **No Complex Expressions**: Keep it simple and working

### ❌ **REMOVED FEATURES**
- String variables (too complex)
- List variables (overkill)
- Complex arithmetic expressions (unnecessary)
- Module system (not needed)
- Import/export (not needed)
- Advanced error handling (keep it simple)

This simplified approach focuses on **MAKING CONTROL STRUCTURES WORK** rather than building a complex language that doesn't compile correctly.

## Documentation and Website Automation

- Docs navigation cleaned to remove unused legacy links in `docs/_config.yml`.
- Downloads page now auto-sources the latest release using `jekyll-github-metadata` with fallbacks to `docs/_data/version.yml`.
- Added scheduled and release-triggered workflow `update-website-version.yml` to update `docs/_data/version.yml` with the latest GitHub release tag and version.
- Docs deploy workflow passes `JEKYLL_GITHUB_TOKEN` to enable GitHub release metadata during Jekyll builds.
-
- Removed legacy theme header in `docs/_layouts/default.html` to avoid duplicate navigation with the enhanced nav include.
- Added a GitHub icon link to `docs/_includes/navigation.html` targeting `https://github.com/{{ site.github_username }}/{{ site.github_repo }}`.
— 2025-08-31 Mobile header fix: Removed duplicate viewport/meta and conflicting nav styles from `docs/_includes/head-custom.html`. Capped mobile menu height with scroll, disabled sticky on small screens, and auto-close on link tap in `docs/_includes/navigation.html` to prevent the header occupying excessive space on mobile.
