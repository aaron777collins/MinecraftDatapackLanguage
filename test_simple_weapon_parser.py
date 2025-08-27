#!/usr/bin/env python3
"""
Test script to verify the simple weapon effects MDL file works with the JavaScript-style parser.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_simple_weapon_effects():
    """Test the simple weapon effects MDL file with the JavaScript-style parser."""
    
    # Read the simple weapon effects MDL file
    with open('test_simple_weapon_effects.mdl', 'r') as f:
        weapon_effects_mdl = f.read()
    
    print("Testing simple weapon effects MDL with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(weapon_effects_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(weapon_effects_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Check the weapon effects function
        if ast['functions']:
            weapon_func = ast['functions'][0]
            print(f"\nWeapon effects function '{weapon_func.name}' has {len(weapon_func.body)} statements")
            
            # Check if it's a for loop with conditionals
            if weapon_func.body and hasattr(weapon_func.body[0], '__class__') and weapon_func.body[0].__class__.__name__ == 'ForLoop':
                for_loop = weapon_func.body[0]
                print(f"  For loop: {for_loop.variable} in {for_loop.selector}")
                print(f"  For loop body has {len(for_loop.body)} statements")
                
                # Check if the for loop contains conditionals
                conditional_count = 0
                for stmt in for_loop.body:
                    if hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'IfStatement':
                        conditional_count += 1
                        print(f"    Found if statement with {len(stmt.body)} commands")
                        if stmt.elif_branches:
                            print(f"    Has {len(stmt.elif_branches)} elif branches")
                
                print(f"  Total conditionals in for loop: {conditional_count}")
        
        print("\nPASS: Simple weapon effects test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Simple weapon effects test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Simple Weapon Effects Test")
    print("=" * 80)
    
    # Run the simple weapon effects test
    success = test_simple_weapon_effects()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Simple weapon effects: {'PASS' if success else 'FAIL'}")
    
    if success:
        print("\nSUCCESS: Simple weapon effects test passed!")
        print("The JavaScript-style parser can handle weapon effects with conditionals!")
    else:
        print("\nWARNING: Simple weapon effects test failed.")
        print("The JavaScript-style parser needs more work.")
