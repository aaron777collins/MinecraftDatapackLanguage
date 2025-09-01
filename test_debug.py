#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _process_statement

# Test the full pipeline
source = '''
function "test" {
    give @s minecraft:iron_ingot 1;
}
'''

ast = parse_mdl_js(source)
print("AST command:", ast['functions'][0]['body'][0].command)

# Test the statement processing
statement = ast['functions'][0]['body'][0]
commands = _process_statement(statement, "test", "test", 0, False, "@s")
print("Processed commands:", commands)
