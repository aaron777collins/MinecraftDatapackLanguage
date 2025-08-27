#!/usr/bin/env python3
"""
Test script for minimal try-catch file.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_minimal_try_catch():
    """Test the minimal try-catch MDL file."""
    
    # Read the minimal try-catch MDL file
    with open('test_minimal_try_catch.mdl', 'r') as f:
        minimal_mdl = f.read()
    
    print("Testing minimal try-catch MDL file...")
    print("=" * 50)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(minimal_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Show tokens around try-catch
        print("\nTokens around try-catch:")
        for i, token in enumerate(tokens):
            if token.type == 'TRY':
                print(f"Found TRY at token {i}")
                for j in range(max(0, i-5), min(len(tokens), i+15)):
                    print(f"{j:3d}: {tokens[j].type} = '{tokens[j].value}'")
                break
        
        # Test parser
        ast = parse_mdl_js(minimal_mdl)
        
        print(f"\nParser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        
        print("\nPASS: Minimal try-catch test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Minimal try-catch test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL Minimal Try-Catch Test")
    print("=" * 50)
    
    # Run the minimal try-catch test
    success = test_minimal_try_catch()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"Minimal Try-Catch: {'PASS' if success else 'FAIL'}")
