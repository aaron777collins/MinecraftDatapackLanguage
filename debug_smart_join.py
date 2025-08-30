#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the function directly
from minecraft_datapack_language.mdl_parser_js import _smart_join_command_parts

def test_smart_join():
    test_cases = [
        ['say', 'Counter:', '$counter$'],
        ['say', 'Counter:', '$counter$', ';'],
        ['say', '"Counter:', '$counter$', '"'],
    ]
    
    for i, parts in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Input parts: {parts}")
        result = _smart_join_command_parts(parts)
        print(f"Result: '{result}'")

if __name__ == "__main__":
    test_smart_join()
