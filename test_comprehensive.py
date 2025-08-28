#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack

# Test with a comprehensive MDL file that covers all features
test_source = '''pack "Comprehensive Test" description "Testing all MDL features" pack_format 82;

namespace "test";

// Test basic commands
function "basic" {
    say Hello World;
    tellraw @a {"text":"Basic test","color":"green"};
}

// Test variables
function "variables" {
    var num counter = 0;
    var str message = "Hello";
    var list items = ["sword", "shield"];
    
    counter = counter + 5;
    message = "Updated message";
}

// Test control flow
function "control_flow" {
    var num value = 10;
    
    if "score @s value matches 10" {
        say Value is 10;
    } else if "score @s value matches 5" {
        say Value is 5;
    } else {
        say Value is something else;
    }
}

// Test function calls
function "calls" {
    function test:basic;
    function test:variables;
}

// Test loops
function "loops" {
    for player in @a {
        say Processing player;
        effect give @s minecraft:speed 1 0;
    }
}

// Test complex expressions
function "expressions" {
    var num a = 5;
    var num b = 3;
    var num result = a + b;
    var str combined = "Hello" + " World";
}'''

print("Testing comprehensive MDL to Minecraft conversion:")
print("=" * 60)

# Parse the MDL
ast = parse_mdl_js(test_source)

# Convert to Pack
pack = _ast_to_pack(ast, 82)

# Check the commands in the Function objects
print("\nChecking all functions:")
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
