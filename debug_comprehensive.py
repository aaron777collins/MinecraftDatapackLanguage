#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Read the comprehensive test file
with open('test_comprehensive.mdl', 'r') as f:
    code = f.read()

print("=== FILE CONTENT ===")
print(code)

print("\n=== LEXING ===")
tokens = lex_mdl_js(code)
for token in tokens[:30]:  # First 30 tokens
    print(f"{token.type.name}: {token.value}")

print("\n=== PARSING ===")
parser = MDLParser(tokens)
ast = parser.parse()

print("AST:")
print(f"Pack: {ast.get('pack')}")
print(f"Namespaces: {ast.get('namespaces', [])}")
print(f"Functions: {len(ast.get('functions', []))}")

for func in ast.get('functions', []):
    print(f"\nFunction: {func.name}")
    print(f"Body: {len(func.body)} statements")
    for i, stmt in enumerate(func.body):
        print(f"  [{i}] {stmt.__class__.__name__}: {stmt}")
