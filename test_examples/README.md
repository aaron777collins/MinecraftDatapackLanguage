# MDL Test Suite - Modern JavaScript-Style Syntax

This test suite validates the new JavaScript-style MDL language implementation with curly braces, semicolons, and modern programming constructs.

## Test Categories

### 1. Basic Syntax Tests
- `hello_world.mdl` - Basic pack declaration and function
- `variables.mdl` - Variable declarations and assignments
- `functions.mdl` - Function definitions and calls

### 2. Control Flow Tests
- `conditionals.mdl` - If/else statements with complex conditions
- `loops.mdl` - While and for loops with entity iteration
- `nested_control.mdl` - Nested control structures

### 3. Data Structure Tests
- `lists.mdl` - List operations (append, remove, insert, pop, clear)
- `list_access.mdl` - List indexing and length operations
- `complex_data.mdl` - Complex data manipulation

### 4. Advanced Features
- `namespaces.mdl` - Multiple namespaces and cross-namespace calls
- `hooks.mdl` - Load and tick hooks
- `tags.mdl` - Function and item tags
- `error_handling.mdl` - Try-catch blocks and error handling

### 5. Real-World Examples
- `adventure_pack.mdl` - Complete adventure pack with multiple features
- `combat_system.mdl` - Combat mechanics with variables and conditionals
- `ui_system.mdl` - User interface system with lists and loops

## Running Tests

```bash
# Run all tests
python run_all_tests.py

# Test individual files
mdl check test_examples/hello_world.mdl
mdl build --mdl test_examples/hello_world.mdl -o dist
```

## Test Structure

Each test file demonstrates:
- Modern pack declarations with metadata
- JavaScript-style syntax with curly braces
- Variable declarations with types (num, str, list)
- Control flow with proper block structure
- List operations and data manipulation
- Cross-namespace function calls
- Proper error handling

## Expected Behavior

All tests should:
1. Parse successfully without syntax errors
2. Generate valid Minecraft datapack files
3. Demonstrate proper variable scoping and data flow
4. Show correct control flow implementation
5. Handle complex data structures properly
