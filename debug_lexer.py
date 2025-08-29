#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js, TokenType

# Test the problematic condition
source = 'if "$player_level$ >= 20" {'
tokens = lex_mdl_js(source)

print("Tokens for condition:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type} = '{token.value}'")
