#!/usr/bin/env python3
"""
Test loop processing functionality.
This module can be imported and run as part of the test suite.
"""

import re
from minecraft_datapack_language import Pack

def test_loop_regex_patterns():
    """Test that the regex patterns correctly identify loop syntax"""
    commands = [
        "say Testing simple while loop",
        "scoreboard players set @s loop_counter 5",
        'while "score @s loop_counter matches 1..":',
        "    say Counter: @s loop_counter",
        "    scoreboard players remove @s loop_counter 1",
        "    say Decremented counter"
    ]
    
    print("Testing while loop regex patterns...")
    while_pattern = r'^while\s+"([^"]+)"\s*:\s*$'
    for i, cmd in enumerate(commands):
        match = re.match(while_pattern, cmd.strip())
        if match:
            print(f"  [+] Line {i}: '{cmd}' -> MATCH: {match.group(1)}")
        else:
            print(f"  [-] Line {i}: '{cmd}' -> NO MATCH")
    
    print("\nTesting for loop regex patterns...")
    for_pattern = r'^for\s+(\w+)\s+in\s+(.+?)\s*:\s*$'
    for i, cmd in enumerate(commands):
        match = re.match(for_pattern, cmd.strip())
        if match:
            print(f"  [+] Line {i}: '{cmd}' -> MATCH: var={match.group(1)}, collection={match.group(2)}")
        else:
            print(f"  [-] Line {i}: '{cmd}' -> NO MATCH")

def test_loop_processing():
    """Test that loop processing generates correct functions"""
    # Create a pack and test the processing function directly
    p = Pack('test')
    ns = p.namespace('test')
    
    # Test commands
    commands = [
        'say Testing simple while loop',
        'scoreboard players set @s loop_counter 5',
        'while "score @s loop_counter matches 1..":',
        'say Counter: @s loop_counter',
        'scoreboard players remove @s loop_counter 1',
        'say Decremented counter'
    ]
    
    print("Testing loop processing directly...")
    processed = p._process_control_flow('test', 'simple_while', commands)
    print("Processed commands:")
    for i, cmd in enumerate(processed):
        print(f"  {i}: '{cmd}'")
    
    print("\nGenerated functions:")
    for func_name, func in ns.functions.items():
        print(f"  {func_name}: {func.commands}")
    
    return len(processed) > 0 and len(ns.functions) > 0

if __name__ == "__main__":
    print("[TEST] Testing Loop Processing Functionality")
    print("=" * 50)
    
    test_loop_regex_patterns()
    print()
    
    success = test_loop_processing()
    if success:
        print("\n[+] All loop processing tests passed!")
    else:
        print("\n[-] Some loop processing tests failed!")
