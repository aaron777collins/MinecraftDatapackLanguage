#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_lexer_js import MDLLexer, TokenType
from minecraft_datapack_language.mdl_parser_js import MDLParser

# Test the list operations
test_code = '''// test_list_operations.mdl - Test list append and remove operations
pack "List Operations Test" description "Testing list append and remove" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];
var list numbers = [1, 2, 3];

function "test_operations" {
    // Test append operations
    items.append("ruby");
    items.append("diamond");
    numbers.append(4);
    numbers.append(5);
    
    // Test remove operations (will show TODO comments for now)
    items.remove("shield");
    numbers.remove(2);
    
    // Test mixed operations
    items.append("emerald");
    numbers.append(6);
}

function "test" {
    say List operations test;
}'''

print("=== LIST OPERATIONS DEBUG ===")
try:
    lexer = MDLLexer(test_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"{i:2d}: {token.type:15} | '{token.value}'")
        if token.type == TokenType.IDENTIFIER and token.value == 'items':
            print(f"    -> Next few tokens:")
            for j in range(i+1, min(i+6, len(tokens))):
                print(f"       {j:2d}: {tokens[j].type:15} | '{tokens[j].value}'")
            print()
    
    print("\n=== PARSING ===")
    parser = MDLParser(tokens)
    ast = parser.parse()
    
    print("AST functions:")
    for func in ast['functions']:
        print(f"  Function: {func.name}")
        for item in func.body:
            print(f"    {type(item).__name__}: {item}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
