#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test the problematic line
test_code = 'function "test1:hello";'

print("Testing lexer with:", test_code)
tokens = lex_mdl_js(test_code)

for i, token in enumerate(tokens):
    print(f"Token {i}: {token.type} = '{token.value}'")
