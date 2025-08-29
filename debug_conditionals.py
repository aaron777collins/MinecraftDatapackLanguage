#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js, TokenType

# Read the conditionals file
with open('test_examples/conditionals.mdl', 'r') as f:
    source = f.read()

print("Lexing conditionals.mdl:")
print("=" * 50)
tokens = lex_mdl_js(source)

# Find the problematic area around the if statement
for i, token in enumerate(tokens):
    if token.type == TokenType.IF:
        print(f"\nFound IF at position {i}:")
        # Show tokens around this position
        start = max(0, i - 5)
        end = min(len(tokens), i + 10)
        for j in range(start, end):
            marker = ">>> " if j == i else "    "
            print(f"{marker}{j}: {tokens[j].type} = '{tokens[j].value}'")
        break
