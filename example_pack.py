
from minecraft_datapack_language import Pack

def create_pack():
    p = Pack("Minecraft Datapack Language", description="MDL Example", pack_format=48)
    ns = p.namespace("example")
    ns.function("hello",
        'say Hello from MDL Python!',
        'tellraw @a {"text":"MDL tick","color":"yellow"}'
    )
    p.on_tick("example:hello")
    p.on_load("example:hello")
    # Tag demo
    p.tag("function", "minecraft:tick", values=["example:hello"])
    p.tag("item", "minecraft:swords", values=["minecraft:diamond_sword"], replace=False)
    return p
