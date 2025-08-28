#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands

# Test with the actual broken test file
with open('test_broken/mypack.mdl', 'r') as f:
    test_source = f.read()

print("Testing _ast_to_commands function:")
print("=" * 60)

# Parse the MDL
ast = parse_mdl_js(test_source)

# Find the variable_demo function
for namespace in ast.get('namespaces', []):
    for func in ast.get('functions', []):
        if hasattr(func, 'name') and func.name == 'variable_demo':
            print(f"\nFound variable_demo function:")
            print(f"Function body has {len(func.body)} nodes")
            
            # Test _ast_to_commands directly
            commands = _ast_to_commands(func.body)
            print(f"\nGenerated commands ({len(commands)}):")
            for i, cmd in enumerate(commands):
                print(f"  {i}: '{cmd}'")
            
            break

print("\nCommand generation test completed!")
