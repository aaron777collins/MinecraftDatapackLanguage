#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

# Test the lexer with a simple length function call
test_code = 'var num count = length(items);'

print("Testing lexer with:", test_code)
print("=" * 50)

tokens = lex_mdl_js(test_code)

for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type:15s} = '{token.value}' (line {token.line})")
