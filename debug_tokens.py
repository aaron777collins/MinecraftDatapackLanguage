#!/usr/bin/env python3
"""
Debug script to see what tokens the lexer is generating.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer import lex_mdl

def debug_tokens():
    """Debug the token generation."""
    
    test_mdl = '''pack "test" description "Deepest nesting test" pack_format 48

namespace "test"

function "deepest_nesting":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            for item in @s:
                while "entity @s[type=minecraft:item]":
                    if "entity @s[nbt={Item:{id:'minecraft:diamond'}}]":
                        say Found diamond: @s
                        effect give @s minecraft:glowing 5 0
                    else:
                        say Not a diamond: @s
                        for entity in @e[type=minecraft:item]:
                            say Processing entity: @s
                            particle minecraft:firework ~ ~ ~ 0.1 0.1 0.1 0.01 1

on_tick "test:deepest_nesting"
'''
    
    print("Debugging token generation...")
    print("=" * 80)
    print("Input MDL:")
    print(test_mdl)
    print("=" * 80)
    
    try:
        tokens = lex_mdl(test_mdl)
        print(f"Generated {len(tokens)} tokens:")
        
        for i, token in enumerate(tokens[:25]):  # Show first 25 tokens
            print(f"  {i+1:2d}: {token.type:15s} = '{token.value}' (line {token.line})")
        
        print("...")
        
        # Show tokens around function declaration
        print("\nTokens around function declaration:")
        for i, token in enumerate(tokens):
            if i >= 10 and i <= 15:  # Around line 5
                print(f"  {i+1:2d}: {token.type:15s} = '{token.value}' (line {token.line})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_tokens()
