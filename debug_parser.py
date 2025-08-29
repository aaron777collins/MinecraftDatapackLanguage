#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the problematic file
source = '''
pack "test" "Test" 82;
namespace "test";
var num player_level = 15;
function "main" {
    if "$player_level$ >= 20" {
        say "Master level!";
    } else if "$player_level$ >= 15" {
        say "Expert level!";
    } else {
        say "Beginner level!";
    }
}
on_tick "test:main";
'''

try:
    result = parse_mdl_js(source)
    print("Parsing successful!")
except Exception as e:
    print(f"Parsing failed: {e}")
    import traceback
    traceback.print_exc()
