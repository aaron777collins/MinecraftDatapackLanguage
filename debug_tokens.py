#!/usr/bin/env python3
"""
Debug script to see what tokens the lexer is generating.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack

# Test the full pipeline with a simple MDL file
test_source = '''pack "Test" description "Test pack" pack_format 82;

namespace "example";

function "hello" {
    say [example:hello] Outer says hi;
    tellraw @a {"text":"Back in hello","color":"aqua"};
}'''

print("Testing full pipeline:")
print("=" * 50)
print("Input MDL:")
print(test_source)
print("=" * 50)

print("\n1. Lexing:")
tokens = lex_mdl_js(test_source)
for token in tokens:
    print(f"  {token.type}: '{token.value}'")

print("\n2. Parsing:")
ast = parse_mdl_js(test_source)
print("AST keys:", list(ast.keys()))
print("Functions:", len(ast.get('functions', [])))
for func in ast.get('functions', []):
    print(f"  Function: {func.name}")
    print(f"  Body nodes: {len(func.body)}")
    for node in func.body:
        print(f"    {node.__class__.__name__}: {getattr(node, 'command', 'N/A')}")

print("\n3. Converting to commands:")
for func in ast.get('functions', []):
    commands = _ast_to_commands(func.body)
    print(f"  Function {func.name} commands:")
    for cmd in commands:
        print(f"    '{cmd}'")

print("\n4. Converting to Pack:")
pack = _ast_to_pack(ast, 82)
print(f"  Pack name: {pack.name}")
for ns_name, ns in pack.namespaces.items():
    print(f"  Namespace: {ns_name}")
    for func_name, func in ns.functions.items():
        print(f"    Function {func_name}: {len(func.commands)} commands")
        print(f"    Raw commands in Function object:")
        for cmd in func.commands:
            print(f"      '{cmd}'")
        
        # Check if commands have semicolons
        for cmd in func.commands:
            if cmd.endswith(';'):
                print(f"      WARNING: Command ends with semicolon: '{cmd}'")
