#!/usr/bin/env python3
"""
Test script to verify MDL parser works correctly with nested control structures.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser import parse_mdl

def test_nested_for_with_if():
    """Test nested for loops with if statements."""
    
    nested_for_mdl = '''pack "test" description "Nested for loops test" pack_format 48

namespace "test"

function "nested_for":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            for item in @s:
                if "entity @s[type=minecraft:item]":
                    say Found item: @s
                else:
                    say Not an item: @s
        else:
            say Not a player: @s

on_tick "test:nested_for"
'''
    
    print("Testing nested for loops with if statements...")
    print("=" * 60)
    print("Input MDL:")
    print(nested_for_mdl)
    print("=" * 60)
    
    try:
        pack = parse_mdl(nested_for_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            for func_name, func in test_ns.functions.items():
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    ⚠️  EMPTY!")
        
        print("\n✅ Nested for loops test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Nested for loops test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_while_with_nested_if():
    """Test while loops with nested if statements."""
    
    while_nested_mdl = '''pack "test" description "While with nested if test" pack_format 48

namespace "test"

function "while_nested":
    while "entity @a":
        if "entity @s[type=minecraft:player]":
            say Player found: @s
            effect give @s minecraft:glowing 5 0
        else:
            say Non-player: @s
            effect give @s minecraft:invisibility 5 0

on_tick "test:while_nested"
'''
    
    print("\nTesting while loops with nested if statements...")
    print("=" * 60)
    print("Input MDL:")
    print(while_nested_mdl)
    print("=" * 60)
    
    try:
        pack = parse_mdl(while_nested_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            for func_name, func in test_ns.functions.items():
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    ⚠️  EMPTY!")
        
        print("\n✅ While with nested if test completed!")
        return True
        
    except Exception as e:
        print(f"❌ While with nested if test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_nested():
    """Test complex nested control structures."""
    
    complex_nested_mdl = '''pack "test" description "Complex nested test" pack_format 48

namespace "test"

function "complex_nested":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            while "entity @s[gamemode=survival]":
                if "entity @s[health=20.0]":
                    say Healthy player: @s
                    effect give @s minecraft:strength 10 0
                else:
                    say Damaged player: @s
                    effect give @s minecraft:regeneration 10 0
        else:
            say Non-player entity: @s

on_tick "test:complex_nested"
'''
    
    print("\nTesting complex nested control structures...")
    print("=" * 60)
    print("Input MDL:")
    print(complex_nested_mdl)
    print("=" * 60)
    
    try:
        pack = parse_mdl(complex_nested_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            for func_name, func in test_ns.functions.items():
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    ⚠️  EMPTY!")
        
        print("\n✅ Complex nested test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Complex nested test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_while():
    """Test simple while loop to compare."""
    
    simple_while_mdl = '''pack "test" description "Simple while test" pack_format 48

namespace "test"

function "simple_while":
    while "entity @a":
        say Found entity: @s
        effect give @s minecraft:glowing 5 0

on_tick "test:simple_while"
'''
    
    print("\nTesting simple while loop...")
    print("=" * 40)
    
    try:
        pack = parse_mdl(simple_while_mdl)
        
        if "test" in pack.namespaces:
            test_ns = pack.namespaces["test"]
            print(f"Generated functions: {list(test_ns.functions.keys())}")
            
            for func_name, func in test_ns.functions.items():
                print(f"\nFunction '{func_name}':")
                print(f"  Commands ({len(func.commands)}):")
                for i, cmd in enumerate(func.commands):
                    print(f"    {i+1}: {cmd}")
                if not func.commands:
                    print("    ⚠️  EMPTY!")
        
        print("\n✅ Simple while test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple while test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL Nested Control Structures Test Suite")
    print("=" * 80)
    
    # Run all tests
    test1 = test_simple_while()
    test2 = test_while_with_nested_if()
    test3 = test_nested_for_with_if()
    test4 = test_complex_nested()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Simple while: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"While with nested if: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Nested for with if: {'✅ PASS' if test3 else '❌ FAIL'}")
    print(f"Complex nested: {'✅ PASS' if test4 else '❌ FAIL'}")
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 All nested control structure tests passed!")
    else:
        print("\n⚠️  Some nested control structure tests failed.")
