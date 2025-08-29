#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js, MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Read the conditionals file
with open('test_examples/conditionals.mdl', 'r') as f:
    source = f.read()

print("Parsing conditionals.mdl step by step:")
print("=" * 50)

# First, let's see the tokens
tokens = lex_mdl_js(source)
print(f"Total tokens: {len(tokens)}")

# Find the if statement tokens
if_positions = []
for i, token in enumerate(tokens):
    if token.type == 'IF':
        if_positions.append(i)

print(f"IF tokens found at positions: {if_positions}")

# Let's look at the tokens around the first if statement
if if_positions:
    pos = if_positions[0]
    print(f"\nTokens around first IF (position {pos}):")
    start = max(0, pos - 2)
    end = min(len(tokens), pos + 8)
    for i in range(start, end):
        marker = ">>> " if i == pos else "    "
        print(f"{marker}{i}: {tokens[i].type} = '{tokens[i].value}'")

# Now let's try to parse step by step
print(f"\nTrying to parse...")
try:
    result = parse_mdl_js(source)
    print("✅ Parsing successful!")
except Exception as e:
    print(f"❌ Parsing failed: {e}")
    import traceback
    traceback.print_exc()
