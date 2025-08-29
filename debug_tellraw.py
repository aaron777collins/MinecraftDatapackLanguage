#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test the tellraw command parsing
source = '''
pack "test" "Test" 82;
namespace "test";

function "main" {
    tellraw @s [{"text":"Score: "},{"score":{"name":"@s","objective":"player_score"}}];
}
'''

# First, let's see the tokens
tokens = lex_mdl_js(source)
print("Tokens:")
for token in tokens:
    if token.type not in ['NEWLINE', 'EOF']:
        print(f"  {token.type}: '{token.value}'")

print("\nParsed AST:")
ast = parse_mdl_js(source)

# Print the raw command
for function in ast.get('functions', []):
    # Handle both dict and object formats
    if isinstance(function, dict):
        function_name = function['name']
        body = function.get('body', [])
    else:
        function_name = getattr(function, 'name', 'unknown')
        body = getattr(function, 'body', [])
    
    print(f"Function: {function_name}")
    for statement in body:
        if hasattr(statement, 'command'):
            print(f"Raw command: '{statement.command}'")
        elif isinstance(statement, dict) and 'command' in statement:
            print(f"Raw command: '{statement['command']}'")
        else:
            print(f"Statement type: {type(statement)}")
