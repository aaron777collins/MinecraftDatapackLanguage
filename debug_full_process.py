#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_lexer_js import MDLLexer
from minecraft_datapack_language.mdl_parser_js import MDLParser
from minecraft_datapack_language.cli import _ast_to_commands, _ast_to_pack
from minecraft_datapack_language.pack import Pack

# Test the list variable declaration
test_code = '''// test_simple_lists.mdl - Simple list test
pack "Simple List Test" description "Testing list functionality" pack_format 82;
namespace "test";

// Test list variable declarations
var list items = ["sword", "shield", "potion"];

function "test" {
    say List test;
}'''

print("=== FULL PROCESS DEBUG ===")
try:
    # Step 1: Lexing
    print("1. LEXING:")
    lexer = MDLLexer(test_code)
    tokens = lexer.tokenize()
    print(f"   Generated {len(tokens)} tokens")
    
    # Step 2: Parsing
    print("\n2. PARSING:")
    parser = MDLParser(tokens)
    ast = parser.parse()
    print(f"   AST keys: {list(ast.keys())}")
    print(f"   Functions: {len(ast['functions'])}")
    for func in ast['functions']:
        print(f"     - {func.name}: {len(func.body)} body items")
    
    # Step 3: AST to Commands
    print("\n3. AST TO COMMANDS:")
    for func in ast['functions']:
        print(f"   Function: {func.name}")
        commands = _ast_to_commands(func.body)
        print(f"     Generated {len(commands)} commands:")
        for i, cmd in enumerate(commands):
            print(f"       {i}: {cmd}")
    
    # Step 4: AST to Pack
    print("\n4. AST TO PACK:")
    pack = _ast_to_pack(ast, 82)
    print(f"   Pack name: {pack.name}")
    print(f"   Namespaces: {list(pack.namespaces.keys())}")
    
    for ns_name, ns in pack.namespaces.items():
        print(f"   Namespace {ns_name}:")
        for func_name, func in ns.functions.items():
            print(f"     Function {func_name}: {len(func.commands)} commands")
            for i, cmd in enumerate(func.commands):
                print(f"       {i}: {cmd}")
    
    # Step 5: Build
    print("\n5. BUILD:")
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
