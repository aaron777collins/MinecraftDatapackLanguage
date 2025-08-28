#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from mdl_lexer_js import MDLLexer, TokenType

# Test the list variable declaration
test_code = '''// test_simple_lists.mdl - Simple list test
pack "Simple List Test" description "Testing list functionality" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];

function "test" {
    say List test;
}'''

print("=== LEXER TOKENS ===")
try:
    lexer = MDLLexer(test_code)
    tokens = lexer.tokenize()
    
    for i, token in enumerate(tokens):
        print(f"{i:2d}: {token.type:15} | '{token.value}' | line {token.line}")
        if token.type == TokenType.VAR:
            print(f"    -> Next few tokens:")
            for j in range(i+1, min(i+6, len(tokens))):
                print(f"       {j:2d}: {tokens[j].type:15} | '{tokens[j].value}'")
            print()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
