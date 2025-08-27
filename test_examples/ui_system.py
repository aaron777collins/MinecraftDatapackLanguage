#!/usr/bin/env python3
"""
Python API equivalent of ui_system.mdl
"""
from minecraft_datapack_language import Pack

def create_ui_system_pack():
    pack = Pack(
        name="UI System",
        description="Custom HUD and UI elements",
        pack_format=48
    )
    
    ui = pack.namespace("ui")
    
    # HUD function
    ui.function("hud",
        '# Show current health',
        'execute as @a run title @s actionbar {"text":"Health: ","color":"red","extra":[{"score":{"name":"@s","objective":"health"}}]}',
        '',
        '# Show current food level',
        'execute as @a run title @s actionbar {"text":"Food: ","color":"yellow","extra":[{"score":{"name":"@s","objective":"food"}}]}'
    )
    
    # Welcome message
    ui.function("welcome_message",
        'tellraw @a {"text":"Welcome to the server!","color":"gold","bold":true}',
        'tellraw @a {"text":"Use /help for commands","color":"gray","italic":true}'
    )
    
    ui.function("update_ui",
        'function ui:hud'
    )
    
    pack.on_load("ui:welcome_message")
    pack.on_tick("ui:update_ui")
    
    return pack

if __name__ == "__main__":
    pack = create_ui_system_pack()
    pack.build("test_examples/dist")
    print("UI system pack built successfully!")
