#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack

# Test with the actual broken test file
with open('test_broken/mypack.mdl', 'r') as f:
    test_source = f.read()

print("Testing with actual broken test file:")
print("=" * 60)

# Parse the MDL
ast = parse_mdl_js(test_source)

# Convert to Pack
pack = _ast_to_pack(ast, 82)

# Check the commands in the Function objects
print("\nChecking Function objects:")
for ns_name, ns in pack.namespaces.items():
    print(f"Namespace: {ns_name}")
    for func_name, func in ns.functions.items():
        print(f"  Function {func_name}:")
        for cmd in func.commands:
            print(f"    '{cmd}'")
            if cmd.endswith(';'):
                print(f"    ERROR: Command has semicolon!")
            else:
                print(f"    OK: No semicolon")

# Now let's simulate the build process
print("\nSimulating build process:")
for ns_name, ns in pack.namespaces.items():
    print(f"Namespace: {ns_name}")
    for func_name, func in ns.functions.items():
        print(f"  Function {func_name}:")
        print(f"    Commands before processing: {len(func.commands)}")
        
        # Check if commands have semicolons (this is what the build method does)
        has_semicolons = any(cmd.endswith(';') for cmd in func.commands)
        print(f"    Has semicolons: {has_semicolons}")
        
        if has_semicolons:
            print(f"    Would use old processing pipeline")
        else:
            print(f"    Would use new processing pipeline (commands as-is)")
            print(f"    Final commands:")
            for cmd in func.commands:
                print(f"      '{cmd}'")

print("\nTest completed!")
