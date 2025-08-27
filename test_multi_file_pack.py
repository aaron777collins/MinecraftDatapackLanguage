#!/usr/bin/env python3
"""
Test script to demonstrate pack declaration behavior in multi-file MDL.
"""

import os
import tempfile
from minecraft_datapack_language.cli import _gather_mdl_files, _parse_many

def create_test_files():
    """Create test files to demonstrate pack declaration behavior."""
    
    temp_dir = tempfile.mkdtemp(prefix="mdl_test_")
    print(f"Creating test files in: {temp_dir}")
    
    # File 1: Has pack declaration
    file1 = '''# main.mdl - Has pack declaration
pack "Test Pack" description "Testing multi-file behavior" pack_format 48

namespace "main"

function "hello":
    say Hello from main!
'''
    
    # File 2: No pack declaration
    file2 = '''# utils.mdl - No pack declaration
namespace "utils"

function "helper":
    say Hello from utils!
'''
    
    # File 3: Has pack declaration (should cause error)
    file3 = '''# conflict.mdl - Has pack declaration (should cause error)
pack "Conflict Pack" description "This should cause an error" pack_format 48

namespace "conflict"

function "test":
    say This should not work!
'''
    
    # Write files
    files = {
        "main.mdl": file1,
        "utils.mdl": file2,
        "conflict.mdl": file3
    }
    
    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"  Created: {filename}")
    
    return temp_dir

def test_scenarios():
    """Test different scenarios with pack declarations."""
    
    temp_dir = create_test_files()
    
    print("\n=== Testing Multi-File Pack Declaration Behavior ===\n")
    
    # Scenario 1: Valid multi-file (first has pack, others don't)
    print("Scenario 1: Valid multi-file (main.mdl + utils.mdl)")
    print("Expected: Success - main.mdl provides pack, utils.mdl merges in")
    try:
        files = [os.path.join(temp_dir, "main.mdl"), os.path.join(temp_dir, "utils.mdl")]
        pack = _parse_many(files, default_pack_format=48, verbose=True)
        print(f"✅ SUCCESS: Pack name = '{pack.name}', Format = {pack.pack_format}")
        print(f"   Namespaces: {list(pack.namespaces.keys())}")
        print()
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print()
    
    # Scenario 2: Invalid multi-file (both have pack declarations)
    print("Scenario 2: Invalid multi-file (main.mdl + conflict.mdl)")
    print("Expected: Error - duplicate pack declaration")
    try:
        files = [os.path.join(temp_dir, "main.mdl"), os.path.join(temp_dir, "conflict.mdl")]
        pack = _parse_many(files, default_pack_format=48, verbose=True)
        print(f"❌ UNEXPECTED SUCCESS: {pack.name}")
    except Exception as e:
        print(f"✅ EXPECTED ERROR: {e}")
        print()
    
    # Scenario 3: No pack declaration in any file
    print("Scenario 3: No pack declaration (utils.mdl only)")
    print("Expected: Error - missing pack declaration")
    try:
        files = [os.path.join(temp_dir, "utils.mdl")]
        pack = _parse_many(files, default_pack_format=48, verbose=True)
        print(f"❌ UNEXPECTED SUCCESS: {pack.name}")
    except Exception as e:
        print(f"✅ EXPECTED ERROR: {e}")
        print()
    
    # Scenario 4: Multiple files without pack, but with default
    print("Scenario 4: Multiple files without pack, using default")
    print("Expected: Success - uses default pack format and generated name")
    try:
        files = [os.path.join(temp_dir, "utils.mdl")]
        pack = _parse_many(files, default_pack_format=48, verbose=True)
        print(f"✅ SUCCESS: Pack name = '{pack.name}', Format = {pack.pack_format}")
        print()
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print()

if __name__ == "__main__":
    test_scenarios()
