#!/usr/bin/env python3
"""
Debug script to test the user's file specifically
"""

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_pack
import tempfile
import os

# User's code with corrected syntax
code = '''
// hello.mdl
pack "My First Pack" "A simple example" 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = $counter$ + 1;
    say Counter: $counter$;
}

on_load "example:hello";
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

# Test _ast_to_pack
print("\nTesting _ast_to_pack...")
with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f:
    f.write(code)
    f_path = f.name

try:
    pack = _ast_to_pack(ast, [f_path])
    print(f"Pack created: {pack.name}")
    
    namespace = pack.namespace('example')
    print(f"Namespace created: {namespace}")
    
    function = namespace.function('hello')
    print(f"Function created: {function}")
    
    commands = function.commands
    print(f"Commands generated: {len(commands)}")
    for i, cmd in enumerate(commands):
        print(f"  Command {i}: {cmd}")
        
finally:
    os.unlink(f_path)
