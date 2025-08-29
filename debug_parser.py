#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def debug_tokens(tokens):
    print("=== TOKENS DEBUG ===")
    for i, token in enumerate(tokens):
        print(f"  {i:2d}: {token.type:15s} = '{token.value}'")

def debug_ast(ast):
    print("=== AST DEBUG ===")
    print(f"Type: {type(ast)}")
    if isinstance(ast, dict):
        print(f"Keys: {list(ast.keys())}")
        if 'functions' in ast:
            print(f"Functions count: {len(ast['functions'])}")
            for i, func in enumerate(ast['functions']):
                print(f"  Function {i}: {type(func)}")
                if isinstance(func, dict):
                    print(f"    Name: {func.get('name', 'unknown')}")
                    print(f"    Body: {func.get('body', [])}")
                    for j, stmt in enumerate(func.get('body', [])):
                        print(f"      Statement {j}: {type(stmt)} = {stmt}")
                else:
                    if hasattr(func, 'name'):
                        print(f"    Name: {func.name}")
                    if hasattr(func, 'body'):
                        print(f"    Body: {func.body}")
                        for j, stmt in enumerate(func.body):
                            print(f"      Statement {j}: {type(stmt)} = {stmt}")
    else:
        print(f"Value: {ast}")

if __name__ == "__main__":
    # Test with a function containing variable assignments
    source = '''function "test" {
        player_count = 0;
        game_timer = 100;
    }'''
    
    print("=== SOURCE ===")
    print(source)
    print()
    
    tokens = lex_mdl_js(source)
    debug_tokens(tokens)
    print()
    
    ast = parse_mdl_js(source)
    debug_ast(ast)
