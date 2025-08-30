#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Read the test1.mdl file
with open('test1.mdl', 'r', encoding='utf-8') as f:
    source = f.read()

# Parse the MDL file
ast = parse_mdl_js(source)

print("AST keys:", list(ast.keys()))
print("\nHooks:", ast.get('hooks', []))
print("\nFunctions:")
for func in ast.get('functions', []):
    if isinstance(func, dict):
        print(f"  {func.get('name', 'unknown')}")
    else:
        print(f"  {getattr(func, 'name', 'unknown')}")

print("\nFull AST:")
import json
print(json.dumps(ast, indent=2, default=str))
