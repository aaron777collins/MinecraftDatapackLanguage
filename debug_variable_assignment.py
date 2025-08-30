#!/usr/bin/env python3
"""
Debug script to test variable assignment processing
"""

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.expression_processor import ExpressionProcessor
from minecraft_datapack_language.cli import _ast_to_pack
import tempfile
import os

# Test code with variable assignment
code = '''
pack "test" "description" 82;
namespace "test";
var num counter = 0;
function "main" {
    say "Initial counter: $counter$";
    counter = $counter$ + 1;
    say "After increment: $counter$";
}
'''

print("Parsing MDL code...")
ast = parse_mdl_js(code)

print("AST keys:", list(ast.keys()))
if 'functions' in ast:
    print("Functions found:", len(ast['functions']))
    for i, func in enumerate(ast['functions']):
        print(f"Function {i}: {func['name']}")
        print(f"  Body statements: {len(func['body'])}")
        for j, stmt in enumerate(func['body']):
            print(f"    Statement {j}: {type(stmt).__name__}")
            if hasattr(stmt, 'name'):
                print(f"      Name: {stmt.name}")
            if hasattr(stmt, 'value'):
                print(f"      Value: {stmt.value}")

# Test expression processor directly
print("\nTesting expression processor...")
expression_processor = ExpressionProcessor()
selector = "@e[type=armor_stand,tag=mdl_server,limit=1]"

# Find the variable assignment
for func in ast['functions']:
    for stmt in func['body']:
        if hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'VariableAssignment':
            print(f"Processing variable assignment: {stmt.name} = {stmt.value}")
            result = expression_processor.process_expression(stmt.value, stmt.name, selector)
            print(f"Result temp_assignments: {result.temp_assignments}")
            print(f"Result final_command: {result.final_command}")

# Test _ast_to_pack
print("\nTesting _ast_to_pack...")
with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f:
    f.write(code)
    f_path = f.name

try:
    pack = _ast_to_pack(ast, [f_path])
    print(f"Pack created: {pack.name}")
    
    namespace = pack.namespace('test')
    print(f"Namespace created: {namespace}")
    
    function = namespace.function('main')
    print(f"Function created: {function}")
    
    commands = function.commands
    print(f"Commands generated: {len(commands)}")
    for i, cmd in enumerate(commands):
        print(f"  Command {i}: {cmd}")
        
finally:
    os.unlink(f_path)
