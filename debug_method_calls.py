#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from mdl_lexer_js import MDLLexer

def test_method_calls():
    """Test method call tokenization"""
    
    test_lines = [
        'items.append("ruby")',
        'numbers.append(4)',
        'items.remove("shield")',
        'numbers.remove(2)'
    ]
    
    for line in test_lines:
        print(f"\nTesting line: {line}")
        lexer = MDLLexer(line)
        lexer.tokenize()
        
        print("Tokens:")
        for token in lexer.tokens:
            print(f"  {token.type}: '{token.value}'")
        
        print("Tokens:")
        for token in lexer.tokens:
            print(f"  {token.type}: '{token.value}'")

if __name__ == "__main__":
    test_method_calls()
