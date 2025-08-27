#!/usr/bin/env python3
"""
Debug script to see all tokens from the simple complete file.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Read the simple complete language MDL file
with open('test_simple_complete.mdl', 'r') as f:
    simple_complete_mdl = f.read()

print("Testing simple complete MDL file tokenization:")
print("=" * 50)

tokens = lex_mdl_js(simple_complete_mdl)

print("All tokens generated:")
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type} = '{token.value}' (line {token.line})")
    
    # Stop after we see the try-catch section
    if token.type == 'TRY':
        print("Found TRY token, showing next 20 tokens:")
        for j in range(i+1, min(i+21, len(tokens))):
            print(f"{j:3d}: {tokens[j].type} = '{tokens[j].value}' (line {tokens[j].line})")
        break
