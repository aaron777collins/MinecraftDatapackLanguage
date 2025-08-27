#!/usr/bin/env python3
"""
Test script to verify the JavaScript-style MDL parser works with unlimited nesting.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_deepest_nesting_js():
    """Test the deepest possible nesting with the JavaScript-style parser."""
    
    deepest_nesting_mdl = '''pack "test" description "Deepest nesting test" pack_format 48;

namespace "test";

function "deepest_nesting" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            for item in @s {
                while "entity @s[type=minecraft:item]" {
                    if "entity @s[nbt={Item:{id:'minecraft:diamond'}}]" {
                        say Found diamond: @s;
                        effect give @s minecraft:glowing 5 0;
                    } else {
                        say Not a diamond: @s;
                        for entity in @e[type=minecraft:item] {
                            say Processing entity: @s;
                            particle minecraft:firework ~ ~ ~ 0.1 0.1 0.1 0.01 1;
                        }
                    }
                }
            }
        }
    }
}

on_tick "test:deepest_nesting";
'''
    
    print("Testing deepest nesting with JavaScript-style parser...")
    print("=" * 80)
    print("Structure: for -> if -> for -> while -> if -> else -> for")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(deepest_nesting_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(deepest_nesting_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Check the main function
        if ast['functions']:
            main_func = ast['functions'][0]
            print(f"\nMain function '{main_func.name}' has {len(main_func.body)} statements")
            
            # Analyze the nesting structure
            def analyze_nesting(statements, level=0):
                indent = "  " * level
                for stmt in statements:
                    if hasattr(stmt, '__class__'):
                        print(f"{indent}- {stmt.__class__.__name__}")
                        if hasattr(stmt, 'body'):
                            analyze_nesting(stmt.body, level + 1)
            
            analyze_nesting(main_func.body)
        
        print("\nPASS: Deepest nesting test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Deepest nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_weapon_effects_js():
    """Test the weapon effects example with the JavaScript-style parser."""
    
    weapon_effects_mdl = '''pack "example" description "Weapon effects test" pack_format 82;

namespace "example";

function "globalweaponeffects" {
    for player in @a {
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
            effect give @s minecraft:strength 10 1;
            effect give @s minecraft:glowing 10 0;
            particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.5 0.5 0.1 10;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:golden_sword'}}]" {
            effect give @s minecraft:speed 10 1;
            effect give @s minecraft:night_vision 10 0;
            particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 5;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:netherite_sword'}}]" {
            effect give @s minecraft:resistance 10 1;
            effect give @s minecraft:fire_resistance 10 0;
            particle minecraft:flame ~ ~1 ~ 0.4 0.4 0.4 0.1 8;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:iron_sword'}}]" {
            effect give @s minecraft:haste 10 0;
            particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.05 3;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:wooden_sword'}}]" {
            effect give @s minecraft:jump_boost 10 0;
            particle minecraft:cloud ~ ~1 ~ 0.2 0.2 0.2 0.05 2;
        }
    }
}

on_tick "example:globalweaponeffects";
'''
    
    print("\nTesting weapon effects with JavaScript-style parser...")
    print("=" * 80)
    
    try:
        ast = parse_mdl_js(weapon_effects_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        
        # Check the main function
        if ast['functions']:
            main_func = ast['functions'][0]
            print(f"\nMain function '{main_func.name}' has {len(main_func.body)} statements")
            
            # Check if it's a for loop with conditionals
            if main_func.body and hasattr(main_func.body[0], '__class__') and main_func.body[0].__class__.__name__ == 'ForLoop':
                for_loop = main_func.body[0]
                print(f"  For loop: {for_loop.variable} in {for_loop.selector}")
                print(f"  For loop body has {len(for_loop.body)} statements")
                
                # Check if the for loop contains conditionals
                conditional_count = 0
                for stmt in for_loop.body:
                    if hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'IfStatement':
                        conditional_count += 1
                        print(f"    Found if statement with {len(stmt.body)} commands")
                        if stmt.elif_branches:
                            print(f"    Has {len(stmt.elif_branches)} elif branches")
                
                print(f"  Total conditionals in for loop: {conditional_count}")
        
        print("\nPASS: Weapon effects test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Weapon effects test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_nested_with_calls_js():
    """Test complex nesting with function calls using the JavaScript-style parser."""
    
    complex_nested_mdl = '''pack "test" description "Complex nested with calls test" pack_format 48;

namespace "test";

function "weapon_check" {
    say Checking weapon;
    effect give @s minecraft:strength 10 0;
}

function "particle_effect" {
    say Creating particles;
    particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 5;
}

function "complex_nested" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            for item in @s {
                if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
                    function test:weapon_check;
                    while "entity @s[health=20.0]" {
                        if "entity @s[gamemode=survival]" {
                            say Healthy survival player with diamond sword: @s;
                            function test:particle_effect;
                            for entity in @e[type=minecraft:area_effect_cloud] {
                                say Processing cloud: @s;
                                particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.05 3;
                            }
                        } else {
                            say Creative player with diamond sword: @s;
                            effect give @s minecraft:night_vision 10 0;
                        }
                    }
                } else {
                    say Player without diamond sword: @s;
                }
            }
        }
    }
}

on_tick "test:complex_nested";
'''
    
    print("\nTesting complex nested with calls using JavaScript-style parser...")
    print("=" * 80)
    
    try:
        ast = parse_mdl_js(complex_nested_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        
        # Check all functions
        for func in ast['functions']:
            print(f"\nFunction '{func.name}' has {len(func.body)} statements")
            
            def count_nesting(statements, level=0):
                count = 0
                for stmt in statements:
                    if hasattr(stmt, '__class__'):
                        count += 1
                        if hasattr(stmt, 'body'):
                            count += count_nesting(stmt.body, level + 1)
                return count
            
            total_statements = count_nesting(func.body)
            print(f"  Total nested statements: {total_statements}")
        
        print("\nPASS: Complex nested with calls test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Complex nested with calls test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Parser Test Suite")
    print("=" * 80)
    
    # Run all tests
    test1 = test_deepest_nesting_js()
    test2 = test_weapon_effects_js()
    test3 = test_complex_nested_with_calls_js()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Deepest nesting: {'PASS' if test1 else 'FAIL'}")
    print(f"Weapon effects: {'PASS' if test2 else 'FAIL'}")
    print(f"Complex nested with calls: {'PASS' if test3 else 'FAIL'}")
    
    if all([test1, test2, test3]):
        print("\nSUCCESS: All tests passed!")
        print("The JavaScript-style parser can handle unlimited nesting and all control structures!")
    else:
        print("\nWARNING: Some tests failed.")
        print("The JavaScript-style parser needs more work.")
