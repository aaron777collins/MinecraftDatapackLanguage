#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.pack import Pack, Function

# Create a pack and function with the expected commands
pack = Pack("debug_test", "Debug Test", 82)
ns = pack.namespace("test")

# Create a function with our expected commands
func = Function("simple", [
    "scoreboard objectives add counter dummy",
    "scoreboard players set @s counter 5"
])

# Add the function to the namespace
ns.functions["simple"] = func

print("=== BEFORE WRITING ===")
print(f"Function commands: {func.commands}")
print(f"Commands joined: '{chr(10).join(func.commands)}'")

# Monkey patch write_text to see what it's receiving
from minecraft_datapack_language import utils
original_write_text = utils.write_text

def debug_write_text(path, text):
    print(f"DEBUG: write_text called with path='{path}', text='{text}'")
    print(f"DEBUG: text repr: {repr(text)}")
    return original_write_text(path, text)

utils.write_text = debug_write_text

# Write the pack
pack.build("debug_output")

print("=== AFTER WRITING ===")

# Read back the written file
import os
file_path = "debug_output/data/test/function/simple.mcfunction"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    print(f"File content: {repr(content)}")
else:
    print(f"File not found: {file_path}")
