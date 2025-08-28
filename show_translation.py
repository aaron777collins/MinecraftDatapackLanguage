#!/usr/bin/env python3
"""
Demonstrates how MDL variables are translated to Minecraft commands.
"""

def show_variable_translation():
    """Show how MDL variables become Minecraft commands."""
    
    print("=" * 60)
    print("MDL VARIABLE TRANSLATION TO MINECRAFT COMMANDS")
    print("=" * 60)
    
    print("\n1. NUMBER VARIABLES:")
    print("-" * 30)
    print("MDL: var num counter = 5;")
    print("Minecraft:")
    print("  scoreboard objectives add counter dummy")
    print("  scoreboard players set @s counter 5")
    
    print("\n2. STRING VARIABLES:")
    print("-" * 30)
    print("MDL: var str message = \"Hello\";")
    print("Minecraft:")
    print("  data modify entity @s CustomName set value \"Hello\"")
    
    print("\n3. VARIABLE OPERATIONS:")
    print("-" * 30)
    print("MDL: counter = counter + 1;")
    print("Minecraft:")
    print("  scoreboard players add @s counter 1")
    
    print("\n4. CONDITIONALS WITH VARIABLES:")
    print("-" * 30)
    print("MDL: if \"score @s counter matches 10\" {")
    print("       say Counter is 10!;")
    print("     }")
    print("Minecraft:")
    print("  execute if score @s counter matches 10 run say Counter is 10!")
    
    print("\n5. LOOPS WITH VARIABLES:")
    print("-" * 30)
    print("MDL: while \"score @s counter matches 1..\" {")
    print("        say Counter: @s counter;")
    print("        counter = counter - 1;")
    print("      }")
    print("Minecraft:")
    print("  execute if score @s counter matches 1.. run function example:loop_body")
    print("  execute if score @s counter matches 1.. run function example:loop_control")
    
    print("\n6. GLOBAL vs LOCAL VARIABLES:")
    print("-" * 30)
    print("MDL Global: var num global_var = 100;")
    print("MDL Local:  var num local_var = 50;")
    print("Minecraft (both use scoreboards):")
    print("  scoreboard objectives add global_var dummy")
    print("  scoreboard objectives add local_var dummy")
    print("  scoreboard players set @s global_var 100")
    print("  scoreboard players set @s local_var 50")
    
    print("\n7. LIST VARIABLES:")
    print("-" * 30)
    print("MDL: var list items = [\"sword\", \"shield\"];")
    print("Minecraft (multiple scoreboards):")
    print("  scoreboard objectives add items_0 dummy")
    print("  scoreboard objectives add items_1 dummy")
    print("  scoreboard players set @s items_0 1  # 1 = sword")
    print("  scoreboard players set @s items_1 2  # 2 = shield")
    
    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("=" * 60)
    print("[+] Variables are NOT stored in Python memory")
print("[+] They become Minecraft scoreboard objectives")
print("[+] Strings become NBT data on entities")
print("[+] Lists become multiple scoreboard objectives")
print("[+] Scope is handled by function boundaries")
print("[+] No garbage collection needed - Minecraft handles it")
print("[+] Data persists between function calls")
print("[+] All operations become Minecraft commands")

if __name__ == "__main__":
    show_variable_translation()
