#!/usr/bin/env python3
"""
Python API test for loop functionality.
This demonstrates how to achieve the same loop logic using the Python API.
"""

from minecraft_datapack_language import Pack

def build_loop_pack():
    """Build a pack with loop logic using the Python API"""
    
    # Create the pack
    p = Pack(
        name="Loop Tests Python",
        description="Python API tests for loop functionality",
        pack_format=48
    )
    
    # Create namespace
    ns = p.namespace("test")
    
    # Test 1: Simple while loop (using execute commands)
    ns.function("simple_while", 
        "say Testing simple while loop",
        "scoreboard players set @s loop_counter 5",
        "execute if score @s loop_counter matches 1.. run function test:simple_while_control"
    )
    
    ns.function("simple_while_control",
        "execute if score @s loop_counter matches 1.. run function test:simple_while_body",
        "execute if score @s loop_counter matches 1.. run function test:simple_while_control"
    )
    
    ns.function("simple_while_body",
        "say Counter: @s loop_counter",
        "scoreboard players remove @s loop_counter 1",
        "say Decremented counter"
    )
    
    # Test 2: While loop with entity condition
    ns.function("entity_while",
        "say Testing while loop with entity condition",
        "execute if entity @e[type=minecraft:zombie,distance=..10] run function test:entity_while_control"
    )
    
    ns.function("entity_while_control",
        "execute if entity @e[type=minecraft:zombie,distance=..10] run function test:entity_while_body",
        "execute if entity @e[type=minecraft:zombie,distance=..10] run function test:entity_while_control"
    )
    
    ns.function("entity_while_body",
        "say Zombie nearby!",
        "effect give @e[type=minecraft:zombie,distance=..10,limit=1] minecraft:glowing 5 1",
        "say Applied effect to zombie"
    )
    
    # Test 3: For loop with entity collection
    ns.function("entity_for",
        "say Testing for loop with entity collection",
        "tag @e[type=minecraft:player] add players",
        "execute if entity @e[tag=players] run function test:entity_for_control"
    )
    
    ns.function("entity_for_control",
        "execute as @e[tag=players] run function test:entity_for_body"
    )
    
    ns.function("entity_for_body",
        "say Processing player: @s",
        "effect give @s minecraft:speed 10 1",
        "tellraw @s {\"text\":\"You got speed!\",\"color\":\"green\"}"
    )
    
    # Test 4: For loop with item collection
    ns.function("item_for",
        "say Testing for loop with item collection",
        "tag @e[type=minecraft:item] add items",
        "execute if entity @e[tag=items] run function test:item_for_control"
    )
    
    ns.function("item_for_control",
        "execute as @e[tag=items] run function test:item_for_body"
    )
    
    ns.function("item_for_body",
        "say Processing item: @s",
        "effect give @s minecraft:glowing 5 1"
    )
    
    # Test 5: Mixed control structures
    ns.function("mixed_control",
        "say Testing mixed control structures",
        "execute if entity @s[type=minecraft:player] run function test:mixed_control_player",
        "execute unless entity @s[type=minecraft:player] run function test:mixed_control_else"
    )
    
    ns.function("mixed_control_player",
        "say Player detected, starting loops",
        "scoreboard players set @s counter 3",
        "execute if score @s counter matches 1.. run function test:mixed_control_while_control"
    )
    
    ns.function("mixed_control_while_control",
        "execute if score @s counter matches 1.. run function test:mixed_control_while_body",
        "execute if score @s counter matches 1.. run function test:mixed_control_while_control"
    )
    
    ns.function("mixed_control_while_body",
        "say Loop iteration: @s counter",
        "execute if entity @e[type=minecraft:zombie,distance=..5] run function test:mixed_control_for_control",
        "scoreboard players remove @s counter 1"
    )
    
    ns.function("mixed_control_for_control",
        "execute as @e[type=minecraft:zombie,distance=..5] run function test:mixed_control_for_body"
    )
    
    ns.function("mixed_control_for_body",
        "say Found zombie: @s",
        "effect give @s minecraft:poison 3 1"
    )
    
    ns.function("mixed_control_else",
        "say No player found"
    )
    
    # Test 6: Nested loops
    ns.function("nested_loops",
        "say Testing nested loops",
        "scoreboard players set @s outer 3",
        "execute if score @s outer matches 1.. run function test:nested_loops_outer_control"
    )
    
    ns.function("nested_loops_outer_control",
        "execute if score @s outer matches 1.. run function test:nested_loops_outer_body",
        "execute if score @s outer matches 1.. run function test:nested_loops_outer_control"
    )
    
    ns.function("nested_loops_outer_body",
        "say Outer loop: @s outer",
        "scoreboard players set @s inner 2",
        "execute if score @s inner matches 1.. run function test:nested_loops_inner_control"
    )
    
    ns.function("nested_loops_inner_control",
        "execute if score @s inner matches 1.. run function test:nested_loops_inner_body",
        "execute if score @s inner matches 1.. run function test:nested_loops_inner_control"
    )
    
    ns.function("nested_loops_inner_body",
        "say Inner loop: @s inner",
        "effect give @s minecraft:glowing 1 1",
        "scoreboard players remove @s inner 1"
    )
    
    # Test 7: For loop with complex selector
    ns.function("complex_for",
        "say Testing for loop with complex selector",
        "execute if entity @a[gamemode=survival] run function test:complex_for_control"
    )
    
    ns.function("complex_for_control",
        "execute as @a[gamemode=survival] run function test:complex_for_body"
    )
    
    ns.function("complex_for_body",
        "say Processing survival player: @s",
        "execute if entity @s[nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] run function test:complex_for_sword",
        "execute unless entity @s[nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] run function test:complex_for_no_sword"
    )
    
    ns.function("complex_for_sword",
        "say Player has diamond sword!",
        "effect give @s minecraft:strength 10 1"
    )
    
    ns.function("complex_for_no_sword",
        "say Player has no diamond sword",
        "effect give @s minecraft:haste 5 0"
    )
    
    # Test 8: While loop with scoreboard condition
    ns.function("scoreboard_while",
        "say Testing while loop with scoreboard condition",
        "scoreboard objectives add test_obj dummy",
        "scoreboard players set @s test_obj 10",
        "execute if score @s test_obj matches 5.. run function test:scoreboard_while_control"
    )
    
    ns.function("scoreboard_while_control",
        "execute if score @s test_obj matches 5.. run function test:scoreboard_while_body",
        "execute if score @s test_obj matches 5.. run function test:scoreboard_while_control"
    )
    
    ns.function("scoreboard_while_body",
        "say Score: @s test_obj",
        "scoreboard players remove @s test_obj 1",
        "say Decremented score"
    )
    
    # Hook functions to run
    p.on_tick("test:simple_while")
    p.on_tick("test:entity_while")
    p.on_tick("test:entity_for")
    p.on_tick("test:item_for")
    p.on_tick("test:mixed_control")
    p.on_tick("test:nested_loops")
    p.on_tick("test:complex_for")
    p.on_tick("test:scoreboard_while")
    
    return p

if __name__ == "__main__":
    pack = build_loop_pack()
    print("Loop pack created successfully!")
