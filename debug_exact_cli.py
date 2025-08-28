#!/usr/bin/env python3

import sys
sys.path.append('.')

from minecraft_datapack_language.cli import _gather_mdl_files, _parse_many

# Exactly replicate the CLI build process
file_path = "debug_simple.mdl"

print("=== GATHERING FILES ===")
files = _gather_mdl_files(file_path)
print(f"Files: {files}")

print("\n=== PARSING FILES ===")
pack = _parse_many(files, default_pack_format=82, verbose=True)

print("\n=== PACK CONTENTS ===")
for ns_name, ns in pack.namespaces.items():
    print(f"Namespace: {ns_name}")
    for func_name, func in ns.functions.items():
        print(f"  Function: {func_name}")
        print(f"  Commands: {len(func.commands)}")
        for i, cmd in enumerate(func.commands):
            print(f"    [{i}] {cmd}")

print("\n=== BUILDING ===")
pack.build("debug_exact_output")

print("\n=== CHECKING OUTPUT ===")
import os
file_path = "debug_exact_output/data/test/function/simple.mcfunction"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    print(f"File content: {repr(content)}")
else:
    print(f"File not found: {file_path}")
