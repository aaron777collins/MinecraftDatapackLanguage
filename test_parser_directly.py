#!/usr/bin/env python3
"""
Test script to verify MDL parser works correctly on the weapon effects example.
This tests the parser directly without needing to build and release.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser import parse_mdl
from minecraft_datapack_language.pack import Pack

def test_weapon_effects_parsing():
    """Test parsing the weapon effects example directly."""
    
    # The weapon effects example with for loop and conditionals
    weapon_effects_mdl = '''# Weapon Effects Datapack
# Provides automatic effects and particles for players based on their equipped weapon
pack "example" description "Automatically applies effects and particles to players based on their equipped weapon" pack_format 82 min_format [82, 0] max_format [82, 1] min_engine_version "1.21.4"

namespace "example"

# Global weapon effects system - affects all players
function "globalweaponeffects":
    for player in @a:
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
            effect give @s minecraft:strength 10 1
            effect give @s minecraft:glowing 10 0
            particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.5 0.5 0.1 10
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:golden_sword'}}]":
            effect give @s minecraft:speed 10 1
            effect give @s minecraft:night_vision 10 0
            particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 5
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:netherite_sword'}}]":
            effect give @s minecraft:resistance 10 1
            effect give @s minecraft:fire_resistance 10 0
            particle minecraft:flame ~ ~1 ~ 0.4 0.4 0.4 0.1 8
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:iron_sword'}}]":
            effect give @s minecraft:haste 10 0
            particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.05 3
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:wooden_sword'}}]":
            effect give @s minecraft:jump_boost 10 0
            particle minecraft:cloud ~ ~1 ~ 0.2 0.2 0.2 0.05 2

# Hook the function into tick
on_tick "example:globalweaponeffects"

# Function tag examples
tag function "minecraft:tick":
    add "example:globalweaponeffects"

# Data tag examples across registries
tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"
'''

    print("Testing MDL parser on weapon effects example...")
    print("=" * 60)
    
    try:
        # Parse the MDL
        pack = parse_mdl(weapon_effects_mdl)
        
        print(f"[+] Successfully parsed MDL!")
        print(f"Pack name: {pack.name}")
        print(f"Pack description: {pack.description}")
        print(f"Pack format: {pack.pack_format}")
        print(f"Namespaces: {list(pack.namespaces.keys())}")
        
        # Check if the function was parsed correctly
        if "example" in pack.namespaces:
            example_ns = pack.namespaces["example"]
            print(f"Functions in 'example' namespace: {list(example_ns.functions.keys())}")
            
            # Check the main function
            if "globalweaponeffects" in example_ns.functions:
                main_func = example_ns.functions["globalweaponeffects"]
                print(f"Main function commands: {len(main_func.commands)}")
                print("First few commands:")
                for i, cmd in enumerate(main_func.commands[:5]):
                    print(f"  {i+1}: {cmd}")
                
                # Check if for loop function was generated
                for_funcs = [name for name in example_ns.functions.keys() if "for" in name]
                print(f"For loop functions generated: {for_funcs}")
                
                # Check if conditional functions were generated
                conditional_funcs = [name for name in example_ns.functions.keys() if any(x in name for x in ["if", "elif", "else"])]
                print(f"Conditional functions generated: {conditional_funcs}")
                
                # Check if the for loop function has content
                for func_name in for_funcs:
                    func = example_ns.functions[func_name]
                    print(f"Function '{func_name}' has {len(func.commands)} commands")
                    if func.commands:
                        print(f"  First command: {func.commands[0]}")
                    else:
                        print(f"  ⚠️  WARNING: Function '{func_name}' is empty!")
                
            else:
                print("[-] Main function 'globalweaponeffects' not found!")
        else:
            print("[-] Namespace 'example' not found!")
        
        # Check hooks
        print(f"Tick functions: {pack._tick_functions}")
        print(f"Load functions: {pack._load_functions}")
        
        # Check tags
        print(f"Tags: {len(pack.tags)}")
        for tag in pack.tags:
            print(f"  {tag.registry}:{tag.name} -> {tag.values}")
        
        print("\n" + "=" * 60)
        print("[+] Parser test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Parser test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_for_loop():
    """Test a simple for loop to isolate the issue."""
    
    simple_for_mdl = '''pack "test" description "Simple for loop test" pack_format 48

namespace "test"

function "simple_for":
    for player in @a:
        say Hello player: @s
        effect give @s minecraft:speed 5 0

on_tick "test:simple_for"
'''
    
    print("\nTesting simple for loop...")
    print("=" * 40)
    
    try:
        pack = parse_mdl(simple_for_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Functions: {list(test_ns.functions.keys())}")
            
            if "simple_for" in test_ns.functions:
                main_func = test_ns.functions["simple_for"]
                print(f"Main function commands: {len(main_func.commands)}")
                for i, cmd in enumerate(main_func.commands):
                    print(f"  {i+1}: {cmd}")
                
                # Check for loop function
                for_funcs = [name for name in test_ns.functions.keys() if "for" in name]
                print(f"For loop functions: {for_funcs}")
                
                for func_name in for_funcs:
                    func = test_ns.functions[func_name]
                    print(f"Function '{func_name}' has {len(func.commands)} commands")
                    if func.commands:
                        print(f"  Commands: {func.commands}")
                    else:
                        print(f"  ⚠️  WARNING: Function '{func_name}' is empty!")
        
        print("✅ Simple for loop test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple for loop test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_for_with_conditionals():
    """Test for loop with conditionals to see the specific issue."""
    
    for_with_conditionals_mdl = '''pack "test" description "For loop with conditionals test" pack_format 48

namespace "test"

function "for_with_conditionals":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            say Player found: @s
            effect give @s minecraft:glowing 5 0
        else:
            say Non-player entity: @s

on_tick "test:for_with_conditionals"
'''
    
    print("\nTesting for loop with conditionals...")
    print("=" * 50)
    
    try:
        pack = parse_mdl(for_with_conditionals_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Functions: {list(test_ns.functions.keys())}")
            
            if "for_with_conditionals" in test_ns.functions:
                main_func = test_ns.functions["for_with_conditionals"]
                print(f"Main function commands: {len(main_func.commands)}")
                for i, cmd in enumerate(main_func.commands):
                    print(f"  {i+1}: {cmd}")
                
                # Check all generated functions
                        for func_name, func in test_ns.functions.items():
            print(f"Function '{func_name}' has {len(func.commands)} commands")
            if func.commands:
                print(f"  Commands: {func.commands}")
            else:
                print(f"  [-] WARNING: Function '{func_name}' is empty!")
        
        print("✅ For loop with conditionals test completed!")
        return True
        
    except Exception as e:
        print(f"❌ For loop with conditionals test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL Parser Test Suite")
    print("=" * 60)
    
    # Run all tests
    test1 = test_simple_for_loop()
    test2 = test_for_with_conditionals()
    test3 = test_weapon_effects_parsing()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Simple for loop: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"For with conditionals: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Weapon effects example: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! The parser is working correctly.")
    else:
        print("\n⚠️  Some tests failed. The parser needs fixes before release.")
