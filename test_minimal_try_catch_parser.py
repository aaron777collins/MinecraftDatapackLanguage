#!/usr/bin/env python3
"""
Test script for minimal try-catch MDL file.
"""

import sys
import os

# Add the current directory to the path so we can import the MDL modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Read the minimal try-catch MDL file
with open('test_minimal_try_catch.mdl', 'r') as f:
    minimal_mdl = f.read()

print("Testing minimal try-catch MDL file parsing:")
print("=" * 50)
print(minimal_mdl)
print("=" * 50)

try:
    ast = parse_mdl_js(minimal_mdl)
    print("[+] Parsing successful!")
    print(f"Pack: {ast['pack']}")
    print(f"Namespaces: {len(ast['namespaces'])}")
    print(f"Functions: {len(ast['functions'])}")
    
    if ast['functions']:
        func = ast['functions'][0]
        print(f"Function name: {func.name}")
        print(f"Function body statements: {len(func.body)}")
        
        # Check for try-catch statement
        try_catch_found = False
        for stmt in func.body:
            if hasattr(stmt, '__class__') and 'TryCatchStatement' in str(stmt.__class__):
                try_catch_found = True
                print(f"[+] Try-catch statement found!")
                print(f"  Try body statements: {len(stmt.try_body)}")
                print(f"  Catch body statements: {len(stmt.catch_body)}")
                print(f"  Error variable: {stmt.error_variable}")
                break
        
        if not try_catch_found:
            print("[-] No try-catch statement found in function body")
            for i, stmt in enumerate(func.body):
                print(f"  Statement {i}: {type(stmt)}")
    
except Exception as e:
    print(f"[-] Parsing failed: {e}")
    import traceback
    traceback.print_exc()
