#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js, Command

def test_cli_processing():
    test_input = '''function "test" {
    say Counter: $counter$;
}'''
    
    print("=== CLI Processing Test ===")
    print(f"Input: {test_input}")
    
    # Parse the input
    ast = parse_mdl_js(test_input)
    
    # Check the Command object directly
    for func in ast.get('functions', []):
        print(f"\nFunction: {func}")
        print(f"Function type: {type(func)}")
        
        # Handle both dict and object formats
        if isinstance(func, dict):
            body = func.get('body', [])
        else:
            body = getattr(func, 'body', [])
        
        print(f"Body: {body}")
        print(f"Body type: {type(body)}")
        
        for stmt in body:
            print(f"  Statement: {stmt}")
            print(f"  Statement type: {type(stmt)}")
            if hasattr(stmt, 'command'):
                print(f"  Command attribute: '{stmt.command}'")
                print(f"  Command attribute type: {type(stmt.command)}")
                
                # Check if it's a Command object
                if isinstance(stmt, Command):
                    print(f"  Is Command object: True")
                    print(f"  Command.command: '{stmt.command}'")
                else:
                    print(f"  Is Command object: False")
                    
                # Check the string representation
                print(f"  str(stmt): {str(stmt)}")
                print(f"  repr(stmt): {repr(stmt)}")

if __name__ == "__main__":
    test_cli_processing()
