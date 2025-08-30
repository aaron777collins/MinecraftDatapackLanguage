#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

def test_file_vs_string():
    # Test 1: Parse from string
    test_string = '''function "hello" {
    say Counter: $counter$;
}'''
    
    print("=== Test 1: Parse from string ===")
    ast1 = parse_mdl_js(test_string)
    for func in ast1.get('functions', []):
        if func['name'] == 'hello':
            body = func.get('body', [])
            for stmt in body:
                if hasattr(stmt, 'command'):
                    print(f"String parsing: Command = '{stmt.command}'")
    
    # Test 2: Parse from file
    print("\n=== Test 2: Parse from file ===")
    with open('test_hello.mdl', 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    print(f"File content:\n{file_content}")
    
    ast2 = parse_mdl_js(file_content)
    for func in ast2.get('functions', []):
        if func['name'] == 'hello':
            body = func.get('body', [])
            for stmt in body:
                if hasattr(stmt, 'command') and 'Counter' in stmt.command:
                    print(f"File parsing: Command = '{stmt.command}'")

if __name__ == "__main__":
    test_file_vs_string()
