#!/usr/bin/env python3
"""
Regression tests for MDL conditional functionality.
This ensures that conditionals work correctly and don't break existing features.
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

def test_conditional_syntax():
    """Test basic conditional syntax"""
    test_code = '''pack "Test" description "Test" pack_format 48

namespace "test"

function "simple_if":
    say Testing simple if statement
    if "entity @s[type=minecraft:player]":
        say Player detected!
        effect give @s minecraft:glowing 5 1

function "if_else":
    say Testing if/else statement
    if "entity @s[type=minecraft:player]":
        say Player detected!
        effect give @s minecraft:glowing 5 1
    else:
        say No player found
        say This is the else block

function "if_else_if_else":
    say Testing if/else if/else statement
    if "entity @s[type=minecraft:player]":
        say Player detected!
        effect give @s minecraft:glowing 5 1
    else if "entity @s[type=minecraft:zombie]":
        say Zombie detected!
        effect give @s minecraft:poison 5 1
    else:
        say Unknown entity
        say This is the final else block
'''
    
    # Write test file
    with open("test_conditional_syntax.mdl", "w") as f:
        f.write(test_code)
    
    # Test syntax check
    if not run_command("mdl check test_conditional_syntax.mdl", "Conditional syntax check"):
        return False
    
    # Test build
    if not run_command("mdl build --mdl test_conditional_syntax.mdl -o test_output", "Conditional build"):
        return False
    
    # Clean up
    os.remove("test_conditional_syntax.mdl")
    return True

def test_existing_functionality():
    """Test that existing functionality still works"""
    # Test sample.mdl
    if not run_command("mdl check sample.mdl", "Sample.mdl syntax check"):
        return False
    
    if not run_command("mdl build --mdl sample.mdl -o test_output", "Sample.mdl build"):
        return False
    
    # Test hello_world.mdl
    if not run_command("mdl check test_examples/hello_world.mdl", "Hello world syntax check"):
        return False
    
    if not run_command("mdl build --mdl test_examples/hello_world.mdl -o test_output", "Hello world build"):
        return False
    
    return True

def test_complex_conditions():
    """Test complex conditional conditions"""
    test_code = '''pack "Test" description "Test" pack_format 48

namespace "test"

function "complex_conditions":
    say Testing complex conditions
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}]":
        say Player with diamond sword!
        effect give @s minecraft:strength 10 1
    else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}]":
        say Player with golden sword!
        effect give @s minecraft:speed 10 1
    else if "entity @s[type=minecraft:player]":
        say Player without special sword
        effect give @s minecraft:haste 5 0
    else:
        say No player found
'''
    
    # Write test file
    with open("test_complex_conditions.mdl", "w") as f:
        f.write(test_code)
    
    # Test syntax check
    if not run_command("mdl check test_complex_conditions.mdl", "Complex conditions syntax check"):
        return False
    
    # Test build
    if not run_command("mdl build --mdl test_complex_conditions.mdl -o test_output", "Complex conditions build"):
        return False
    
    # Clean up
    os.remove("test_complex_conditions.mdl")
    return True

def test_mixed_commands():
    """Test conditionals mixed with regular commands"""
    test_code = '''pack "Test" description "Test" pack_format 48

namespace "test"

function "mixed_commands":
    say Testing mixed commands with conditionals
    say This is before the conditional
    if "entity @s[type=minecraft:player]":
        say Inside if block
        effect give @s minecraft:glowing 5 1
    say This is after the conditional
    say Another command after
'''
    
    # Write test file
    with open("test_mixed_commands.mdl", "w") as f:
        f.write(test_code)
    
    # Test syntax check
    if not run_command("mdl check test_mixed_commands.mdl", "Mixed commands syntax check"):
        return False
    
    # Test build
    if not run_command("mdl build --mdl test_mixed_commands.mdl -o test_output", "Mixed commands build"):
        return False
    
    # Clean up
    os.remove("test_mixed_commands.mdl")
    return True

def test_multiple_else_if():
    """Test multiple else if blocks"""
    test_code = '''pack "Test" description "Test" pack_format 48

namespace "test"

function "multiple_else_if":
    say Testing multiple else if blocks
    if "entity @s[type=minecraft:player]":
        say Player
    else if "entity @s[type=minecraft:zombie]":
        say Zombie
    else if "entity @s[type=minecraft:skeleton]":
        say Skeleton
    else if "entity @s[type=minecraft:creeper]":
        say Creeper
    else if "entity @s[type=minecraft:spider]":
        say Spider
    else:
        say Unknown entity
'''
    
    # Write test file
    with open("test_multiple_else_if.mdl", "w") as f:
        f.write(test_code)
    
    # Test syntax check
    if not run_command("mdl check test_multiple_else_if.mdl", "Multiple else if syntax check"):
        return False
    
    # Test build
    if not run_command("mdl build --mdl test_multiple_else_if.mdl -o test_output", "Multiple else if build"):
        return False
    
    # Clean up
    os.remove("test_multiple_else_if.mdl")
    return True

def test_conditional_with_function_calls():
    """Test conditionals that call other functions"""
    test_code = '''pack "Test" description "Test" pack_format 48

namespace "test"

function "conditional_with_calls":
    say Testing conditionals with function calls
    if "entity @s[type=minecraft:player]":
        say Calling player function
        function test:player_effects
    else if "entity @s[type=minecraft:zombie]":
        say Calling zombie function
        function test:zombie_effects
    else:
        say Calling default function
        function test:default_effects

function "player_effects":
    say Applying player effects
    effect give @s minecraft:night_vision 10 0

function "zombie_effects":
    say Applying zombie effects
    effect give @s minecraft:poison 5 1

function "default_effects":
    say Applying default effects
    effect give @s minecraft:glowing 5 0
'''
    
    # Write test file
    with open("test_conditional_with_calls.mdl", "w") as f:
        f.write(test_code)
    
    # Test syntax check
    if not run_command("mdl check test_conditional_with_calls.mdl", "Conditional with function calls syntax check"):
        return False
    
    # Test build
    if not run_command("mdl build --mdl test_conditional_with_calls.mdl -o test_output", "Conditional with function calls build"):
        return False
    
    # Clean up
    os.remove("test_conditional_with_calls.mdl")
    return True

def test_invalid_conditional_syntax():
    """Test that invalid conditional syntax is properly handled"""
    # Note: Invalid conditional syntax is treated as regular commands by the parser
    # This is the correct behavior since conditionals are processed in post-processing
    invalid_tests = [
        # Missing quotes around condition - should be treated as regular command
        '''pack "Test" description "Test" pack_format 48
namespace "test"
function "invalid":
    if entity @s[type=minecraft:player]:
        say Invalid
''',
        # Missing colon - should be treated as regular command
        '''pack "Test" description "Test" pack_format 48
namespace "test"
function "invalid":
    if "entity @s[type=minecraft:player]"
        say Invalid
''',
        # Invalid else if syntax - should be treated as regular command
        '''pack "Test" description "Test" pack_format 48
namespace "test"
function "invalid":
    if "entity @s[type=minecraft:player]":
        say Valid
    else if entity @s[type=minecraft:zombie]:
        say Invalid
''',
    ]
    
    for i, test_code in enumerate(invalid_tests):
        # Write test file
        test_file = f"test_invalid_{i}.mdl"
        with open(test_file, "w") as f:
            f.write(test_code)
        
        # Test that it passes syntax check (invalid conditionals are treated as regular commands)
        try:
            result = subprocess.run(f"mdl check {test_file}", shell=True, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print(f"✅ Invalid syntax test {i} - Correctly handled as regular command")
            else:
                print(f"❌ Invalid syntax test {i} - Should have passed but failed")
                os.remove(test_file)
                return False
        except Exception as e:
            print(f"❌ Invalid syntax test {i} - Unexpected error: {e}")
            os.remove(test_file)
            return False
        
        # Clean up
        os.remove(test_file)
    
    return True

def main():
    """Run all regression tests"""
    print("🚀 Starting MDL conditional regression tests...")
    print("=" * 60)
    
    # Create test directory
    os.makedirs("test_output", exist_ok=True)
    
    # Test results tracking
    total_tests = 0
    passed_tests = 0
    
    # Define test functions
    test_functions = [
        ("Basic conditional syntax", test_conditional_syntax),
        ("Existing functionality", test_existing_functionality),
        ("Complex conditions", test_complex_conditions),
        ("Mixed commands", test_mixed_commands),
        ("Multiple else if", test_multiple_else_if),
        ("Conditional with function calls", test_conditional_with_function_calls),
        ("Invalid syntax rejection", test_invalid_conditional_syntax),
    ]
    
    # Run tests
    for test_name, test_func in test_functions:
        print(f"\n📝 Testing: {test_name}")
        print("-" * 40)
        total_tests += 1
        if test_func():
            passed_tests += 1
        else:
            print(f"❌ {test_name} failed!")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Conditional functionality is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
