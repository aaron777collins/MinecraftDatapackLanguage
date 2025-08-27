#!/usr/bin/env python3
"""
Comprehensive test script for all MDL examples and their Python API equivalents.
This script tests both MDL files and Python API examples to ensure they work correctly.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"Testing: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def test_mdl_file(mdl_file, description):
    """Test an MDL file by checking and building it"""
    # Test syntax check
    if not run_command(f"mdl check {mdl_file}", f"Syntax check: {description}"):
        return False
    
    # Test build
    if not run_command(f"mdl build --mdl {mdl_file} -o test_examples/dist", f"Build: {description}"):
        return False
    
    return True

def test_python_file(py_file, description):
    """Test a Python file by running it"""
    return run_command(f"python {py_file}", f"Python API: {description}")

def test_multi_file_project(project_dir, description):
    """Test a multi-file project"""
    # Test syntax check
    if not run_command(f"mdl check {project_dir}/", f"Multi-file syntax check: {description}"):
        return False
    
    # Test build
    if not run_command(f"mdl build --mdl {project_dir}/ -o test_examples/dist", f"Multi-file build: {description}"):
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive MDL example tests...")
    print("=" * 60)
    
    # Create test directory
    os.makedirs("test_examples/dist", exist_ok=True)
    
    # Test results tracking
    total_tests = 0
    passed_tests = 0
    
    # Single file MDL examples
    mdl_examples = [
        ("test_examples/hello_world.mdl", "Hello World"),
        ("test_examples/particles.mdl", "Particle Effects"),
        ("test_examples/commands.mdl", "Custom Commands"),
        ("test_examples/combat_system.mdl", "Combat System"),
        ("test_examples/ui_system.mdl", "UI System"),
        ("test_examples/adventure_pack.mdl", "Adventure Pack"),
        ("test_examples/conditionals.mdl", "Conditionals"),
    ]
    
    # Python API examples
    python_examples = [
        ("test_examples/hello_world.py", "Hello World"),
        ("test_examples/particles.py", "Particle Effects"),
        ("test_examples/commands.py", "Custom Commands"),
        ("test_examples/combat_system.py", "Combat System"),
        ("test_examples/ui_system.py", "UI System"),
        ("test_examples/adventure_pack.py", "Adventure Pack"),
        ("test_examples/conditionals.py", "Conditionals"),
    ]
    
    # Multi-file project
    multi_file_projects = [
        ("test_examples/adventure_pack", "Multi-file Adventure Pack"),
    ]
    
    # Test MDL files
    print("\n📝 Testing MDL Files:")
    print("-" * 30)
    for mdl_file, description in mdl_examples:
        total_tests += 1
        if test_mdl_file(mdl_file, description):
            passed_tests += 1
    
    # Test Python API files
    print("\n🐍 Testing Python API Examples:")
    print("-" * 35)
    for py_file, description in python_examples:
        total_tests += 1
        if test_python_file(py_file, description):
            passed_tests += 1
    
    # Test multi-file projects
    print("\n📁 Testing Multi-file Projects:")
    print("-" * 30)
    for project_dir, description in multi_file_projects:
        total_tests += 1
        if test_multi_file_project(project_dir, description):
            passed_tests += 1
    
    # Test CLI functionality
    print("\n🔧 Testing CLI Functionality:")
    print("-" * 30)
    
    # Test help command
    total_tests += 1
    if run_command("mdl --help", "CLI help command"):
        passed_tests += 1
    
    # Test new command
    total_tests += 1
    if run_command('mdl new test_pack --name "Test Pack" --pack-format 48', "CLI new command"):
        passed_tests += 1
    
    # Clean up test pack
    if os.path.exists("test_pack"):
        shutil.rmtree("test_pack")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! All examples are working correctly.")
        return 0
    else:
        print(f"\n❌ {total_tests - passed_tests} test(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
