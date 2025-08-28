#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js
from minecraft_datapack_language.cli import _ast_to_pack

# Exactly the same code as debug_simple.mdl
code = '''// debug_simple.mdl - Very simple test
pack "debug" description "Debug" pack_format 82;

namespace "test";

function "simple" {
    var num counter = 5;
}
'''

print("=== LEXING ===")
tokens = lex_mdl_js(code)

print("\n=== PARSING ===")
parser = MDLParser(tokens)
ast = parser.parse()

print("\n=== PACK GENERATION (CLI-style) ===")
pack = _ast_to_pack(ast, 82)

# Debug the pack contents
for ns_name, ns in pack.namespaces.items():
    print(f"\nNamespace: {ns_name}")
    for func_name, func in ns.functions.items():
        print(f"  Function: {func_name}")
        print(f"  Commands: {len(func.commands)}")
        for i, cmd in enumerate(func.commands):
            print(f"    [{i}] {cmd}")

print("\n=== BUILDING ===")
pack.build("debug_cli_output")

print("\n=== CHECKING OUTPUT ===")
import os
file_path = "debug_cli_output/data/test/function/simple.mcfunction"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    print(f"File content: {repr(content)}")
else:
    print(f"File not found: {file_path}")
