#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the problematic line
test_code = 'function "test1:hello";'

print("Testing parser with:", test_code)
try:
    result = parse_mdl_js(test_code)
    print("Parser succeeded!")
    print("Result:", result)
except Exception as e:
    print("Parser failed with error:", e)
    import traceback
    traceback.print_exc()
