#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_lexer_js import MDLLexer, TokenType
from minecraft_datapack_language.mdl_parser_js import MDLParser

# Test the list variable declaration
test_code = '''// test_simple_lists.mdl - Simple list test
pack "Simple List Test" description "Testing list functionality" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];

function "test" {
    say List test;
}'''

print("=== PARSER DEBUG ===")
try:
    lexer = MDLLexer(test_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"{i:2d}: {token.type:15} | '{token.value}'")
    
    print("\n=== PARSING ===")
    parser = MDLParser(tokens)
    ast = parser.parse()
    
    print("AST:")
    for key, value in ast.items():
        print(f"  {key}: {value}")
        if isinstance(value, list):
            for i, item in enumerate(value):
                print(f"    [{i}] {type(item).__name__}: {item}")
                if hasattr(item, 'body'):
                    print(f"      Body: {item.body}")
                if hasattr(item, 'variables'):
                    print(f"      Variables: {item.variables}")
                if hasattr(item, 'data_type'):
                    print(f"      Data type: {item.data_type}")
                if hasattr(item, 'name'):
                    print(f"      Name: {item.name}")
                if hasattr(item, 'value'):
                    print(f"      Value: {item.value}")
                    if hasattr(item.value, 'elements'):
                        print(f"      Elements: {item.value.elements}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
