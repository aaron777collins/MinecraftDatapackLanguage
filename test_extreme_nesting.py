#!/usr/bin/env python3
"""
Extreme nesting test for JavaScript-style MDL parser.
This test pushes the limits with the most complex nested structures possible.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_extreme_nesting():
    """Test the most extreme nesting possible with the JavaScript-style parser."""
    
    extreme_nesting_mdl = '''pack "extreme" description "Extreme nesting test" pack_format 82;

namespace "extreme";

// Helper functions for the extreme test
function "helper_1" {
    say Helper 1 called;
    effect give @s minecraft:strength 5 0;
}

function "helper_2" {
    say Helper 2 called;
    particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 3;
}

function "helper_3" {
    say Helper 3 called;
    effect give @s minecraft:speed 5 0;
}

function "helper_4" {
    say Helper 4 called;
    particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.05 2;
}

function "helper_5" {
    say Helper 5 called;
    effect give @s minecraft:jump_boost 5 0;
}

function "helper_6" {
    say Helper 6 called;
    particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.01 1;
}

function "helper_7" {
    say Helper 7 called;
    effect give @s minecraft:night_vision 5 0;
}

function "helper_8" {
    say Helper 8 called;
    particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.01 1;
}

// The main extreme nesting function
function "extreme_nesting" {
    // Level 1: For loop
    for player in @a {
        // Level 2: If statement
        if "entity @s[type=minecraft:player]" {
            // Level 3: For loop
            for item in @s {
                // Level 4: While loop
                while "entity @s[type=minecraft:item]" {
                    // Level 5: If statement
                    if "entity @s[nbt={Item:{id:'minecraft:diamond'}}]" {
                        // Level 6: For loop
                        for entity in @e[type=minecraft:area_effect_cloud] {
                            // Level 7: If statement
                            if "entity @s[type=minecraft:area_effect_cloud]" {
                                // Level 8: While loop
                                while "entity @s[type=minecraft:area_effect_cloud]" {
                                    // Level 9: If statement
                                    if "entity @s[type=minecraft:area_effect_cloud]" {
                                        // Level 10: For loop
                                        for particle in @e[type=minecraft:item] {
                                            // Level 11: If statement
                                            if "entity @s[type=minecraft:item]" {
                                                // Level 12: While loop
                                                while "entity @s[type=minecraft:item]" {
                                                    // Level 13: If statement
                                                    if "entity @s[nbt={Item:{id:'minecraft:emerald'}}]" {
                                                        say Found emerald at level 13!;
                                                        function extreme:helper_1;
                                                        // Level 14: For loop
                                                        for deep in @e[type=minecraft:item] {
                                                            // Level 15: If statement
                                                            if "entity @s[type=minecraft:item]" {
                                                                say Processing deep item at level 15;
                                                                function extreme:helper_2;
                                                                // Level 16: While loop
                                                                while "entity @s[type=minecraft:item]" {
                                                                    // Level 17: If statement
                                                                    if "entity @s[nbt={Item:{id:'minecraft:gold_ingot'}}]" {
                                                                        say Found gold ingot at level 17!;
                                                                        function extreme:helper_3;
                                                                        // Level 18: For loop
                                                                        for deeper in @e[type=minecraft:item] {
                                                                            // Level 19: If statement
                                                                            if "entity @s[type=minecraft:item]" {
                                                                                say Processing deeper item at level 19;
                                                                                function extreme:helper_4;
                                                                                // Level 20: While loop
                                                                                while "entity @s[type=minecraft:item]" {
                                                                                    // Level 21: If statement
                                                                                    if "entity @s[nbt={Item:{id:'minecraft:iron_ingot'}}]" {
                                                                                        say Found iron ingot at level 21!;
                                                                                        function extreme:helper_5;
                                                                                        // Level 22: For loop
                                                                                        for deepest in @e[type=minecraft:item] {
                                                                                            // Level 23: If statement
                                                                                            if "entity @s[type=minecraft:item]" {
                                                                                                say Processing deepest item at level 23;
                                                                                                function extreme:helper_6;
                                                                                                // Level 24: While loop
                                                                                                while "entity @s[type=minecraft:item]" {
                                                                                                    // Level 25: If statement
                                                                                                    if "entity @s[nbt={Item:{id:'minecraft:coal'}}]" {
                                                                                                        say Found coal at level 25!;
                                                                                                        function extreme:helper_7;
                                                                                                        // Level 26: For loop
                                                                                                        for final in @e[type=minecraft:item] {
                                                                                                            // Level 27: If statement
                                                                                                            if "entity @s[type=minecraft:item]" {
                                                                                                                say Processing final item at level 27;
                                                                                                                function extreme:helper_8;
                                                                                                                // Level 28: While loop
                                                                                                                while "entity @s[type=minecraft:item]" {
                                                                                                                    // Level 29: If statement
                                                                                                                    if "entity @s[nbt={Item:{id:'minecraft:redstone'}}]" {
                                                                                                                        say Found redstone at level 29!;
                                                                                                                        say This is the deepest level!;
                                                                                                                        effect give @s minecraft:glowing 10 0;
                                                                                                                        particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 10;
                                                                                                                    } else {
                                                                                                                        say Not redstone at level 29;
                                                                                                                        effect give @s minecraft:haste 5 0;
                                                                                                                    }
                                                                                                                }
                                                                                                            } else {
                                                                                                                say Not an item at level 27;
                                                                                                                effect give @s minecraft:resistance 5 0;
                                                                                                            }
                                                                                                        }
                                                                                                    } else {
                                                                                                        say Not coal at level 25;
                                                                                                        effect give @s minecraft:fire_resistance 5 0;
                                                                                                    }
                                                                                                }
                                                                                            } else {
                                                                                                say Not an item at level 23;
                                                                                                effect give @s minecraft:water_breathing 5 0;
                                                                                            }
                                                                                        }
                                                                                    } else {
                                                                                        say Not iron ingot at level 21;
                                                                                        effect give @s minecraft:slow_falling 5 0;
                                                                                    }
                                                                                }
                                                                            } else {
                                                                                say Not an item at level 19;
                                                                                effect give @s minecraft:conduit_power 5 0;
                                                                            }
                                                                        }
                                                                    } else {
                                                                        say Not gold ingot at level 17;
                                                                        effect give @s minecraft:dolphins_grace 5 0;
                                                                    }
                                                                }
                                                            } else {
                                                                say Not an item at level 15;
                                                                effect give @s minecraft:bad_omen 5 0;
                                                            }
                                                        }
                                                    } else {
                                                        say Not emerald at level 13;
                                                        effect give @s minecraft:hero_of_the_village 5 0;
                                                    }
                                                }
                                            } else {
                                                say Not an item at level 11;
                                                effect give @s minecraft:darkness 5 0;
                                            }
                                        }
                                    } else {
                                        say Not an area effect cloud at level 9;
                                        effect give @s minecraft:blindness 5 0;
                                    }
                                }
                            } else {
                                say Not an area effect cloud at level 7;
                                effect give @s minecraft:levitation 5 0;
                            }
                        }
                    } else {
                        say Not a diamond at level 5;
                        effect give @s minecraft:slow 5 0;
                    }
                }
            }
        } else {
            say Not a player at level 2;
            effect give @s minecraft:poison 5 0;
        }
    }
}

on_tick "extreme:extreme_nesting";
'''
    
    print("Testing EXTREME nesting with JavaScript-style parser...")
    print("=" * 80)
    print("Structure: 29 levels deep with for -> if -> for -> while -> if -> else -> for -> if -> while -> if -> for -> if -> while -> if -> for -> if -> while -> if -> for -> if -> while -> if -> for -> if -> while -> if -> for -> if -> while -> if")
    print("=" * 80)
    
    try:
        # Test lexer first
        tokens = lex_mdl_js(extreme_nesting_mdl)
        print(f"Lexer generated {len(tokens)} tokens")
        
        # Test parser
        ast = parse_mdl_js(extreme_nesting_mdl)
        
        print(f"Parser generated AST with:")
        print(f"  Pack: {ast['pack']}")
        print(f"  Namespaces: {len(ast['namespaces'])}")
        print(f"  Functions: {len(ast['functions'])}")
        print(f"  Hooks: {len(ast['hooks'])}")
        print(f"  Tags: {len(ast['tags'])}")
        
        # Check the main function
        if ast['functions']:
            main_func = ast['functions'][-1]  # The extreme_nesting function should be last
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
            
            # Count total nesting levels
            def count_max_depth(statements, current_depth=0):
                max_depth = current_depth
                for stmt in statements:
                    if hasattr(stmt, 'body'):
                        depth = count_max_depth(stmt.body, current_depth + 1)
                        max_depth = max(max_depth, depth)
                return max_depth
            
            max_depth = count_max_depth(main_func.body)
            print(f"\nMaximum nesting depth: {max_depth} levels")
            
            # Count total statements
            def count_statements(statements):
                total = 0
                for stmt in statements:
                    total += 1
                    if hasattr(stmt, 'body'):
                        total += count_statements(stmt.body)
                return total
            
            total_statements = count_statements(main_func.body)
            print(f"Total nested statements: {total_statements}")
        
        print("\nPASS: Extreme nesting test with JavaScript-style parser completed!")
        return True
        
    except Exception as e:
        print(f"FAIL: Extreme nesting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MDL JavaScript-Style Extreme Nesting Test")
    print("=" * 80)
    
    # Run the extreme test
    success = test_extreme_nesting()
    
    print("\n" + "=" * 80)
    print("Test Results Summary:")
    print(f"Extreme nesting: {'PASS' if success else 'FAIL'}")
    
    if success:
        print("\nSUCCESS: Extreme nesting test passed!")
        print("The JavaScript-style parser can handle the most complex nested structures!")
    else:
        print("\nWARNING: Extreme nesting test failed.")
        print("The JavaScript-style parser needs more work.")
