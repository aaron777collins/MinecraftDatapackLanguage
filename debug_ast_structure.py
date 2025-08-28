#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the AST structure
with open('test_systematic.mdl', 'r') as f:
    src = f.read()

ast = parse_mdl_js(src)

# Find the function and examine its body
print("AST structure:")
print(f"Type: {type(ast)}")
print(f"Keys: {ast.keys() if hasattr(ast, 'keys') else 'No keys'}")

# Examine the AST structure
print("AST structure:")
print(f"Type: {type(ast)}")
print(f"Keys: {ast.keys()}")

# Look at functions
if 'functions' in ast:
    print(f"Functions: {type(ast['functions'])}")
    for func in ast['functions']:
        print(f"  Function: {type(func).__name__}: {func}")
        if hasattr(func, 'name'):
            print(f"    Name: {func.name}")
        if hasattr(func, 'body'):
            for stmt in func.body:
                print(f"    Statement: {type(stmt).__name__}: {stmt}")
                if hasattr(stmt, 'value'):
                    print(f"      Value: {type(stmt.value).__name__}: {stmt.value}")
                    if hasattr(stmt.value, '__class__'):
                        print(f"      Value class: {stmt.value.__class__.__name__}")
                        if hasattr(stmt.value, 'list_name'):
                            print(f"      List name: {stmt.value.list_name}")
                        if hasattr(stmt.value, 'index'):
                            print(f"      Index: {stmt.value.index}")
                        if hasattr(stmt.value, 'left'):
                            print(f"      Left: {stmt.value.left}")
                        if hasattr(stmt.value, 'right'):
                            print(f"      Right: {stmt.value.right}")
                        if hasattr(stmt.value, 'operator'):
                            print(f"      Operator: {stmt.value.operator}")
                print("Function body:")
                for stmt in func.body:
                    print(f"  {type(stmt).__name__}: {stmt}")
                    if hasattr(stmt, 'value'):
                        print(f"    Value: {type(stmt.value).__name__}: {stmt.value}")
                        if hasattr(stmt.value, '__class__'):
                            print(f"    Value class: {stmt.value.__class__.__name__}")
                            if hasattr(stmt.value, 'list_name'):
                                print(f"    List name: {stmt.value.list_name}")
                            if hasattr(stmt.value, 'index'):
                                print(f"    Index: {stmt.value.index}")
                            if hasattr(stmt.value, 'left'):
                                print(f"    Left: {stmt.value.left}")
                            if hasattr(stmt.value, 'right'):
                                print(f"    Right: {stmt.value.right}")
                            if hasattr(stmt.value, 'operator'):
                                print(f"    Operator: {stmt.value.operator}")
                break
