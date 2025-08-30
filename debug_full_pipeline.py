#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js, TokenType
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

def test_full_pipeline():
    test_input = '''function "test" {
    say Counter: $counter$;
}'''
    
    print("=== Full Pipeline Test ===")
    print(f"Input: {test_input}")
    
    # Step 1: Lexer
    print("\n1. Lexer Output:")
    tokens = lex_mdl_js(test_input)
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type} = '{token.value}'")
    
    # Step 2: Parser
    print("\n2. Parser Output:")
    ast = parse_mdl_js(test_input)
    for func in ast.get('functions', []):
        print(f"  Function: {func}")
        if hasattr(func, 'body'):
            for stmt in func.body:
                print(f"    Statement: {stmt}")
                if hasattr(stmt, 'command'):
                    print(f"      Command: '{stmt.command}'")

if __name__ == "__main__":
    test_full_pipeline()
