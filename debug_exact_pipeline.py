#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js, TokenType
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

def test_exact_structure():
    test_input = '''// hello.mdl
pack "My First Pack" "A simple example" 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    say Counter: $counter$;
}

on_load "example:hello";'''
    
    print("=== Exact Structure Test ===")
    print(f"Input: {test_input}")
    
    # Step 1: Parse the input
    print("\n1. Parser Output:")
    ast = parse_mdl_js(test_input)
    
    # Check the specific function
    for func in ast.get('functions', []):
        if func['name'] == 'hello':
            print(f"  Function: {func}")
            body = func.get('body', [])
            for i, stmt in enumerate(body):
                print(f"    Statement {i}: {stmt}")
                if hasattr(stmt, 'command'):
                    print(f"      Command: '{stmt.command}'")

if __name__ == "__main__":
    test_exact_structure()
