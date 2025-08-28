# MDL (Minecraft Datapack Language) AI Specification Sheet

NOTE: we want to fully implement this language. If you get stuck, take a step back and think about a better solution.

## Overview
MDL is a JavaScript-style language that compiles to Minecraft datapack `.mcfunction` files. The language provides a modern, developer-friendly syntax for creating complex Minecraft datapacks with advanced features like variables, lists, functions, control flow, and error handling.

## Core Language Features

### 1. Basic Syntax Structure
- **Pack Declaration**: `pack "pack_name" description "description" pack_format 82;`
- **Namespace Declaration**: `namespace "namespace_name";`
- **Function Declaration**: `function "function_name" { ... }`
- **Curly Brace Blocks**: All code blocks use `{ }` syntax (JavaScript-style)
- **Semicolons**: Required at the end of statements
- **No Indentation Requirements**: Uses explicit block boundaries instead of indentation

### 2. Variable System
- **Variable Types**:
  - `num`: Integer variables (stored in scoreboard objectives)
  - `str`: String variables (stored in NBT storage)
  - `list`: Array variables (stored in NBT storage as arrays)
- **Declaration**: `var type variable_name = value;`
- **Assignment**: `variable_name = new_value;`

### 3. Data Types and Literals
- **Numbers**: `42`, `-10`, `3.14`
- **Strings**: `"Hello World"`, `'Single quotes too'`
- **Lists**: `["item1", "item2", "item3"]`
- **Nested Lists**: `[["a", "b"], ["c", "d"]]`

### 4. List Operations
- **List Access**: `list_name[index]` (supports variable and literal indices)
- **List Length**: `length(list_name)` (built-in function)
- **List Append**: `append list_name "new_item"`
- **List Remove**: `remove list_name[index]`
- **List Insert**: `insert list_name[index] "new_item"`
- **List Pop**: `pop list_name`
- **List Clear**: `clear list_name`

### 5. String Operations
- **String Concatenation**: `"Hello" + " " + "World"`
- **Variable Interpolation**: `"Value: $variable_name"`
- **Complex Concatenation**: `"Found " + item + " at index " + index`

### 6. Arithmetic Operations
- **Basic Operations**: `+`, `-`, `*`, `/`
- **Complex Expressions**: `(count + 5) * 2`
- **Variable Operations**: `result = a + b * c`

### 7. Control Flow
- **If Statements**: `if "condition" { ... }`
- **If-Else**: `if "condition" { ... } else { ... }`
- **While Loops**: `while "condition" { ... }`
- **For Loops**: `for variable in selector { ... }`
- **For-In Loops**: `for (var item in list) { ... }` (planned feature)

### 8. Functions and Commands
- **Built-in Commands**: `say "message"`, `tellraw @s {"text":"message","color":"green"}`
- **Custom Functions**: `function "my_function" { ... }`
- **Function Calls**: `function "namespace:function_name"`
- **Cross-namespace Calls**: `function "namespace:function_name"`

### 9. Error Handling
- **Conditional Error Prevention**: Use if statements to prevent errors
- **Bounds Checking**: Check list indices and array bounds before access
- **Safe Operations**: Validate conditions before performing operations

### 10. Advanced Features
- **Nested Expressions**: Complex expressions with multiple operations
- **Variable Scope**: Proper scoping within functions and blocks
- **Type Inference**: Automatic type detection for literals
- **Memory Management**: Automatic garbage collection for temporary variables
- **Explicit Block Boundaries**: All control structures use curly braces `{ }`
- **Minecraft Selector Integration**: Conditions use valid Minecraft selector syntax
- **Modern Datapack Format**: Uses pack format 82+ by default for latest features
- **Multi-file Support**: Compile multiple MDL files into a single datapack

## Compilation Architecture

### 1. Lexer (`mdl_lexer_js.py`)
- Tokenizes MDL source code into tokens
- Handles keywords, literals, operators, and punctuation
- Supports JavaScript-style syntax with curly braces and semicolons
- No indentation-based parsing - uses explicit block boundaries

