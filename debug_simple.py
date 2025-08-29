#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

if __name__ == "__main__":
    # Test with a simple variable assignment
    source = '''function "test" {
        result = 5 + 3;
    }'''
    
    print("=== SOURCE ===")
    print(source)
    print()
    
    tokens = lex_mdl_js(source)
    print("=== TOKENS ===")
    for i, token in enumerate(tokens):
        print(f"  {i:2d}: {token.type:15s} = '{token.value}'")
    print()
    
    ast = parse_mdl_js(source)
    print("=== AST ===")
    if 'functions' in ast:
        for func in ast['functions']:
            print(f"Function: {func.get('name', 'unknown')}")
            for i, stmt in enumerate(func.get('body', [])):
                print(f"  Statement {i}: {type(stmt)} = {stmt}")
                if hasattr(stmt, '__class__'):
                    print(f"    Class: {stmt.__class__.__name__}")
                if hasattr(stmt, 'name'):
                    print(f"    Name: {stmt.name}")
                if hasattr(stmt, 'value'):
                    print(f"    Value: {stmt.value}")
