#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the scope syntax
source = """
var num global_timer scope<global> = 0;
"""

tokens = lex_mdl_js(source)
print("Tokens:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type} = '{token.value}'")

print("\nTrying to parse:")
try:
    ast = parse_mdl_js(source)
    print("Parsing successful!")
    print("AST:", ast)
except Exception as e:
    print(f"Parsing failed: {e}")
    import traceback
    traceback.print_exc()
