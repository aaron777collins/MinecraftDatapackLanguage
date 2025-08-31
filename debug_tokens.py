#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import lex_mdl_js, TokenType

# Test the lexer
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

tokens = lex_mdl_js(source)
print("Tokens:")
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type} = '{token.value}'")