### 2. Parser (`mdl_parser_js.py`)
- Converts token stream into Abstract Syntax Tree (AST)
- Handles complex expressions and nested structures
- Supports function calls, list access, and binary operations
- Parses curly brace blocks and semicolon-terminated statements
- Supports control flow (if/else, while, for loops)

### 3. Expression Processor (`expression_processor.py`)
- Systematically breaks down complex expressions
- Generates temporary variables for intermediate calculations
- Handles string concatenation, arithmetic, and list operations
- Converts high-level expressions to Minecraft commands
- Manages temporary variable cleanup and memory optimization

### 4. Compiler (`cli.py`)
- Converts AST into Minecraft `.mcfunction` files
- Manages datapack structure and file organization
- Handles variable storage and scoreboard objectives
- Generates proper Minecraft command syntax
- Compiles control flow structures to separate functions
- Handles loops, variables, and list operations

## Minecraft Integration

### 1. Variable Storage
- **Numbers**: Stored in scoreboard objectives
- **Strings**: Stored in NBT storage (`storage mdl:variables`)
- **Lists**: Stored as NBT arrays in storage
- **Temporary Variables**: Generated for complex expressions
- **Modern Format**: Defaults to pack format 82+ for modern datapack features

### 2. Command Generation
- **Data Commands**: `data modify`, `data get`, `data set`
- **Scoreboard Commands**: `scoreboard players set`, `scoreboard players operation`
- **Execute Commands**: `execute store result`, `execute if`, `execute as`
- **Tellraw Commands**: JSON-based text display
- **Control Flow**: Generates separate functions for complex control structures

### 3. Datapack Structure
- **Pack Metadata**: `pack.mcmeta` with format and description
- **Function Files**: `.mcfunction` files in `data/namespace/function/`
- **Tags**: Load and tick function tags for automation
- **Modern Format**: Uses pack format 82+ by default for latest features

## Testing Workflow

### Development Cycle
When testing changes to the MDL language, follow this exact workflow:

1. **Make Code Changes**
   - Edit source files in `minecraft_datapack_language/`
   - Test locally if possible

2. **Commit and Push**
   ```bash
   git add .
   git commit -m "descriptive message"
   git push
   ```

3. **Release New Version**
   ```bash
   ./scripts/release.sh patch
   ```

4. **Wait for PyPI**
   ```bash
   # Wait 20 seconds for PyPI to update
   sleep 20
   ```

5. **Upgrade MDL Package**
   ```bash
   pipx upgrade minecraft-datapack-language
   ```

6. **Repeat Upgrade** (First one primes PyPI)
   ```bash
   pipx upgrade minecraft-datapack-language
   ```

7. **Test Changes**
   ```bash
   mdl build --mdl test_file.mdl -o output_dir --verbose
   ```
   Check the output to ensure the outputted files are valid mcfunction files and work as a datapack

### Important Notes
- **Always use `pipx`** for installation and upgrades
- **Never test locally** without releasing first
- **PyPI takes time** to update after release
- **First upgrade** often fails, second one works
- **Version numbers** increment automatically with patch releases
- **Remove all old features you come across** We want to remove old features in the docs, examples, tests, etc. For example: we stopped supporting try catch and switch statements.
- **Fix core features and test them** We want core features like mdl new <name> to work. Test them to make sure it works. We also want to verify the output compiles and the output files actually work as a minecraft datapack
- **Check mdl version when doubting** use mdl --version to check the version we have locally. Upload our changes, release, wait, upgrade mdl then test.

## Quality Assurance

### 1. Compilation Testing
- All MDL files must compile without errors
- Generated `.mcfunction` files must be valid Minecraft commands
- Complex expressions must be properly broken down
- Temporary variables must be correctly managed
- Control flow structures must generate valid function calls
- Variable assignments and list operations must work correctly

### 2. Feature Testing
- Test each language feature individually
- Test complex nested expressions
- Test edge cases and error conditions
- Verify Minecraft command output is correct
- Test control flow structures (if/else, while, for)
- Test variable operations and assignments
- Test list operations and string concatenation

