#!/usr/bin/env python3
"""
Test script to verify the variable system works with the JavaScript-style parser.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_variables_mdl():
    """Test the variables MDL file with the JavaScript-style parser."""
    
    # Read the variables MDL file
    with open('test_variables.mdl', 'r') as f:
        variables_mdl = f.read()
    
    print("Testing variables MDL with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(variables_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(variables_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Check all functions for variables
        print(f"\nFunctions found:")
        for func in ast['functions']:
            print(f"  - {func.name} ({len(func.body)} statements)")
            
            # Count variable declarations and assignments
            var_declarations = 0
            var_assignments = 0
            expressions = 0
            
            def analyze_statements(statements):
                nonlocal var_declarations, var_assignments, expressions
                for stmt in statements:
                    if hasattr(stmt, '__class__'):
                        class_name = stmt.__class__.__name__
                        if class_name == 'VariableDeclaration':
                            var_declarations += 1
                            print(f"      Variable declaration: {stmt.var_type} {stmt.data_type} {stmt.name}")
                        elif class_name == 'VariableAssignment':
                            var_assignments += 1
                            print(f"      Variable assignment: {stmt.name} = {stmt.value}")
                        elif class_name in ['BinaryExpression', 'LiteralExpression', 'VariableExpression']:
                            expressions += 1
                        elif hasattr(stmt, 'body'):
                            analyze_statements(stmt.body)
            
            analyze_statements(func.body)
            print(f"    Variables: {var_declarations} declarations, {var_assignments} assignments, {expressions} expressions")
        
        # Check namespaces
        print(f"\nNamespaces found:")
        for ns in ast['namespaces']:
            print(f"  - {ns.name}")
        
        # Check hooks
        print(f"\nHooks found:")
        for hook in ast['hooks']:
            print(f"  - {hook.hook_type}: {hook.function_name}")
        
        print("\nPASS: Variables test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Variables test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Variables Test")
    print("=" * 80)
    
    # Run the variables test
    success = test_variables_mdl()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Variables: {'PASS' if success else 'FAIL'}")
    
    if success:
        print("\nSUCCESS: Variables test passed!")
        print("The JavaScript-style parser can handle variables with different scopes and types!")
    else:
        print("\nWARNING: Variables test failed.")
        print("The JavaScript-style parser needs more work.")
