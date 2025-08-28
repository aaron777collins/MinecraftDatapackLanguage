#!/usr/bin/env python3
"""
Test the loop processing functionality directly.
This module can be imported and run as part of the test suite.
"""

from minecraft_datapack_language import Pack

def test_loop_processing_direct():
    """Test that loop processing works correctly when called directly"""
    # Create a pack and test the processing function directly
    p = Pack('test')
    ns = p.namespace('test')
    
    # Test commands with a while loop
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
    
    # Verify that processing worked
    has_while_control = any('while_control' in name for name in ns.functions.keys())
    has_while_body = any('while_' in name and 'control' not in name for name in ns.functions.keys())
    
    return len(processed) > 0 and has_while_control and has_while_body

def test_for_loop_processing():
    """Test that for loop processing works correctly"""
    p = Pack('test')
    ns = p.namespace('test')
    
    # Test commands with a for loop
    commands = [
        'say Testing for loop',
        'tag @e[type=minecraft:player] add players',
        'for player in @e[tag=players]:',
        'say Processing player: @s',
        'effect give @s minecraft:speed 10 1'
    ]
    
    print("Testing for loop processing...")
    processed = p._process_control_flow('test', 'for_test', commands)
    
    print("Processed commands:")
    for i, cmd in enumerate(processed):
        print(f"  {i}: '{cmd}'")
    
    print("\nGenerated functions:")
    for func_name, func in ns.functions.items():
        print(f"  {func_name}: {func.commands}")
    
    # Verify that processing worked
    has_for_control = any('for_control' in name for name in ns.functions.keys())
    has_for_body = any('for_' in name and 'control' not in name for name in ns.functions.keys())
    
    return len(processed) > 0 and has_for_control and has_for_body

if __name__ == "__main__":
    print("[TEST] Testing Loop Processing")
    print("=" * 40)
    
    success1 = test_loop_processing_direct()
    print()
    
    success2 = test_for_loop_processing()
    
    if success1 and success2:
        print("\n[+] All loop processing tests passed!")
    else:
        print("\n[-] Some loop processing tests failed!")
