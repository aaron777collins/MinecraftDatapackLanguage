#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack

# Test with a simple MDL file
test_source = '''pack "Simple Test" description "Simple test" pack_format 82;

namespace "test";

function "hello" {
    say Hello World;
    tellraw @a {"text":"Test","color":"green"};
}'''

print("Testing simple MDL to Minecraft conversion:")
print("=" * 50)

# Parse the MDL
ast = parse_mdl_js(test_source)

# Convert to Pack
pack = _ast_to_pack(ast, 82)

# Check the commands in the Function objects
print("\nChecking function:")
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

print("\nTest completed!")
