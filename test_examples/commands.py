#!/usr/bin/env python3
"""
Python API equivalent of commands.mdl
"""
from minecraft_datapack_language import Pack

def create_commands_pack():
    pack = Pack(
        name="Custom Commands",
        description="Adds useful commands for players",
        pack_format=48
    )
    
    commands = pack.namespace("commands")
    commands.function("heal",
        'effect give @s minecraft:instant_health 1 1',
        'effect give @s minecraft:regeneration 5 1',
        'tellraw @s {"text":"You have been healed!","color":"green"}'
    )
    
    commands.function("feed",
        'effect give @s minecraft:saturation 1 5',
        'tellraw @s {"text":"You are no longer hungry!","color":"yellow"}'
    )
    
    commands.function("fly",
        'effect give @s minecraft:levitation 10 1',
        'tellraw @s {"text":"You can now fly!","color":"aqua"}'
    )
    
    # Make functions available as commands
    pack.tag("function", "minecraft:load", values=[
        "commands:heal",
        "commands:feed", 
        "commands:fly"
    ])
    
    return pack

if __name__ == "__main__":
    pack = create_commands_pack()
    pack.build("test_examples/dist")
    print("Commands pack built successfully!")
