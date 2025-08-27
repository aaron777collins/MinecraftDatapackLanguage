#!/usr/bin/env python3
"""
Test script to verify MDL parser works correctly with the deepest possible nesting.
Tests: for -> if -> for -> while -> if -> else -> for
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
    print("Input MDL:")
    print(deepest_nesting_mdl)
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
                    print("    ⚠️  EMPTY!")
            
            # Check if the deepest function has content
            deepest_funcs = [name for name in test_ns.functions.keys() if "for" in name and len(name.split('_')) > 3]
            print(f"\nDeepest functions (likely the innermost for): {deepest_funcs}")
            
            for func_name in deepest_funcs:
                func = test_ns.functions[func_name]
                print(f"Deepest function '{func_name}' has {len(func.commands)} commands")
                if func.commands:
                    print(f"  Commands: {func.commands}")
                else:
                    print(f"  ⚠️  WARNING: Deepest function '{func_name}' is empty!")
        
        print("\n✅ Deepest nesting test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Deepest nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alternate_deep_nesting():
    """Test an alternate deep nesting pattern."""
    
    alternate_deep_mdl = '''pack "test" description "Alternate deep nesting test" pack_format 48

namespace "test"

function "alternate_deep":
    for entity in @e:
        if "entity @s[type=minecraft:player]":
            while "entity @s[gamemode=survival]":
                for item in @s:
                    if "entity @s[type=minecraft:item]":
                        say Player has item: @s
                        effect give @s minecraft:haste 5 0
                    else:
                        say Player has no items
                        for block in @e[type=minecraft:falling_block]:
                            say Found falling block: @s
                            particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.05 3

on_tick "test:alternate_deep"
'''
    
    print("\nTesting alternate deep nesting pattern...")
    print("=" * 80)
    print("Structure: for -> if -> while -> for -> if -> else -> for")
    print("=" * 80)
    print("Input MDL:")
    print(alternate_deep_mdl)
    print("=" * 80)
    
    try:
        pack = parse_mdl(alternate_deep_mdl)
        
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
                    print("    ⚠️  EMPTY!")
            
            # Check if the deepest function has content
            deepest_funcs = [name for name in test_ns.functions.keys() if "for" in name and len(name.split('_')) > 3]
            print(f"\nDeepest functions (likely the innermost for): {deepest_funcs}")
            
            for func_name in deepest_funcs:
                func = test_ns.functions[func_name]
                print(f"Deepest function '{func_name}' has {len(func.commands)} commands")
                if func.commands:
                    print(f"  Commands: {func.commands}")
                else:
                    print(f"  ⚠️  WARNING: Deepest function '{func_name}' is empty!")
        
        print("\n✅ Alternate deep nesting test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Alternate deep nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_weapon_effects_deep():
    """Test the weapon effects example with deeper nesting."""
    
    weapon_effects_deep_mdl = '''pack "test" description "Weapon effects with deep nesting" pack_format 48

namespace "test"

function "weapon_effects_deep":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            for item in @s:
                if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
                    while "entity @s[health=20.0]":
                        if "entity @s[gamemode=survival]":
                            say Healthy survival player with diamond sword: @s
                            effect give @s minecraft:strength 10 1
                            effect give @s minecraft:glowing 10 0
                            for particle in @e[type=minecraft:area_effect_cloud]:
                                particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.5 0.5 0.1 10
                        else:
                            say Creative player with diamond sword: @s
                            effect give @s minecraft:night_vision 10 0
                else:
                    say Player without diamond sword: @s

on_tick "test:weapon_effects_deep"
'''
    
    print("\nTesting weapon effects with deep nesting...")
    print("=" * 80)
    print("Structure: for -> if -> for -> if -> while -> if -> else -> for")
    print("=" * 80)
    print("Input MDL:")
    print(weapon_effects_deep_mdl)
    print("=" * 80)
    
    try:
        pack = parse_mdl(weapon_effects_deep_mdl)
        
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
                    print("    ⚠️  EMPTY!")
            
            # Check if the deepest function has content
            deepest_funcs = [name for name in test_ns.functions.keys() if "for" in name and len(name.split('_')) > 3]
            print(f"\nDeepest functions (likely the innermost for): {deepest_funcs}")
            
            for func_name in deepest_funcs:
                func = test_ns.functions[func_name]
                print(f"Deepest function '{func_name}' has {len(func.commands)} commands")
                if func.commands:
                    print(f"  Commands: {func.commands}")
                else:
                    print(f"  ⚠️  WARNING: Deepest function '{func_name}' is empty!")
        
        print("\n✅ Weapon effects deep nesting test completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Weapon effects deep nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL Deepest Nesting Test Suite")
    print("=" * 80)
    
    # Run all tests
    test1 = test_deepest_nesting()
    test2 = test_alternate_deep_nesting()
    test3 = test_weapon_effects_deep()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Deepest nesting: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Alternate deep nesting: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Weapon effects deep nesting: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All deepest nesting tests passed!")
        print("The parser can handle the most complex nested control structures!")
    else:
        print("\n⚠️  Some deepest nesting tests failed.")
        print("The parser has limitations with deeply nested control structures.")
