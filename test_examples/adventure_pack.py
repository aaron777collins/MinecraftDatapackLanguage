#!/usr/bin/env python3
"""
Python API equivalent of adventure_pack.mdl
"""
from minecraft_datapack_language import Pack

def create_adventure_pack():
    # Create the main pack
    pack = Pack(
        name="Adventure Pack",
        description="A complete adventure experience",
        pack_format=48
    )
    
    # Core system
    core = pack.namespace("core")
    core.function("init",
        'say [core:init] Initializing Adventure Pack...',
        'tellraw @a {"text":"Adventure Pack loaded!","color":"green"}',
        'scoreboard objectives add adventure_points dummy "Adventure Points"'
    )
    
    core.function("tick",
        'say [core:tick] Core systems running...'
    )
    
    # Combat system
    combat = pack.namespace("combat")
    combat.function("weapon_effects",
        'execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run effect give @s minecraft:strength 1 0 true'
    )
    
    combat.function("update_combat",
        'function core:tick',
        'function combat:weapon_effects'
    )
    
    # UI system
    ui = pack.namespace("ui")
    ui.function("hud",
        'title @a actionbar {"text":"Adventure Pack Active","color":"gold"}'
    )
    
    ui.function("update_ui",
        'function ui:hud',
        'function combat:update_combat'
    )
    
    # Lifecycle hooks
    pack.on_load("core:init")
    pack.on_tick("ui:update_ui")
    
    # Function tags
    pack.tag("function", "minecraft:load", values=["core:init"])
    pack.tag("function", "minecraft:tick", values=["ui:update_ui"])
    
    # Data tags
    pack.tag("item", "adventure:weapons", values=[
        "minecraft:diamond_sword",
        "minecraft:netherite_sword"
    ])
    
    pack.tag("item", "adventure:armor", values=[
        "minecraft:diamond_helmet",
        "minecraft:diamond_chestplate",
        "minecraft:diamond_leggings",
        "minecraft:diamond_boots"
    ])
    
    return pack

if __name__ == "__main__":
    pack = create_adventure_pack()
    pack.build("test_examples/dist")
    print("Adventure pack built successfully!")
