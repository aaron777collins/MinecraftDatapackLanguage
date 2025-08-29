#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def debug_tokens(tokens):
    print("=== TOKENS DEBUG ===")
    for i, token in enumerate(tokens):
        print(f"  {i:2d}: {token.type:15s} = '{token.value}'")

if __name__ == "__main__":
    # Test with a simple variable assignment
    source = '''player_count = 0;'''
    
    print("=== SOURCE ===")
    print(source)
    print()
    
    tokens = lex_mdl_js(source)
    debug_tokens(tokens)