### 3. Integration Testing
- Test complete datapack compilation
- Verify datapack structure is correct
- Test function loading and execution
- Validate NBT storage and scoreboard usage

## Future Enhancements

### 1. Language Features
- **For-in Loops**: List iteration with `for (var item in list)`
- **Enhanced List Operations**: More efficient list manipulation
- **Advanced Variable Types**: Support for more complex data structures
- **Modules and Imports**: Code organization and reusability
- **Performance Optimizations**: Faster compilation and execution

### 2. Compiler Improvements
- **Optimization**: Reduce generated command count
- **Error Recovery**: Better error messages and recovery
- **Debugging**: Source maps and debugging information
- **Performance**: Faster compilation and better memory usage

### 3. Tooling
- **IDE Support**: Better syntax highlighting and autocomplete
- **Debugging Tools**: Step-through debugging for MDL code
- **Profiling**: Performance analysis of generated commands
- **Documentation**: Auto-generated API documentation

## Implementation Status

### ✅ Completed Features
- Basic syntax parsing and compilation
- Variable declarations and assignments
- List operations and access
- String concatenation
- Arithmetic operations
- Function declarations
- Control flow (if/else, while, for loops)
- Expression processing system
- Modern datapack format (82+) by default

### ✅ Recently Completed
- For-in loops for list iteration (`for (var item in list)`)
- Enhanced list operations (insert, remove, pop, clear)
- Module system (import/export statements)
- Enhanced error handling and debugging
- Performance optimizations
- Complex nested expressions optimization

### 📋 Planned Features
- Advanced control flow optimizations
- Advanced debugging tools (source maps, step-through debugging)
- Enhanced error recovery
- Advanced variable types (objects, custom data structures)
- Performance optimizations (further command reduction)
- IDE integration improvements

## Bug Tracking & Issues

### 🐛 Known Bugs & Issues

#### High Priority (Fix ASAP)
1. **`mdl new` command creates redundant directory structure**
   - **Issue**: Creates `example/example` instead of just `example`
   - **Status**: ✅ FIXED - Now creates proper directory structure with better file naming
   - **Solution**: Fixed directory creation logic and improved file naming

2. **Expression processor import debug message**
   - **Issue**: Shows debug message on every command execution
   - **Status**: 🔄 IN PROGRESS - Should be removed or made optional
   - **Impact**: Clutters output, not user-friendly

#### Medium Priority
3. **Switch statements and try-catch not fully implemented**
   - **Issue**: Parser supports them but compiler doesn't handle them properly
   - **Status**: ✅ RESOLVED - Removed from spec as not needed at this stage
   - **Solution**: Simplified to focus on core features

4. **For-in loops need better error handling**
   - **Issue**: No bounds checking for list iteration
   - **Status**: 🔄 IN PROGRESS - Basic implementation exists, needs enhancement

#### Low Priority
5. **Performance optimization needed**
   - **Issue**: Generated commands could be more efficient
   - **Status**: 📋 PLANNED - Basic optimizations implemented, more needed

### 🚀 Feature Requests
1. **Source maps for debugging**
2. **Step-through debugging support**
3. **Advanced variable types (objects)**
4. **IDE integration improvements**

### 📝 Bug Reporting Guidelines
- Always include the exact command that caused the issue
- Include the MDL source code that reproduces the bug
- Specify the expected vs actual behavior
- Include any error messages or debug output

## Technical Requirements
- **Python 3.8+**: Core language implementation
- **Git**: Version control and collaboration
- **pipx**: Package management for development
- **Minecraft**: Target platform for testing
- **Modern Datapack Format**: Pack format 82+ for latest features

### Dependencies
- **setuptools**: Package building and distribution
- **wheel**: Binary package format
- **build**: Modern Python packaging

### Testing Requirements
- **Valid MDL Files**: Test cases for all features
- **Minecraft Server**: For datapack testing
- **Automated Tests**: CI/CD pipeline integration
- **Manual Testing**: Complex scenario validation

---

*This specification is a living document and should be updated as the language evolves.*
