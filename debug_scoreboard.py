#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _generate_scoreboard_objectives
from pathlib import Path

if __name__ == "__main__":
    with open('test_new_pack/test_new_pack.mdl', 'r') as f:
        source = f.read()
    
    ast = parse_mdl_js(source)
    print("AST keys:", list(ast.keys()))
    
    scoreboard_commands = _generate_scoreboard_objectives(ast, Path("."))
    print("Scoreboard commands:", scoreboard_commands)
