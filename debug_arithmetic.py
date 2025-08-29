#!/usr/bin/env python3
"""
Debug script to examine AST structure for arithmetic expressions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import MDLLexer

def debug_arithmetic():
    """Debug arithmetic expression parsing"""
    
    # Test the specific expression from the helper function
    source = '''
function "helper" {
    var num result = 0;
    result = 5 + 3;
    say "Calculation result: $result$";
}
'''
    
    print("=== LEXER OUTPUT ===")
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    for token in tokens:
        print(f"  {token}")
    
    print("\n=== PARSER OUTPUT ===")
    parser = MDLParser(tokens)
    ast = parser.parse()
    
    print("AST structure:")
    print(f"  Functions: {len(ast.get('functions', []))}")
    
    for i, func in enumerate(ast.get('functions', [])):
        print(f"  Function {i}: {func.get('name', 'unknown')}")
        print(f"    Body statements: {len(func.get('body', []))}")
        
        for j, stmt in enumerate(func.get('body', [])):
            print(f"    Statement {j}: {type(stmt)}")
            if hasattr(stmt, '__class__'):
                print(f"      Class: {stmt.__class__.__name__}")
                if hasattr(stmt, 'name'):
                    print(f"      Name: {stmt.name}")
                if hasattr(stmt, 'value'):
                    print(f"      Value: {stmt.value}")
                    if hasattr(stmt.value, '__class__'):
                        print(f"      Value class: {stmt.value.__class__.__name__}")
                        if hasattr(stmt.value, 'left'):
                            print(f"      Left: {stmt.value.left}")
                            if hasattr(stmt.value.left, '__class__'):
                                print(f"      Left class: {stmt.value.left.__class__.__name__}")
                        if hasattr(stmt.value, 'right'):
                            print(f"      Right: {stmt.value.right}")
                            if hasattr(stmt.value.right, '__class__'):
                                print(f"      Right class: {stmt.value.right.__class__.__name__}")
                        if hasattr(stmt.value, 'operator'):
                            print(f"      Operator: {stmt.value.operator}")

if __name__ == "__main__":
    debug_arithmetic()
