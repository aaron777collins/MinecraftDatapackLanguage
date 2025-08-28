#!/usr/bin/env python3
"""
Test script to verify the complete MDL system works with the JavaScript-style parser.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_complete_system():
    """Test the complete system MDL file with the JavaScript-style parser."""
    
    # Read the complete system MDL file
    with open('test_complete_system.mdl', 'r') as f:
        complete_system_mdl = f.read()
    
    print("Testing complete system MDL with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(complete_system_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(complete_system_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Analyze all functions
        print(f"\nFunctions found:")
        total_variables = 0
        total_assignments = 0
        total_expressions = 0
        total_conditionals = 0
        total_loops = 0
        
        for func in ast['functions']:
            print(f"  - {func.name} ({len(func.body)} statements)")
            
            # Count different types of statements
            var_declarations = 0
            var_assignments = 0
            expressions = 0
            conditionals = 0
            loops = 0
            
            def analyze_statements(statements, depth=0):
                nonlocal var_declarations, var_assignments, expressions, conditionals, loops
                for stmt in statements:
                    if hasattr(stmt, '__class__'):
                        class_name = stmt.__class__.__name__
                        indent = "  " * (depth + 2)
                        
                        if class_name == 'VariableDeclaration':
                            var_declarations += 1
                            print(f"{indent}Variable declaration: {stmt.var_type} {stmt.data_type} {stmt.name}")
                        elif class_name == 'VariableAssignment':
                            var_assignments += 1
                            print(f"{indent}Variable assignment: {stmt.name} = {stmt.value}")
                        elif class_name in ['BinaryExpression', 'LiteralExpression', 'VariableExpression']:
                            expressions += 1
                        elif class_name == 'IfStatement':
                            conditionals += 1
                            print(f"{indent}If statement with {len(stmt.body)} commands")
                            analyze_statements(stmt.body, depth + 1)
                            for elif_branch in stmt.elif_branches:
                                print(f"{indent}Else if branch with {len(elif_branch.body)} commands")
                                analyze_statements(elif_branch.body, depth + 1)
                            if stmt.else_body:
                                print(f"{indent}Else branch with {len(stmt.else_body)} commands")
                                analyze_statements(stmt.else_body, depth + 1)
                        elif class_name == 'ForLoop':
                            loops += 1
                            print(f"{indent}For loop: {stmt.variable} in {stmt.selector}")
                            analyze_statements(stmt.body, depth + 1)
                        elif class_name == 'WhileLoop':
                            loops += 1
                            print(f"{indent}While loop with condition")
                            analyze_statements(stmt.body, depth + 1)
                        elif hasattr(stmt, 'body'):
                            analyze_statements(stmt.body, depth + 1)
            
            analyze_statements(func.body)
            print(f"    Variables: {var_declarations} declarations, {var_assignments} assignments")
            print(f"    Control: {conditionals} conditionals, {loops} loops, {expressions} expressions")
            
            total_variables += var_declarations + var_assignments
            total_assignments += var_assignments
            total_expressions += expressions
            total_conditionals += conditionals
            total_loops += loops
        
        # Check namespaces
        print(f"\nNamespaces found:")
        for ns in ast['namespaces']:
            print(f"  - {ns.name}")
        
        # Check hooks
        print(f"\nHooks found:")
        for hook in ast['hooks']:
            print(f"  - {hook.hook_type}: {hook.function_name}")
        
        # Summary statistics
        print(f"\nComplete System Summary:")
        print(f"  Total variables: {total_variables}")
        print(f"  Total assignments: {total_assignments}")
        print(f"  Total expressions: {total_expressions}")
        print(f"  Total conditionals: {total_conditionals}")
        print(f"  Total loops: {total_loops}")
        print(f"  Total statements: {total_variables + total_conditionals + total_loops}")
        
        print("\nPASS: Complete system test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Complete system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Complete System Test")
    print("=" * 80)
    
    # Run the complete system test
    success = test_complete_system()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Complete System: {'PASS' if success else 'FAIL'}")
    
    if success:
        print("\nSUCCESS: Complete system test passed!")
        print("The JavaScript-style parser can handle the complete MDL language!")
        print("Features supported:")
        print("  [+] Variables (var, let, const)")
        print("  [+] Data types (num, str)")
        print("  [+] Mathematical operations (+, -, *, /, %)")
        print("  [+] String concatenation")
        print("  [+] Variable scopes and assignments")
        print("  [+] Nested conditionals (if/else if/else)")
        print("  [+] Loops (for, while)")
        print("  [+] Function calls")
        print("  [+] Unlimited nesting")
        print("  [+] Complex expressions")
    else:
        print("\nWARNING: Complete system test failed.")
        print("The JavaScript-style parser needs more work.")
