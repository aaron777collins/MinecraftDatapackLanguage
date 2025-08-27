#!/usr/bin/env python3
"""
Python API test for conditional functionality.
This demonstrates how to achieve the same conditional logic using the Python API.
"""

from minecraft_datapack_language import Pack

def build_conditional_pack():
    """Build a pack with conditional logic using the Python API"""
    
    # Create the pack
    p = Pack(
        name="Conditional Tests Python",
        description="Python API tests for conditional functionality",
        pack_format=48
    )
    
    # Create namespace
    ns = p.namespace("test")
    
    # Test 1: Simple if statement (using execute commands)
    ns.function("simple_if", 
        "say Testing simple if statement",
        "execute if entity @s[type=minecraft:player] run function test:simple_if_player"
    )
    
    ns.function("simple_if_player",
        "say Player detected!",
        "effect give @s minecraft:glowing 5 1"
    )
    
    # Test 2: if/else statement
    ns.function("if_else",
        "say Testing if/else statement",
        "execute if entity @s[type=minecraft:player] run function test:if_else_player",
        "execute unless entity @s[type=minecraft:player] run function test:if_else_else"
    )
    
    ns.function("if_else_player",
        "say Player detected!",
        "effect give @s minecraft:glowing 5 1"
    )
    
    ns.function("if_else_else",
        "say No player found",
        "say This is the else block"
    )
    
    # Test 3: if/else if/else statement
    ns.function("if_else_if_else",
        "say Testing if/else if/else statement",
        "execute if entity @s[type=minecraft:player] run function test:if_else_if_else_player",
        "execute unless entity @s[type=minecraft:player] if entity @s[type=minecraft:zombie] run function test:if_else_if_else_zombie",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] if entity @s[type=minecraft:creeper] run function test:if_else_if_else_creeper",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] unless entity @s[type=minecraft:creeper] run function test:if_else_if_else_else"
    )
    
    ns.function("if_else_if_else_player",
        "say Player detected!",
        "effect give @s minecraft:glowing 5 1"
    )
    
    ns.function("if_else_if_else_zombie",
        "say Zombie detected!",
        "effect give @s minecraft:poison 5 1"
    )
    
    ns.function("if_else_if_else_creeper",
        "say Creeper detected!",
        "effect give @s minecraft:resistance 5 1"
    )
    
    ns.function("if_else_if_else_else",
        "say Unknown entity",
        "say This is the final else block"
    )
    
    # Test 4: Complex conditions with NBT
    ns.function("complex_conditions",
        "say Testing complex conditions",
        "execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] run function test:complex_conditions_diamond",
        "execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] if entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}] run function test:complex_conditions_golden",
        "execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}] if entity @s[type=minecraft:player] run function test:complex_conditions_player",
        "execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}] unless entity @s[type=minecraft:player] run function test:complex_conditions_else"
    )
    
    ns.function("complex_conditions_diamond",
        "say Player with diamond sword!",
        "effect give @s minecraft:strength 10 1"
    )
    
    ns.function("complex_conditions_golden",
        "say Player with golden sword!",
        "effect give @s minecraft:speed 10 1"
    )
    
    ns.function("complex_conditions_player",
        "say Player without special sword",
        "effect give @s minecraft:haste 5 0"
    )
    
    ns.function("complex_conditions_else",
        "say No player found"
    )
    
    # Test 5: Mixed commands with conditionals
    ns.function("mixed_commands",
        "say Testing mixed commands with conditionals",
        "say This is before the conditional",
        "execute if entity @s[type=minecraft:player] run function test:mixed_commands_if",
        "say This is after the conditional",
        "say Another command after"
    )
    
    ns.function("mixed_commands_if",
        "say Inside if block",
        "effect give @s minecraft:glowing 5 1"
    )
    
    # Test 6: Multiple else if blocks
    ns.function("multiple_else_if",
        "say Testing multiple else if blocks",
        "execute if entity @s[type=minecraft:player] run function test:multiple_else_if_player",
        "execute unless entity @s[type=minecraft:player] if entity @s[type=minecraft:zombie] run function test:multiple_else_if_zombie",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] if entity @s[type=minecraft:skeleton] run function test:multiple_else_if_skeleton",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] unless entity @s[type=minecraft:skeleton] if entity @s[type=minecraft:creeper] run function test:multiple_else_if_creeper",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] unless entity @s[type=minecraft:skeleton] unless entity @s[type=minecraft:creeper] if entity @s[type=minecraft:spider] run function test:multiple_else_if_spider",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] unless entity @s[type=minecraft:skeleton] unless entity @s[type=minecraft:creeper] unless entity @s[type=minecraft:spider] run function test:multiple_else_if_else"
    )
    
    ns.function("multiple_else_if_player", "say Player")
    ns.function("multiple_else_if_zombie", "say Zombie")
    ns.function("multiple_else_if_skeleton", "say Skeleton")
    ns.function("multiple_else_if_creeper", "say Creeper")
    ns.function("multiple_else_if_spider", "say Spider")
    ns.function("multiple_else_if_else", "say Unknown entity")
    
    # Test 7: Conditional with function calls
    ns.function("conditional_with_calls",
        "say Testing conditionals with function calls",
        "execute if entity @s[type=minecraft:player] run function test:conditional_with_calls_player",
        "execute unless entity @s[type=minecraft:player] if entity @s[type=minecraft:zombie] run function test:conditional_with_calls_zombie",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] run function test:conditional_with_calls_default"
    )
    
    ns.function("conditional_with_calls_player",
        "say Calling player function",
        "function test:player_effects"
    )
    
    ns.function("conditional_with_calls_zombie",
        "say Calling zombie function",
        "function test:zombie_effects"
    )
    
    ns.function("conditional_with_calls_default",
        "say Calling default function",
        "function test:default_effects"
    )
    
    # Helper functions
    ns.function("player_effects",
        "say Applying player effects",
        "effect give @s minecraft:night_vision 10 0"
    )
    
    ns.function("zombie_effects",
        "say Applying zombie effects",
        "effect give @s minecraft:poison 5 1"
    )
    
    ns.function("default_effects",
        "say Applying default effects",
        "effect give @s minecraft:glowing 5 0"
    )
    
    # Hook into tick for testing
    p.on_tick("test:simple_if")
    
    return p

if __name__ == "__main__":
    # Build the pack
    pack = build_conditional_pack()
    
    # Print some info
    print("Built conditional pack with Python API")
    print(f"Pack name: {pack.name}")
    print(f"Number of namespaces: {len(pack.namespaces)}")
    
    # Show functions in test namespace
    test_ns = pack.namespaces.get("test")
    if test_ns:
        print(f"Number of functions in test namespace: {len(test_ns.functions)}")
        print("Functions:")
        for func_name in sorted(test_ns.functions.keys()):
            print(f"  - {func_name}")
    
    print("\nPython API conditional test completed successfully!")
