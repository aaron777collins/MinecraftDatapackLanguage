#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test with control flow lines from the test file
test_source = '''if "entity @s[type=minecraft:player]" {
    say Player detected!;
    effect give @s minecraft:glowing 5 1;
    tellraw @a {"text":"A player is nearby!","color":"green"};
} else if "entity @s[type=minecraft:zombie]" {
    say Zombie detected!;
    effect give @s minecraft:poison 5 1;
    tellraw @a {"text":"A zombie is nearby!","color":"red"};
} else if "entity @s[type=minecraft:creeper]" {
    say Creeper detected!;
    effect give @s minecraft:resistance 5 1;
    tellraw @a {"text":"A creeper is nearby!","color":"dark_red"};
} else {
    say Unknown entity detected;
    tellraw @a {"text":"Something unknown is nearby...","color":"gray"};
}'''

print("Testing token generation for control flow:")
print("=" * 60)

tokens = lex_mdl_js(test_source)
print("Tokens:")
for token in tokens:
    print(f"  {token.type}: '{token.value}'")

print("\nToken analysis completed!")
