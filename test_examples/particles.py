#!/usr/bin/env python3
"""
Python API equivalent of particles.mdl
"""
from minecraft_datapack_language import Pack

def create_particles_pack():
    pack = Pack(
        name="Particle Effects",
        description="Creates particle effects around players",
        pack_format=48
    )
    
    particles = pack.namespace("particles")
    particles.function("tick",
        'execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1',
        'execute as @a run particle minecraft:firework ~ ~ ~ 0.2 0.2 0.2 0.02 2'
    )
    
    particles.function("init",
        'say Particle effects enabled!'
    )
    
    pack.on_load("particles:init")
    pack.on_tick("particles:tick")
    
    return pack

if __name__ == "__main__":
    pack = create_particles_pack()
    pack.build("test_examples/dist")
    print("Particles pack built successfully!")
