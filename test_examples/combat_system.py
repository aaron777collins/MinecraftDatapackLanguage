#!/usr/bin/env python3
"""
Python API equivalent of combat_system.mdl
"""
from minecraft_datapack_language import Pack

def create_combat_system_pack():
    pack = Pack(
        name="Combat System",
        description="Enhanced combat mechanics",
        pack_format=48
    )
    
    combat = pack.namespace("combat")
    
    # Weapon effects
    combat.function("weapon_effects",
        '# Diamond sword gives strength',
        'execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run effect give @s minecraft:strength 1 0 true',
        '',
        '# Golden sword gives speed',
        'execute as @a[nbt={SelectedItem:{id:"minecraft:golden_sword"}}] run effect give @s minecraft:speed 1 0 true',
        '',
        '# Netherite sword gives fire resistance',
        'execute as @a[nbt={SelectedItem:{id:"minecraft:netherite_sword"}}] run effect give @s minecraft:fire_resistance 1 0 true'
    )
    
    # Armor effects
    combat.function("armor_effects",
        '# Diamond armor gives resistance',
        'execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] run effect give @s minecraft:resistance 1 0 true',
        '',
        '# Netherite armor gives fire resistance',
        'execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:netherite_helmet"}]}] run effect give @s minecraft:fire_resistance 1 0 true'
    )
    
    combat.function("update_combat",
        'function combat:weapon_effects',
        'function combat:armor_effects'
    )
    
    pack.on_tick("combat:update_combat")
    
    return pack

if __name__ == "__main__":
    pack = create_combat_system_pack()
    pack.build("test_examples/dist")
    print("Combat system pack built successfully!")
