#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from minecraft_datapack_language.cli import _convert_condition_to_minecraft_syntax

# Test the conversion function
test_conditions = [
    "score @s player_level >= 10",
    "score @s experience >= 50",
    "score @s health <= 20",
    "score @s damage > 5",
    "score @s armor < 10",
    "data storage mdl:variables player_class matches 'warrior'"
]

print("Testing condition conversion:")
print("=" * 50)

for condition in test_conditions:
    converted = _convert_condition_to_minecraft_syntax(condition)
    print(f"Original: {condition}")
    print(f"Converted: {converted}")
    print("-" * 30)
