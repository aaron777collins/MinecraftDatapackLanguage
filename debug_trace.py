#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack

# Simple test code
code = '''
pack "debug" description "Debug" pack_format 82;
namespace "test";
function "simple" {
    var num counter = 5;
}
'''

print("=== LEXING ===")
tokens = lex_mdl_js(code)
for token in tokens:
    print(f"{token.type.name}: {token.value}")

print("\n=== PARSING ===")
parser = MDLParser(tokens)
ast = parser.parse()

print("AST:")
print(f"Namespaces: {ast.get('namespaces', [])}")
print(f"Functions: {len(ast.get('functions', []))}")

for func in ast.get('functions', []):
    print(f"\nFunction: {func.name}")
    print(f"Body: {len(func.body)} statements")
    for i, stmt in enumerate(func.body):
        print(f"  [{i}] {stmt.__class__.__name__}: {stmt}")
        
print("\n=== COMMAND GENERATION ===")
for func in ast.get('functions', []):
    print(f"\nProcessing function: {func.name}")
    commands = _ast_to_commands(func.body)
    print(f"Generated {len(commands)} commands:")
    for i, cmd in enumerate(commands):
        print(f"  [{i}] {cmd}")

print("\n=== PACK GENERATION ===")
pack = _ast_to_pack(ast, 82)
print(f"Pack name: {pack.name}")
print(f"Namespaces: {list(pack.namespaces.keys())}")

for ns_name, ns in pack.namespaces.items():
    print(f"\nNamespace: {ns_name}")
    print(f"Functions: {list(ns.functions.keys())}")
    
    for func_name, func in ns.functions.items():
        print(f"\n  Function: {func_name}")
        print(f"  Commands: {len(func.commands)}")
        for i, cmd in enumerate(func.commands):
            print(f"    [{i}] {cmd}")
