#!/usr/bin/env python3
"""
Debug script to see what tokens the lexer is generating.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test with variable assignment lines
test_lines = [
    "local_counter = local_counter + 5",
    "player_name = \"Alex\"",
    "global_message = \"Updated: \" + player_name"
]

print("Testing token generation for variable assignments:")
print("=" * 60)

for line in test_lines:
    print(f"\nLine: {line}")
    tokens = lex_mdl_js(line)
    print("Tokens:")
    for token in tokens:
        print(f"  {token.type}: '{token.value}'")
    print()

print("Token analysis completed!")
