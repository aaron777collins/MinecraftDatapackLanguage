#!/usr/bin/env python3
"""
Test the build process with loop functionality.
This module can be imported and run as part of the test suite.
"""

from minecraft_datapack_language import Pack
import os
import tempfile
import shutil

def test_build_with_loops():
    """Test that the build process works correctly with loop syntax"""
    # Create a simple pack with a while loop
    p = Pack('test')
    p.namespace('test').function('test', 
        'while "score @s test matches 1..":',
        '    say test'
    )
    
    print("Testing build process with loop syntax...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            p.build(temp_dir)
            print(f"[+] Build completed successfully in {temp_dir}")
            
            # Check that the output directory was created
            if os.path.exists(temp_dir):
                print("[+] Output directory created")
                return True
            else:
                print("[-] Output directory not created")
                return False
                
        except Exception as e:
            print(f"[-] Build failed with error: {e}")
            return False

def test_build_with_mixed_control_flow():
    """Test that the build process works with loops and conditionals together"""
    p = Pack('test')
    p.namespace('test').function('mixed_test',
        'if "entity @s[type=minecraft:player]":',
        '    say Player detected',
        '    while "score @s counter matches 1..":',
        '        say Counter: @s counter',
        '        scoreboard players remove @s counter 1',
        '    say Loop finished',
        'else:',
        '    say No player found'
    )
    
    print("Testing build process with mixed control flow...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            p.build(temp_dir)
            print(f"[+] Mixed control flow build completed successfully in {temp_dir}")
            return True
        except Exception as e:
            print(f"[-] Mixed control flow build failed with error: {e}")
            return False

if __name__ == "__main__":
    print("[TEST] Testing Build Process with Loops")
    print("=" * 45)
    
    success1 = test_build_with_loops()
    print()
    
    success2 = test_build_with_mixed_control_flow()
    
    if success1 and success2:
        print("\n[+] All build tests passed!")
    else:
        print("\n[-] Some build tests failed!")
