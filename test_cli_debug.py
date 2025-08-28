#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.cli import _ast_to_pack

# Test the list variable declaration
test_code = '''// test_simple_lists.mdl - Simple list test
pack "Simple List Test" description "Testing list functionality" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];

function "test" {
    say List test;
}'''

print("=== CLI DEBUG ===")
try:
    # Step 1: Parse with parse_mdl_js (exactly what CLI does)
    print("1. PARSING with parse_mdl_js:")
    ast = parse_mdl_js(test_code)
    print(f"   AST keys: {list(ast.keys())}")
    print(f"   Functions: {len(ast['functions'])}")
    for func in ast['functions']:
        print(f"     - {func.name}: {len(func.body)} body items")
        for item in func.body:
            print(f"       * {type(item).__name__}: {item}")
    
    # Step 2: Convert AST to Pack (exactly what CLI does)
    print("\n2. AST TO PACK:")
    pack = _ast_to_pack(ast, 82)
    print(f"   Pack name: {pack.name}")
    print(f"   Namespaces: {list(pack.namespaces.keys())}")
    
    for ns_name, ns in pack.namespaces.items():
        print(f"   Namespace {ns_name}:")
        for func_name, func in ns.functions.items():
            print(f"     Function {func_name}: {len(func.commands)} commands")
            for i, cmd in enumerate(func.commands):
                print(f"       {i}: {cmd}")
    
    # Step 3: Build
    print("\n3. BUILD:")
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        pack.build(temp_dir)
        print(f"   Built to: {temp_dir}")
        
        # Check the generated files
        import glob
        mcfunction_files = glob.glob(f"{temp_dir}/**/*.mcfunction", recursive=True)
        for file_path in mcfunction_files:
            rel_path = os.path.relpath(file_path, temp_dir)
            print(f"   File: {rel_path}")
            with open(file_path, 'r') as f:
                content = f.read()
                print(f"     Content: {repr(content)}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
