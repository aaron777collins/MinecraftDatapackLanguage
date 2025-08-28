#!/usr/bin/env python3
"""
Test that the MDL parser correctly stores loop commands.
This module can be imported and run as part of the test suite.
"""

from minecraft_datapack_language.mdl_parser import parse_mdl

def test_parser_stores_loop_commands():
    """Test that the parser correctly stores indented loop body commands"""
    # Test MDL content with loops
    mdl_content = '''
pack "Test" description "Test" pack_format 48

namespace "test"

function "simple_while":
    say Testing simple while loop
    scoreboard players set @s loop_counter 5
    while "score @s loop_counter matches 1..":
        say Counter: @s loop_counter
        scoreboard players remove @s loop_counter 1
        say Decremented counter

function "simple_for":
    tag @e[type=minecraft:player] add players
    for player in @e[tag=players]:
        say Processing player: @s
        effect give @s minecraft:speed 10 1
'''
    
    # Parse the MDL
    pack = parse_mdl(mdl_content)
    
    print("Testing MDL parser with loop commands...")
    
    # Check the function commands
    for ns_name, ns in pack.namespaces.items():
        for func_name, func in ns.functions.items():
            print(f"Function: {ns_name}:{func_name}")
            print("Commands:")
            for i, cmd in enumerate(func.commands):
                print(f"  {i}: '{cmd}'")
            print()
    
    # Verify that loop commands are stored correctly
    simple_while_commands = pack.namespaces['test'].functions['simple_while'].commands
    simple_for_commands = pack.namespaces['test'].functions['simple_for'].commands
    
    # Check that while loop body is stored
    has_while_body = any('say Counter:' in cmd for cmd in simple_while_commands)
    has_while_decrement = any('scoreboard players remove' in cmd for cmd in simple_while_commands)
    
    # Check that for loop body is stored
    has_for_body = any('say Processing player:' in cmd for cmd in simple_for_commands)
    has_for_effect = any('effect give @s minecraft:speed' in cmd for cmd in simple_for_commands)
    
    return has_while_body and has_while_decrement and has_for_body and has_for_effect

if __name__ == "__main__":
    print("[TEST] Testing MDL Parser with Loop Commands")
    print("=" * 50)
    
    success = test_parser_stores_loop_commands()
    
    if success:
        print("\n[+] Parser correctly stores loop commands!")
    else:
        print("\n[-] Parser has issues with loop commands!")
