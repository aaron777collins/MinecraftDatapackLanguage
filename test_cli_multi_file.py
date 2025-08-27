#!/usr/bin/env python3
"""
Test script to actually test CLI multi-file functionality.
"""

import os
import tempfile
import subprocess
import sys
import shutil

def create_test_files():
    """Create test files to test CLI multi-file functionality."""
    
    temp_dir = tempfile.mkdtemp(prefix="mdl_cli_test_")
    print(f"Creating test files in: {temp_dir}")
    
    # Create main directory
    main_dir = os.path.join(temp_dir, "main_project")
    os.makedirs(main_dir, exist_ok=True)
    
    # File 1: Has pack declaration
    file1 = '''# main.mdl - Has pack declaration
pack "Test Pack" description "Testing CLI multi-file behavior" pack_format 48

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
    
    # Write files to main directory
    files = {
        "main.mdl": file1,
        "utils.mdl": file2,
    }
    
    for filename, content in files.items():
        filepath = os.path.join(main_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"  Created: {filename}")
    
    # Create conflict directory
    conflict_dir = os.path.join(temp_dir, "conflict_project")
    os.makedirs(conflict_dir, exist_ok=True)
    
    # File 3: Has pack declaration (should cause error)
    file3 = '''# conflict.mdl - Has pack declaration (should cause error)
pack "Conflict Pack" description "This should cause an error" pack_format 48

namespace "conflict"

function "test":
    say This should not work!
'''
    
    # File 4: Another pack declaration
    file4 = '''# another.mdl - Another pack declaration
pack "Another Pack" description "This should also cause an error" pack_format 48

namespace "another"

function "test":
    say This should not work either!
'''
    
    conflict_files = {
        "conflict.mdl": file3,
        "another.mdl": file4,
    }
    
    for filename, content in conflict_files.items():
        filepath = os.path.join(conflict_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"  Created: {filename}")
    
    return temp_dir, main_dir, conflict_dir

def run_mdl_command(args):
    """Run mdl command and return result."""
    cmd = ["mdl"] + args
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        print(f"✅ SUCCESS")
        print(f"STDOUT: {result.stdout}")
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED (exit code: {e.returncode})")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False, e.stdout, e.stderr

def test_scenarios():
    """Test different CLI scenarios."""
    
    temp_dir, main_dir, conflict_dir = create_test_files()
    
    print("\n=== Testing CLI Multi-File Functionality ===\n")
    
    # Scenario 1: Check single file with pack declaration
    print("Scenario 1: Check single file with pack declaration")
    main_file = os.path.join(main_dir, "main.mdl")
    print(f"Checking file: {main_file}")
    print(f"File exists: {os.path.exists(main_file)}")
    success, stdout, stderr = run_mdl_command(["check", main_file])
    print()
    
    # Scenario 2: Check single file without pack declaration
    print("Scenario 2: Check single file without pack declaration")
    success, stdout, stderr = run_mdl_command(["check", os.path.join(main_dir, "utils.mdl")])
    print()
    
    # Scenario 3: Check directory with multiple files (should work)
    print("Scenario 3: Check directory with multiple files (main.mdl + utils.mdl)")
    success, stdout, stderr = run_mdl_command(["check", main_dir])
    print()
    
    # Scenario 4: Check directory with conflicting pack declarations (should fail)
    print("Scenario 4: Check directory with conflicting pack declarations")
    success, stdout, stderr = run_mdl_command(["check", conflict_dir])
    print()
    
    # Scenario 5: Build directory with multiple files (should work)
    print("Scenario 5: Build directory with multiple files")
    build_dir = os.path.join(temp_dir, "build_output")
    success, stdout, stderr = run_mdl_command(["build", "--mdl", main_dir, "-o", build_dir, "--verbose"])
    print()
    
    # Scenario 6: Build specific files (should work)
    print("Scenario 6: Build specific files")
    specific_files = f"{os.path.join(main_dir, 'main.mdl')} {os.path.join(main_dir, 'utils.mdl')}"
    success, stdout, stderr = run_mdl_command(["build", "--mdl", specific_files, "-o", build_dir, "--verbose"])
    print()

if __name__ == "__main__":
    test_scenarios()
