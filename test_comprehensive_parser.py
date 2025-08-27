#!/usr/bin/env python3
"""
Test script to verify the comprehensive MDL file works with the JavaScript-style parser.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_comprehensive_mdl():
    """Test the comprehensive MDL file with the JavaScript-style parser."""
    
    # Read the comprehensive MDL file
    with open('test_comprehensive_nested.mdl', 'r') as f:
        comprehensive_mdl = f.read()
    
    print("Testing comprehensive MDL with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(comprehensive_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(comprehensive_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Check all functions
        print(f"\nFunctions found:")
        for func in ast['functions']:
            print(f"  - {func.name} ({len(func.body)} statements)")
            
            # Count nested statements
            def count_nesting(statements, level=0):
                count = 0
                for stmt in statements:
                    if hasattr(stmt, '__class__'):
                        count += 1
                        if hasattr(stmt, 'body'):
                            count += count_nesting(stmt.body, level + 1)
                return count
            
            total_statements = count_nesting(func.body)
            print(f"    Total nested statements: {total_statements}")
        
        # Check namespaces
        print(f"\nNamespaces found:")
        for ns in ast['namespaces']:
            print(f"  - {ns.name}")
        
        # Check hooks
        print(f"\nHooks found:")
        for hook in ast['hooks']:
            print(f"  - {hook.hook_type}: {hook.function_name}")
        
        # Check tags
        print(f"\nTags found:")
        for tag in ast['tags']:
            print(f"  - {tag.tag_type} {tag.name} ({len(tag.values)} values)")
        
        print("\nPASS: Comprehensive MDL test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Comprehensive MDL test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Comprehensive Test")
    print("=" * 80)
    
    # Run the comprehensive test
    success = test_comprehensive_mdl()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Comprehensive MDL: {'PASS' if success else 'FAIL'}")
    
    if success:
        print("\nSUCCESS: Comprehensive MDL test passed!")
        print("The JavaScript-style parser can handle complex nested structures!")
    else:
        print("\nWARNING: Comprehensive MDL test failed.")
        print("The JavaScript-style parser needs more work.")
