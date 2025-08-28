#!/usr/bin/env python3
import sys
sys.path.append('.')
from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

code = '''
pack "test" description "Test" pack_format 82;
namespace "test";

var list items = ["apple", "banana", "cherry"];
var num index = 0;
var str item = items[index];
'''

print("=== PARSING ===")
tokens = lex_mdl_js(code)
parser = MDLParser(tokens)
ast = parser.parse()

for func in ast.get('functions', []):
    print(f"\nFunction: {func.name}")
    for i, stmt in enumerate(func.body):
        print(f"  [{i}] {stmt.__class__.__name__}: {stmt}")
        if hasattr(stmt, 'value') and stmt.value:
            print(f"      value: {stmt.value}")
            print(f"      value type: {type(stmt.value)}")
            print(f"      value class: {stmt.value.__class__.__name__}")
            if hasattr(stmt.value, 'list_name'):
                print(f"      list_name: {stmt.value.list_name}")
            if hasattr(stmt.value, 'index'):
                print(f"      index: {stmt.value.index}")
                print(f"      index class: {stmt.value.index.__class__.__name__}")
