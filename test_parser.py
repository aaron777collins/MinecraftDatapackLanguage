#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the parser
source = '''
function "test" {
    give @s minecraft:iron_ingot 1;
}
'''

ast = parse_mdl_js(source)
print("AST:")
print(ast)
