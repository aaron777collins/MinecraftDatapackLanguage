# MDL (Minecraft Datapack Language) AI Specification Sheet

## Overview
MDL is a JavaScript-style language that compiles to Minecraft datapack `.mcfunction` files. The language provides a modern, developer-friendly syntax for creating complex Minecraft datapacks with advanced features like variables, lists, functions, and control flow.

## Core Language Features

### 1. Basic Syntax Structure
- **Pack Declaration**: `pack "pack_name" description "description" pack_format 82;`
- **Namespace Declaration**: `namespace "namespace_name";`
- **Function Declaration**: `function "function_name" { ... }`
- **Curly Brace Blocks**: All code blocks use `{ }` syntax
- **Semicolons**: Required at the end of statements

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
- **If Statements**: `if (condition) { ... }`
- **If-Else**: `if (condition) { ... } else { ... }`
- **While Loops**: `while (condition) { ... }`
- **For Loops**: `for (var i = 0; i < 10; i++) { ... }`
- **For-In Loops**: `for (var item in list) { ... }`

### 8. Functions and Commands
- **Built-in Commands**: `say "message"`, `tellraw @s {"text":"message","color":"green"}`
- **Custom Functions**: `function "my_function" { ... }`
- **Function Calls**: `call "namespace:function_name"`

### 9. Error Handling
- **Try-Catch**: `try { ... } catch (error) { ... }`
- **Throw**: `throw "error message"`

### 10. Advanced Features
- **Nested Expressions**: Complex expressions with multiple operations
- **Variable Scope**: Proper scoping within functions and blocks
- **Type Inference**: Automatic type detection for literals
- **Memory Management**: Automatic garbage collection for temporary variables

## Compilation Architecture

### 1. Lexer (`mdl_lexer_js.py`)
- Tokenizes MDL source code into tokens
- Handles keywords, literals, operators, and punctuation
- Supports JavaScript-style syntax with curly braces

### 2. Parser (`mdl_parser_js.py`)
- Converts token stream into Abstract Syntax Tree (AST)
- Handles complex expressions and nested structures
- Supports function calls, list access, and binary operations

### 3. Expression Processor (`expression_processor.py`)
- Systematically breaks down complex expressions
- Generates temporary variables for intermediate calculations
- Handles string concatenation, arithmetic, and list operations
- Converts high-level expressions to Minecraft commands

### 4. Compiler (`cli.py`)
- Converts AST into Minecraft `.mcfunction` files
- Manages datapack structure and file organization
- Handles variable storage and scoreboard objectives
- Generates proper Minecraft command syntax

## Minecraft Integration

### 1. Variable Storage
- **Numbers**: Stored in scoreboard objectives
- **Strings**: Stored in NBT storage (`storage mdl:variables`)
- **Lists**: Stored as NBT arrays in storage
- **Temporary Variables**: Generated for complex expressions

### 2. Command Generation
- **Data Commands**: `data modify`, `data get`, `data set`
- **Scoreboard Commands**: `scoreboard players set`, `scoreboard players operation`
- **Execute Commands**: `execute store result`, `execute if`
- **Tellraw Commands**: JSON-based text display

### 3. Datapack Structure
- **Pack Metadata**: `pack.mcmeta` with format and description
- **Function Files**: `.mcfunction` files in `data/namespace/function/`
- **Tags**: Load and tick function tags for automation

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

### Important Notes
- **Always use `pipx`** for installation and upgrades
- **Never test locally** without releasing first
- **PyPI takes time** to update after release
- **First upgrade** often fails, second one works
- **Version numbers** increment automatically with patch releases

## Quality Assurance

### 1. Compilation Testing
- All MDL files must compile without errors
- Generated `.mcfunction` files must be valid Minecraft commands
- Complex expressions must be properly broken down
- Temporary variables must be correctly managed

### 2. Feature Testing
- Test each language feature individually
- Test complex nested expressions
- Test edge cases and error conditions
- Verify Minecraft command output is correct

### 3. Integration Testing
- Test complete datapack compilation
- Verify datapack structure is correct
- Test function loading and execution
- Validate NBT storage and scoreboard usage

## Future Enhancements

### 1. Language Features
- **Classes and Objects**: Object-oriented programming support
- **Modules and Imports**: Code organization and reusability
- **Advanced Types**: Custom data types and structures
- **Macros**: Code generation and metaprogramming

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
- Basic control flow
- Expression processing system

### 🔄 In Progress
- Complex nested expressions
- Error handling improvements
- Performance optimization
- Documentation updates

### 📋 Planned Features
- Advanced control flow
- Object-oriented features
- Module system
- Advanced debugging tools

## Technical Requirements

### Development Environment
- **Python 3.8+**: Core language implementation
- **Git**: Version control and collaboration
- **pipx**: Package management for development
- **Minecraft**: Target platform for testing

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
