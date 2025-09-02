#!/usr/bin/env python3
"""
Comprehensive input/output test framework for MDL
Tests that MDL files compile to expected .mcfunction output
"""

import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any

class MDLOutputTester:
    def __init__(self):
        # Find the test_examples directory relative to this script
        script_dir = Path(__file__).parent
        self.test_dir = script_dir
        # Use unique output directory from environment variable if available (for CI)
        # This prevents race conditions when multiple jobs run in parallel
        test_output_dir = os.environ.get('TEST_OUTPUT_DIR', 'test_output')
        self.output_dir = script_dir / test_output_dir
        self.output_dir.mkdir(exist_ok=True)
        
    def run_mdl_build(self, mdl_file: Path, output_dir: Path) -> bool:
        """Run mdl build and return success status"""
        try:
            result = subprocess.run([
                "mdl", "build", "--mdl", str(mdl_file), "-o", str(output_dir)
            ], capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Build failed for {mdl_file}: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            return False
    
    def test_basic_hello_world(self) -> bool:
        """Test basic hello world example"""
        print("Testing basic hello world...")
        
        mdl_file = self.test_dir / "01_basic_hello_world.mdl"
        output_dir = self.output_dir / "basic_hello"
        
        if not self.run_mdl_build(mdl_file, output_dir):
            return False
        
        # Check expected structure
        expected_files = [
            "pack.mcmeta",
            "data/basic_hello/function/main.mcfunction",
            "data/minecraft/tags/function/load.json"
        ]
        
        for file_path in expected_files:
            full_path = output_dir / file_path
            if not full_path.exists():
                print(f"❌ Missing expected file: {file_path}")
                return False
        
        # Check pack.mcmeta content
        pack_meta = output_dir / "pack.mcmeta"
        with open(pack_meta) as f:
            meta_data = json.load(f)
            if meta_data.get("pack", {}).get("pack_format") != 82:
                print(f"❌ Wrong pack format: {meta_data.get('pack', {}).get('pack_format')}")
                return False
        
        # Check main.mcfunction content
        main_func = output_dir / "data/basic_hello/function/main.mcfunction"
        with open(main_func) as f:
            content = f.read().strip()
            expected_commands = [
                "execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}",
                "tellraw @a [{\"text\":\"Hello, Minecraft!\"}]",
                "tellraw @a {\"text\":\"Welcome to my datapack!\",\"color\":\"green\"}"
            ]
            for cmd in expected_commands:
                if cmd not in content:
                    print(f"❌ Missing expected command: {cmd}")
                    return False
        
        # Check load.json content
        load_json = output_dir / "data/minecraft/tags/function/load.json"
        with open(load_json) as f:
            load_data = json.load(f)
            if "basic_hello:main" not in load_data.get("values", []):
                print(f"❌ Missing load function in load.json")
                return False
        
        print("✅ Basic hello world test passed")
        return True
    
    def test_scoped_function_calls(self) -> bool:
        """Test scoped function calls example"""
        print("Testing scoped function calls...")
        
        mdl_file = self.test_dir / "03_scoped_function_calls.mdl"
        output_dir = self.output_dir / "scoped_calls"
        
        if not self.run_mdl_build(mdl_file, output_dir):
            return False
        
        # Check main.mcfunction for scoped function calls
        main_func = output_dir / "data/scoped_calls/function/main.mcfunction"
        with open(main_func) as f:
            content = f.read().strip()
            expected_commands = [
                "execute as @s run function scoped_calls:increment_player",
                "execute as @e[type=armor_stand,tag=mdl_server,limit=1] run function scoped_calls:increment_global",
                "execute as @a run function scoped_calls:show_scores"
            ]
            for cmd in expected_commands:
                if cmd not in content:
                    print(f"❌ Missing expected scoped function call: {cmd}")
                    return False
        
        # Check that the called functions exist
        expected_functions = [
            "data/scoped_calls/function/increment_player.mcfunction",
            "data/scoped_calls/function/increment_global.mcfunction",
            "data/scoped_calls/function/show_scores.mcfunction"
        ]
        
        for func_path in expected_functions:
            full_path = output_dir / func_path
            if not full_path.exists():
                print(f"❌ Missing function file: {func_path}")
                return False
        
        print("✅ Scoped function calls test passed")
        return True
    
    def test_variables_and_scopes(self) -> bool:
        """Test variables with different scopes"""
        print("Testing variables and scopes...")
        
        mdl_file = self.test_dir / "02_variables_and_scopes.mdl"
        output_dir = self.output_dir / "variables"
        
        if not self.run_mdl_build(mdl_file, output_dir):
            return False
        
        # Check main.mcfunction for variable operations
        main_func = output_dir / "data/variables/function/main.mcfunction"
        with open(main_func) as f:
            content = f.read().strip()
            
            # Check for scoreboard operations
            expected_ops = [
                "scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] globalCounter 1",
                "scoreboard players add @s playerCounter 1",
                "scoreboard players add @a[team=red] teamCounter 1"
            ]
            
            for op in expected_ops:
                if op not in content:
                    print(f"❌ Missing expected scoreboard operation: {op}")
                    return False
            
            # Check for tellraw with scoreboard display
            expected_tellraw = [
                "tellraw @a [{\"text\":\"Global counter: \"},{\"score\":{\"name\":\"@e[type=armor_stand,tag=mdl_server,limit=1]\",\"objective\":\"globalCounter\"}}]",
                "tellraw @a [{\"text\":\"Player counter: \"},{\"score\":{\"name\":\"@e[type=armor_stand,tag=mdl_server,limit=1]\",\"objective\":\"playerCounter\"}}]",
                "tellraw @a [{\"text\":\"Team counter: \"},{\"score\":{\"name\":\"@a[team=red]\",\"objective\":\"teamCounter\"}}]"
            ]
            
            for tellraw in expected_tellraw:
                if tellraw not in content:
                    print(f"❌ Missing expected tellraw: {tellraw}")
                    return False
        
        print("✅ Variables and scopes test passed")
        return True
    
    def test_while_loops(self) -> bool:
        """Test while loops"""
        print("Testing while loops...")
        
        mdl_file = self.test_dir / "04_while_loops.mdl"
        output_dir = self.output_dir / "while_loops"
        
        if not self.run_mdl_build(mdl_file, output_dir):
            return False
        
        # Check main.mcfunction for while loop structure
        main_func = output_dir / "data/while_loops/function/main.mcfunction"
        with open(main_func) as f:
            content = f.read().strip()
            
            # Should contain conditional function calls for while loop
            if "function while_loops:test_main_while_2" not in content:
                print("❌ Missing while loop function call")
                return False
        
        # Check that while loop function exists
        while_func = output_dir / "data/while_loops/function/test_main_while_2.mcfunction"
        if not while_func.exists():
            print("❌ Missing while loop function file")
            return False
        
        with open(while_func) as f:
            while_content = f.read().strip()
            
            # Should contain the loop body and recursive call
            expected_commands = [
                "scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] counter 1",
                "tellraw @a [{\"text\":\"Loop iteration: \"},{\"score\":{\"name\":\"@e[type=armor_stand,tag=mdl_server,limit=1]\",\"objective\":\"counter\"}}]"
            ]
            
            for cmd in expected_commands:
                if cmd not in while_content:
                    print(f"❌ Missing expected while loop command: {cmd}")
                    return False
        
        print("✅ While loops test passed")
        return True
    
    def test_raw_commands(self) -> bool:
        """Test raw command blocks"""
        print("Testing raw commands...")
        
        mdl_file = self.test_dir / "05_raw_commands.mdl"
        output_dir = self.output_dir / "raw_commands"
        
        if not self.run_mdl_build(mdl_file, output_dir):
            return False
        
        # Check main.mcfunction for raw commands
        main_func = output_dir / "data/raw_commands/function/main.mcfunction"
        with open(main_func) as f:
            content = f.read().strip()
            
            # Should contain raw commands exactly as written
            expected_raw_commands = [
                "effect give @a minecraft:night_vision 10 1 true",
                "effect give @a minecraft:jump_boost 10 2 true"
            ]
            
            for cmd in expected_raw_commands:
                if cmd not in content:
                    print(f"❌ Missing expected raw command: {cmd}")
                    return False
        
        # Check custom_commands.mcfunction for additional raw commands
        custom_func = output_dir / "data/raw_commands/function/custom_commands.mcfunction"
        with open(custom_func) as f:
            custom_content = f.read().strip()
            
            additional_raw_commands = [
                "gamemode creative @a",
                "weather clear",
                "time set day"
            ]
            
            for cmd in additional_raw_commands:
                if cmd not in custom_content:
                    print(f"❌ Missing expected raw command in custom_commands: {cmd}")
                    return False
        
        print("✅ Raw commands test passed")
        return True
    
    def run_all_tests(self) -> bool:
        """Run all output validation tests"""
        print("🧪 Running comprehensive MDL output validation tests...")
        
        tests = [
            self.test_basic_hello_world,
            self.test_scoped_function_calls,
            self.test_variables_and_scopes,
            self.test_while_loops,
            self.test_raw_commands
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    print(f"❌ Test failed: {test.__name__}")
            except Exception as e:
                print(f"❌ Test error in {test.__name__}: {e}")
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All output validation tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False

if __name__ == "__main__":
    tester = MDLOutputTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
