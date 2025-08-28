#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test with the actual broken test file
with open('test_broken/mypack.mdl', 'r') as f:
    test_source = f.read()

print("Testing AST structure:")
print("=" * 60)

# Parse the MDL
ast = parse_mdl_js(test_source)

print("AST keys:", list(ast.keys()))
print("Namespaces:", len(ast.get('namespaces', [])))
print("Functions:", len(ast.get('functions', [])))
print("Hooks:", len(ast.get('hooks', [])))
print("Tags:", len(ast.get('tags', [])))

# Show namespace structure
for i, namespace in enumerate(ast.get('namespaces', [])):
    print(f"\nNamespace {i}: {namespace.name}")

# Show function structure with namespace info
for i, func in enumerate(ast.get('functions', [])):
    namespace_name = getattr(func, 'namespace', 'unknown')
    print(f"\nFunction {i}: {func.name} (namespace: {namespace_name})")
    print(f"  Body nodes: {len(func.body)}")
    for j, node in enumerate(func.body):
        print(f"    Node {j}: {node.__class__.__name__}")

print("\nAST structure analysis completed!")
