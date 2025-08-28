#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Simple test with string variable
code = '''
pack "test" description "Test" pack_format 82;
namespace "test";

var str message = "Hello World";
'''

print("=== PARSING ===")
tokens = lex_mdl_js(code)
parser = MDLParser(tokens)
ast = parser.parse()

for func in ast.get('functions', []):
    print(f"\nFunction: {func.name}")
    for i, stmt in enumerate(func.body):
        print(f"  [{i}] {stmt.__class__.__name__}: {stmt}")
        if hasattr(stmt, 'value') and stmt.value:
            print(f"      value: {stmt.value}")
            print(f"      value type: {type(stmt.value)}")
            if hasattr(stmt.value, 'value'):
                print(f"      value.value: {stmt.value.value}")
                print(f"      value.value type: {type(stmt.value.value)}")
            if hasattr(stmt.value, 'type'):
                print(f"      value.type: {stmt.value.type}")
