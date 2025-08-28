#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_lexer_js import MDLLexer
from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.cli import _ast_to_commands

# Test the list variable declaration
test_code = '''// test_simple_lists.mdl - Simple list test
pack "Simple List Test" description "Testing list functionality" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];

function "test" {
    say List test;
}'''

print("=== COMMANDS DEBUG ===")
try:
    lexer = MDLLexer(test_code)
    tokens = lexer.tokenize()
    
    parser = MDLParser(tokens)
    ast = parser.parse()
    
    print("AST functions:")
    for func in ast['functions']:
        print(f"  Function: {func.name}")
        print(f"    Body: {func.body}")
        
        # Generate commands for this function
        commands = _ast_to_commands(func.body)
        print(f"    Generated commands:")
        for i, cmd in enumerate(commands):
            print(f"      {i}: {cmd}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
