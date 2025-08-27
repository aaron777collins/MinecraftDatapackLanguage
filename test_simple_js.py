#!/usr/bin/env python3
"""
Simple test to debug the JavaScript-style parser.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_simple():
    """Test a simple MDL with JavaScript-style syntax."""
    
    simple_mdl = '''pack "test" description "Simple test" pack_format 48;

namespace "test";

function "simple" {
    say Hello world;
}

on_tick "test:simple";
'''
    
    print("Testing simple MDL with JavaScript-style parser...")
    print("=" * 80)
    print("Input MDL:")
    print(simple_mdl)
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(simple_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Show first 20 tokens
        for i, token in enumerate(tokens[:20]):
            print(f"  {i+1:2d}: {token.type:15s} = '{token.value}' (line {token.line})")
        
        # Test parser
        ast = parse_mdl_js(simple_mdl)
        
        print(f"\nParser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        
        print("\nPASS: Simple test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Simple test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_for_loop():
    """Test a simple for loop."""
    
    for_mdl = '''pack "test" description "For loop test" pack_format 48;

namespace "test";

function "for_test" {
    for player in @a {
        say Hello @s;
    }
}

on_tick "test:for_test";
'''
    
    print("\nTesting for loop with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        ast = parse_mdl_js(for_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Functions: {len(ast['functions'])}")
        
        if ast['functions']:
            func = ast['functions'][0]
            print(f"  Function '{func.name}' has {len(func.body)} statements")
            if func.body:
                print(f"  First statement: {func.body[0].__class__.__name__}")
        
        print("\nPASS: For loop test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: For loop test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Simple Test Suite")
    print("=" * 80)
    
    # Run tests
    test1 = test_simple()
    test2 = test_for_loop()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Simple: {'PASS' if test1 else 'FAIL'}")
    print(f"For loop: {'PASS' if test2 else 'FAIL'}")
    
    if all([test1, test2]):
        print("\nSUCCESS: All simple tests passed!")
    else:
        print("\nWARNING: Some simple tests failed.")
