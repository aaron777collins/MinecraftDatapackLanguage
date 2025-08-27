#!/usr/bin/env python3
"""
Python API equivalent of hello_world.mdl
"""
from minecraft_datapack_language import Pack

def create_hello_world_pack():
    pack = Pack(
        name="Hello World",
        description="A simple example datapack",
        pack_format=48
    )
    
    example = pack.namespace("example")
    example.function("hello",
        'say Hello, Minecraft!',
        'tellraw @a {"text":"Welcome to my datapack!","color":"green"}'
    )
    
    pack.on_load("example:hello")
    
    return pack

if __name__ == "__main__":
    pack = create_hello_world_pack()
    pack.build("test_examples/dist")
    print("Hello World pack built successfully!")
