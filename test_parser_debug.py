#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from mdl_lexer_js import MDLLexer
from mdl_parser_js import MDLParserJS

def test_parser():
    """Test parser with method calls"""
    
    test_code = '''
function "test" {
    items.append("ruby");
}
'''
    
    print("Testing parser with method calls...")
    
    # Lex
    lexer = MDLLexer(test_code)
    lexer.tokenize()
    
    print("Tokens:")
    for token in lexer.tokens:
        if token.type.name not in ['NEWLINE', 'EOF']:
            print(f"  {token.type}: '{token.value}'")
    
    # Parse
    parser = MDLParserJS(lexer.tokens)
    ast = parser.parse()
    
    print("\nAST:")
    print(f"Functions: {len(ast.get('functions', []))}")
    
    for func in ast.get('functions', []):
        print(f"\nFunction: {func.name}")
        print(f"Body nodes: {len(func.body)}")
        
        for i, node in enumerate(func.body):
            print(f"  Node {i}: {type(node).__name__}")
            if hasattr(node, 'list_name'):
                print(f"    List: {node.list_name}")
            if hasattr(node, 'value'):
                print(f"    Value: {node.value}")

if __name__ == "__main__":
    test_parser()
