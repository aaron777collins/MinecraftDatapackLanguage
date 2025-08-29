#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _generate_scoreboard_objectives, _generate_load_function
from pathlib import Path

if __name__ == "__main__":
    with open('test_new_pack/test_new_pack.mdl', 'r') as f:
        source = f.read()
    
    ast = parse_mdl_js(source)
    print("AST keys:", list(ast.keys()))
    
    # Get namespace
    namespace = ast.get('namespace', {}).get('name', 'mdl') if ast.get('namespace') else 'mdl'
    print("Namespace:", namespace)
    
    scoreboard_commands = _generate_scoreboard_objectives(ast, Path("."))
    print("Scoreboard commands:", scoreboard_commands)
    
    if scoreboard_commands:
        print("Generating load function...")
        _generate_load_function(scoreboard_commands, Path("test_output"), namespace, ast)
        print("Load function generated!")
    else:
        print("No scoreboard commands to generate!")
