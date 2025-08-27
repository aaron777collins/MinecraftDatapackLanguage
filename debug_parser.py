#!/usr/bin/env python3
"""
Debug script to see what's happening with the loop body collection.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser import parse_mdl

def debug_for_loop_parsing():
    """Debug the for loop parsing to see what's happening."""
    
    # Simple test case
    test_mdl = '''pack "test" description "Debug test" pack_format 48

namespace "test"

function "debug_for":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            say Player found: @s
        else:
            say Non-player: @s

on_tick "test:debug_for"
'''
    
    print("Debugging for loop parsing...")
    print("=" * 50)
    print("Input MDL:")
    print(test_mdl)
    print("=" * 50)
    
    try:
        pack = parse_mdl(test_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            for func_name, func in test_ns.functions.items():
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    ⚠️  EMPTY!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_for_loop_parsing()
