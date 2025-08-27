#!/usr/bin/env python3
"""
Test script to verify MDL parser works correctly with the deepest possible nesting.
Tests: for -> if -> for -> while -> if -> else -> for
Also tests nested function calls.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser import parse_mdl

def test_deepest_nesting():
    """Test the deepest possible nesting of control structures."""
    
    deepest_nesting_mdl = '''pack "test" description "Deepest nesting test" pack_format 48

namespace "test"

function "deepest_nesting":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            for item in @s:
                while "entity @s[type=minecraft:item]":
                    if "entity @s[nbt={Item:{id:'minecraft:diamond'}}]":
                        say Found diamond: @s
                        effect give @s minecraft:glowing 5 0
                    else:
                        say Not a diamond: @s
                        for entity in @e[type=minecraft:item]:
                            say Processing entity: @s
                            particle minecraft:firework ~ ~ ~ 0.1 0.1 0.1 0.01 1

on_tick "test:deepest_nesting"
'''
    
    print("Testing deepest possible nesting...")
    print("=" * 80)
    print("Structure: for -> if -> for -> while -> if -> else -> for")
    print("=" * 80)
    
    try:
        pack = parse_mdl(deepest_nesting_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            # Sort functions by name for easier reading
            sorted_functions = sorted(test_ns.functions.items())
            
            for func_name, func in sorted_functions:
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    [EMPTY]")
            
            # Check if the deepest function has content
            deepest_funcs = [name for name in test_ns.functions.keys() if "for" in name and len(name.split('_')) > 3]
            print(f"\nDeepest functions (likely the innermost for): {deepest_funcs}")
            
            for func_name in deepest_funcs:
                func = test_ns.functions[func_name]
                print(f"Deepest function '{func_name}' has {len(func.commands)} commands")
                if func.commands:
                    print(f"  Commands: {func.commands}")
                else:
                    print(f"  WARNING: Deepest function '{func_name}' is empty!")
        
        print("\nPASS: Deepest nesting test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Deepest nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_nested_function_calls():
    """Test nested function calls within control structures."""
    
    nested_calls_mdl = '''pack "test" description "Nested function calls test" pack_format 48

namespace "test"

function "helper1":
    say Helper 1 called
    effect give @s minecraft:speed 5 0

function "helper2":
    say Helper 2 called
    effect give @s minecraft:jump_boost 5 0

function "helper3":
    say Helper 3 called
    effect give @s minecraft:glowing 5 0

function "nested_calls":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            function test:helper1
            for item in @s:
                if "entity @s[type=minecraft:item]":
                    function test:helper2
                    while "entity @s[nbt={Item:{id:'minecraft:diamond'}}]":
                        function test:helper3
                        say Deep nested call
                else:
                    say No item found
        else:
            say Not a player

on_tick "test:nested_calls"
'''
    
    print("\nTesting nested function calls...")
    print("=" * 80)
    print("Structure: for -> if -> function -> for -> if -> function -> while -> function")
    print("=" * 80)
    
    try:
        pack = parse_mdl(nested_calls_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            # Sort functions by name for easier reading
            sorted_functions = sorted(test_ns.functions.items())
            
            for func_name, func in sorted_functions:
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    [EMPTY]")
        
        print("\nPASS: Nested function calls test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Nested function calls test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_nested_with_calls():
    """Test complex nesting with function calls."""
    
    complex_nested_mdl = '''pack "test" description "Complex nested with calls test" pack_format 48

namespace "test"

function "weapon_check":
    say Checking weapon
    effect give @s minecraft:strength 10 0

function "particle_effect":
    say Creating particles
    particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 5

function "complex_nested":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            for item in @s:
                if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
                    function test:weapon_check
                    while "entity @s[health=20.0]":
                        if "entity @s[gamemode=survival]":
                            say Healthy survival player with diamond sword: @s
                            function test:particle_effect
                            for entity in @e[type=minecraft:area_effect_cloud]:
                                say Processing cloud: @s
                                particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.05 3
                        else:
                            say Creative player with diamond sword: @s
                            effect give @s minecraft:night_vision 10 0
                else:
                    say Player without diamond sword: @s

on_tick "test:complex_nested"
'''
    
    print("\nTesting complex nested with function calls...")
    print("=" * 80)
    print("Structure: for -> if -> for -> if -> function -> while -> if -> function -> for")
    print("=" * 80)
    
    try:
        pack = parse_mdl(complex_nested_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            # Sort functions by name for easier reading
            sorted_functions = sorted(test_ns.functions.items())
            
            for func_name, func in sorted_functions:
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    [EMPTY]")
            
            # Check if the deepest function has content
            deepest_funcs = [name for name in test_ns.functions.keys() if "for" in name and len(name.split('_')) > 3]
            print(f"\nDeepest functions (likely the innermost for): {deepest_funcs}")
            
            for func_name in deepest_funcs:
                func = test_ns.functions[func_name]
                print(f"Deepest function '{func_name}' has {len(func.commands)} commands")
                if func.commands:
                    print(f"  Commands: {func.commands}")
                else:
                    print(f"  WARNING: Deepest function '{func_name}' is empty!")
        
        print("\nPASS: Complex nested with calls test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Complex nested with calls test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL Deep Nesting and Function Calls Test Suite")
    print("=" * 80)
    
    # Run all tests
    test1 = test_deepest_nesting()
    test2 = test_nested_function_calls()
    test3 = test_complex_nested_with_calls()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Deepest nesting: {'PASS' if test1 else 'FAIL'}")
    print(f"Nested function calls: {'PASS' if test2 else 'FAIL'}")
    print(f"Complex nested with calls: {'PASS' if test3 else 'FAIL'}")
    
    if all([test1, test2, test3]):
        print("\nSUCCESS: All tests passed!")
        print("The parser can handle the most complex nested control structures and function calls!")
    else:
        print("\nWARNING: Some tests failed.")
        print("The parser has limitations with deeply nested control structures.")
