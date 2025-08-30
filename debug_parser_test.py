#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

def test_parser():
    test_cases = [
        '''function "test" {
    say Counter: $counter$;
}''',
        '''function "test" {
    say "Counter: $counter$";
}''',
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Input: {test_case}")
        
        try:
            ast = parse_mdl_js(test_case)
            print("AST:")
            print(f"  Functions: {len(ast.get('functions', []))}")
            for func in ast.get('functions', []):
                print(f"    Function: {func}")
                if hasattr(func, 'body'):
                    for stmt in func.body:
                        print(f"      Statement: {stmt}")
                        if hasattr(stmt, 'command'):
                            print(f"        Command: '{stmt.command}'")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_parser()
