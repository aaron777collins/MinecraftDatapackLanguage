#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the parser with a simple length function call
test_code = '''pack "test" description "test" pack_format 82;
namespace "test";

function "demo" {
    var num count = length(items);
}

on_tick "test:demo";
'''

print("Testing parser with:", test_code)
print("=" * 50)

try:
    ast = parse_mdl_js(test_code)
    print("✅ Parser succeeded!")
    print("AST:", ast)
except Exception as e:
    print("❌ Parser failed:", e)
    import traceback
    traceback.print_exc()
