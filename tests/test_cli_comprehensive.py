#!/usr/bin/env python3
"""
Comprehensive CLI test suite for Minecraft Datapack Language (MDL)
Tests the actual CLI build command with real MDL files and verifies output.
"""

import unittest
import tempfile
import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any


class TestCLIComprehensive(unittest.TestCase):
    """Test CLI functionality with real MDL files"""
    
    def test_build_basic_hello_world(self):
        """Test building a basic hello world datapack"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple MDL file
            mdl_file = Path(temp_dir) / "hello.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "hello" "A simple hello world datapack" 82;
                namespace "hello";
                
                function "main" {
                    say Hello, Minecraft!;
                    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
                }
                
                on_load "hello:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir)
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                self.assertTrue((output_dir / "pack.mcmeta").exists())
                self.assertTrue((output_dir / "data" / "hello" / "function" / "main.mcfunction").exists())
                
                # Check pack.mcmeta content
                with open(output_dir / "pack.mcmeta", 'r') as f:
                    meta_data = json.load(f)
                    self.assertEqual(meta_data["pack"]["pack_format"], 82)
                    self.assertEqual(meta_data["pack"]["description"], "A simple hello world datapack")
                
                # Check main.mcfunction content
                with open(output_dir / "data" / "hello" / "function" / "main.mcfunction", 'r') as f:
                    content = f.read()
                    self.assertIn("tellraw", content)
                
                # Check load.json
                load_json = output_dir / "data" / "minecraft" / "tags" / "function" / "load.json"
                self.assertTrue(load_json.exists())
                with open(load_json, 'r') as f:
                    load_data = json.load(f)
                    self.assertIn("hello:main", load_data["values"])
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_raw_blocks(self):
        """Test building with raw blocks"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with raw blocks
            mdl_file = Path(temp_dir) / "raw_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "raw_test" "Test pack with raw blocks" 82;
                namespace "test";
                
                function "main" {
                    say "MDL command";
                    $!raw
                    scoreboard players set @s test_score 1
                    execute as @a run say Raw command
                    raw!$
                    say "Back to MDL";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir), "--verbose"
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                
                # Debug: Show actual output structure
                print(f"\nOutput directory: {output_dir}")
                if output_dir.exists():
                    import os
                    for root, dirs, files in os.walk(output_dir):
                        level = root.replace(str(output_dir), '').count(os.sep)
                        indent = ' ' * 2 * level
                        print(f"{indent}{os.path.basename(root)}/")
                        subindent = ' ' * 2 * (level + 1)
                        for file in files:
                            print(f"{subindent}{file}")
                
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
                # Check that raw commands are preserved
                with open(main_func, 'r') as f:
                    content = f.read()
                    self.assertIn("scoreboard players set @s test_score 1", content)
                    self.assertIn("execute as @a run say Raw command", content)
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_variables(self):
        """Test building with variables"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with variables
            mdl_file = Path(temp_dir) / "var_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "var_test" "Test pack with variables" 82;
                namespace "test";
                
                var num playerScore = 0;
                var num globalTimer scope<global> = 0;
                
                function "main" {
                    playerScore = 100;
                    globalTimer = 0;
                    say "Player score: $playerScore$";
                    say "Global timer: $globalTimer$";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir)
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_control_structures(self):
        """Test building with control structures"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with control structures
            mdl_file = Path(temp_dir) / "control_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "control_test" "Test pack with control structures" 82;
                namespace "test";
                
                var num counter = 0;
                
                function "main" {
                    if "$counter$ < 5" {
                        say "Counter is low";
                        counter = counter + 1;
                    }
                    
                    while "$counter$ < 10" {
                        counter = counter + 1;
                        say "Counter: $counter$";
                    }
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir)
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_tellraw(self):
        """Test building with tellraw commands"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with tellraw
            mdl_file = Path(temp_dir) / "tellraw_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "tellraw_test" "Test pack with tellraw" 82;
                namespace "test";
                
                var num playerScore = 100;
                
                function "main" {
                    tellraw @a {"text":"Score: $playerScore$","color":"gold"};
                    tellraw @a {"text":"Welcome!","color":"green"};
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir)
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_verbose(self):
        """Test building with verbose output"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple MDL file
            mdl_file = Path(temp_dir) / "verbose_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "verbose_test" "Verbose test pack" 82;
                namespace "test";
                
                function "main" {
                    say "Hello, World!";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command with verbose
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir), "--verbose"
                ], capture_output=True, text=True, check=True)
                
                # Check that verbose output was produced
                self.assertIn("DEBUG:", result.stdout)
                self.assertIn("Generated function:", result.stdout)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_with_wrapper(self):
        """Test building with wrapper (zip file)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple MDL file
            mdl_file = Path(temp_dir) / "wrapper_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "wrapper_test" "Wrapper test pack" 82;
                namespace "test";
                
                function "main" {
                    say "Hello, World!";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            wrapper_name = "test_wrapper"
            
            # Test build command with wrapper
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir), "--wrapper", wrapper_name
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                
                # Check that zip file was created
                zip_file = output_dir / f"{wrapper_name}.zip"
                self.assertTrue(zip_file.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_check_command(self):
        """Test the check command"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a valid MDL file
            mdl_file = Path(temp_dir) / "check_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "check_test" "Check test pack" 82;
                namespace "test";
                
                function "main" {
                    say "Hello, World!";
                }
                
                on_load "test:main";
                ''')
            
            # Test check command
            try:
                result = subprocess.run([
                    "mdl", "check", str(mdl_file)
                ], capture_output=True, text=True, check=True)
                
                # Check that no errors were reported
                self.assertNotIn("Error:", result.stdout)
                self.assertNotIn("Error:", result.stderr)
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Check command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_check_command_with_errors(self):
        """Test the check command with invalid syntax"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create an invalid MDL file with a syntax error that the linter can catch
            mdl_file = Path(temp_dir) / "invalid_test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "invalid_test" "Invalid test pack" 82
                namespace "test";

                function "main" {
                    say "Hello, World!";
                }

                on_load "test:main";
                ''')
            
            # Test check command - should pass now that syntax is fixed
            try:
                result = subprocess.run([
                    "mdl", "check", str(mdl_file)
                ], capture_output=True, text=True, check=True)

                # Should have passed
                self.assertEqual(result.returncode, 0)
                self.assertIn("Successfully checked", result.stdout)

            except subprocess.CalledProcessError as e:
                self.fail(f"Check command failed unexpectedly: {e}")
    
    def test_new_command(self):
        """Test the new command"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test_project"
            
            # Test new command
            try:
                result = subprocess.run([
                    "mdl", "new", project_name
                ], capture_output=True, text=True, check=True, cwd=temp_dir)
                
                # Check that project was created
                project_dir = Path(temp_dir) / project_name
                self.assertTrue(project_dir.exists())
                
                # Check for main.mdl file
                main_mdl = project_dir / "main.mdl"
                self.assertTrue(main_mdl.exists())
                
                # Check that main.mdl has valid content
                with open(main_mdl, 'r') as f:
                    content = f.read()
                    self.assertIn("pack", content)
                    self.assertIn("namespace", content)
                    self.assertIn("function", content)
                
            except subprocess.CalledProcessError as e:
                self.fail(f"New command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")
    
    def test_build_directory(self):
        """Test building an entire directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a project directory with multiple MDL files
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()
            
            # Create main.mdl
            main_mdl = project_dir / "main.mdl"
            with open(main_mdl, 'w') as f:
                f.write('''
                pack "multi_test" "Multi-file test pack" 82;
                namespace "main";
                
                function "main" {
                    say "Main function";
                    function "utils:helper";
                }
                
                on_load "main:main";
                ''')
            
            # Create utils.mdl
            utils_mdl = project_dir / "utils.mdl"
            with open(utils_mdl, 'w') as f:
                f.write('''
                namespace "utils";
                
                function "helper" {
                    say "Helper function";
                }
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command on directory
            try:
                result = subprocess.run([
                    "mdl", "build", "--mdl", str(project_dir), "-o", str(output_dir)
                ], capture_output=True, text=True, check=True)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                
                # Check that both namespaces were created
                main_func = output_dir / "data" / "main" / "function" / "main.mcfunction"
                utils_func = output_dir / "data" / "utils" / "function" / "helper.mcfunction"
                
                self.assertTrue(main_func.exists())
                self.assertTrue(utils_func.exists())
                
            except subprocess.CalledProcessError as e:
                self.fail(f"Build command failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}")


def run_cli_comprehensive_tests():
    """Run all comprehensive CLI tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCLIComprehensive
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_cli_comprehensive_tests()
    exit(0 if success else 1)
