#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test the lexer
source = 'give @s minecraft:iron_ingot 1;'
tokens = lex_mdl_js(source)

print("Tokens:")
for token in tokens:
    print(f"  {token.type}: '{token.value}'")
