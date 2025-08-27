#!/usr/bin/env python3
"""
Example demonstrating multi-file MDL support.

This script shows how to:
1. Create multiple MDL files programmatically
2. Build a datapack from multiple files
3. Use the CLI to process multiple files
"""

import os
import tempfile
import subprocess
from minecraft_datapack_language import Pack

def create_sample_files():
    """Create sample MDL files to demonstrate multi-file support."""
    
    # Create a temporary directory for our example
    temp_dir = tempfile.mkdtemp(prefix="mdl_multi_")
    print(f"Creating sample files in: {temp_dir}")
    
    # File 1: Core functionality
    core_mdl = '''# core.mdl - Main pack and core functions
pack "Multi-File Example" description "Demonstrating multi-file MDL support" pack_format 48

namespace "core"

function "init":
    say [core:init] Initializing core systems...
    tellraw @a {"text":"Core systems ready","color":"green"}

function "tick":
    say [core:tick] Core tick running...
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

# Hook into vanilla lifecycle
on_load "core:init"
on_tick "core:tick"
'''
    
    # File 2: Combat system
    combat_mdl = '''# combat.mdl - Combat-related functions
namespace "combat"

function "weapon_effects":
    say [combat:weapon_effects] Applying weapon effects...
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run effect give @s minecraft:strength 1 0 true

function "armor_bonus":
    say [combat:armor_bonus] Checking armor bonuses...
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] run effect give @s minecraft:resistance 1 0 true

# Call core functions
function "update":
    function core:tick
    function combat:weapon_effects
    function combat:armor_bonus
'''
    
    # File 3: UI system
    ui_mdl = '''# ui.mdl - User interface functions
namespace "ui"

function "show_hud":
    say [ui:show_hud] Updating HUD...
    title @a actionbar {"text":"Multi-File MDL Demo","color":"gold"}

function "show_stats":
    say [ui:show_stats] Displaying player stats...
    execute as @a run tellraw @s {"text":"Health: ","color":"red","extra":[{"score":{"name":"@s","objective":"health"}}]}

# Integrate with combat system
function "update_ui":
    function ui:show_hud
    function ui:show_stats
    function combat:update
'''
    
    # File 4: Data definitions
    data_mdl = '''# data.mdl - Recipes and other data
namespace "data"

# Custom recipe for a special item
recipe "special_sword":
    {
        "type": "minecraft:crafting",
        "pattern": [
            " D ",
            " D ",
            " S "
        ],
        "key": {
            "D": {"item": "minecraft:diamond"},
            "S": {"item": "minecraft:stick"}
        },
        "result": {
            "item": "minecraft:diamond_sword",
            "count": 1
        }
    }

# Function tag to run UI updates
tag function "minecraft:tick":
    add "ui:update_ui"
'''
    
    # Write the files
    files = {
        "core.mdl": core_mdl,
        "combat.mdl": combat_mdl,
        "ui.mdl": ui_mdl,
        "data.mdl": data_mdl
    }
    
    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"  Created: {filename}")
    
    return temp_dir

def build_with_cli(mdl_dir, output_dir):
    """Build the datapack using the CLI."""
    print(f"\nBuilding datapack from {mdl_dir}...")
    
    # Use the CLI to build
    cmd = [
        "python", "-m", "minecraft_datapack_language.cli", "build",
        "--mdl", mdl_dir,
        "-o", output_dir,
        "--wrapper", "multi_file_demo",
        "--verbose"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("CLI Output:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"CLI Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def build_programmatically(mdl_dir, output_dir):
    """Build the datapack programmatically."""
    print(f"\nBuilding datapack programmatically from {mdl_dir}...")
    
    from minecraft_datapack_language.cli import _gather_mdl_files, _parse_many
    
    # Gather all MDL files
    files = _gather_mdl_files(mdl_dir)
    print(f"Found {len(files)} MDL files: {[os.path.basename(f) for f in files]}")
    
    # Parse and merge all files
    pack = _parse_many(files, default_pack_format=48, verbose=True)
    
    # Build the datapack
    wrapped_dir = os.path.join(output_dir, "multi_file_demo_prog")
    pack.build(wrapped_dir)
    
    print(f"Built datapack at: {wrapped_dir}")
    return wrapped_dir

def main():
    """Main demonstration function."""
    print("=== Multi-File MDL Support Demo ===\n")
    
    # Create sample files
    mdl_dir = create_sample_files()
    
    # Create output directory
    output_dir = os.path.join(os.getcwd(), "dist")
    os.makedirs(output_dir, exist_ok=True)
    
    # Method 1: Build using CLI
    print("\n--- Method 1: CLI Build ---")
    success = build_with_cli(mdl_dir, output_dir)
    
    # Method 2: Build programmatically
    print("\n--- Method 2: Programmatic Build ---")
    prog_output = build_programmatically(mdl_dir, output_dir)
    
    print(f"\n=== Demo Complete ===")
    print(f"Sample files created in: {mdl_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Programmatic output: {prog_output}")
    
    if success:
        print("\nBoth methods completed successfully!")
        print("You can now test the datapack in Minecraft.")
    else:
        print("\nCLI method failed, but programmatic method succeeded.")

if __name__ == "__main__":
    main()
