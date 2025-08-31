#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the parser
source = '''
pack "Debug" "Debug namespace tracking" 82;

namespace "first";

recipe "first_recipe" "recipes/first.json";

function "first_func" {
    say First namespace function;
}

namespace "second";

recipe "second_recipe" "recipes/second.json";

function "second_func" {
    say Second namespace function;
}

on_load "first:first_func";
'''

ast = parse_mdl_js(source)
print("AST:")
print(f"Namespace: {ast.get('namespace')}")
print(f"Recipes: {ast.get('recipes')}")
print(f"Functions: {[f['name'] for f in ast.get('functions', [])]}")
