#!/usr/bin/env python3
"""
Input/Output Test System for MDL

This test system takes MDL input files, builds them through our CLI,
and verifies every generated file matches expected output.
"""

import os
import tempfile
import zipfile
import json
from pathlib import Path
from typing import Dict, List, Any
import pytest

from minecraft_datapack_language.cli import build_mdl


class IOTestCase:
    """Represents a single input/output test case."""
    
    def __init__(self, name: str, mdl_content: str, expected_files: Dict[str, str]):
        self.name = name
        self.mdl_content = mdl_content
        self.expected_files = expected_files
    
    def run(self) -> List[str]:
        """Run the test and return list of errors (empty if success)."""
        errors = []
        
        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Write the MDL file
            mdl_file = temp_path / "test.mdl"
            with open(mdl_file, 'w', encoding='utf-8') as f:
                f.write(self.mdl_content)
            
            # Build the datapack
            output_dir = temp_path / "output"
            try:
                build_mdl(str(mdl_file), str(output_dir), verbose=False)
            except Exception as e:
                errors.append(f"Build failed: {e}")
                return errors
            
            # Check if zip file was created
            zip_file = output_dir.parent / f"{output_dir.name}.zip"
            if not zip_file.exists():
                errors.append(f"Expected zip file not found: {zip_file}")
                return errors
            
            # Extract and verify files
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Get all files in the zip
                zip_files = {info.filename: info for info in zip_ref.infolist()}
                
                # Verify each expected file
                for expected_path, expected_content in self.expected_files.items():
                    if expected_path not in zip_files:
                        errors.append(f"Expected file not found: {expected_path}")
                        continue
                    
                    # Read the actual file content
                    actual_content = zip_ref.read(expected_path).decode('utf-8')
                    
                    # Compare content (normalize line endings)
                    expected_normalized = expected_content.replace('\r\n', '\n').strip()
                    actual_normalized = actual_content.replace('\r\n', '\n').strip()
                    
                    if expected_normalized != actual_normalized:
                        errors.append(f"Content mismatch in {expected_path}:")
                        errors.append(f"Expected:\n{expected_normalized}")
                        errors.append(f"Actual:\n{actual_normalized}")
                        errors.append("---")
        
        return errors


def test_hello_load_function():
    """Test the hello.mdl example with load function verification."""
    
    mdl_content = '''// hello.mdl
pack "My First Pack" "A simple example" 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    say Counter: $counter$;
}

on_load "example:hello";
'''
    
    expected_files = {
        # Pack metadata
        "pack.mcmeta": '''{
  "pack": {
    "description": "A simple example",
    "pack_format": 82
  }
}''',
        
        # Load function - should NOT call hello function (handled by load.json tag)
        "data/example/function/load.mcfunction": '''execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] counter 0''',
        
        # Hello function with proper variable substitution (no armor stand setup needed)
        "data/example/function/hello.mcfunction": '''tellraw @a [{"text":"Hello, Minecraft !"}]
tellraw @a {"text":"Welcome to my datapack!","color":"green"}
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] counter 1
tellraw @a [{"text":"Counter: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"counter"}}]''',
        
        # Load tag - should include both load and hello functions
        "data/minecraft/tags/function/load.json": '''{
  "replace": false,
  "values": [
    "example:hello",
    "example:load"
  ]
}'''
    }
    
    test_case = IOTestCase("hello_load_function", mdl_content, expected_files)
    errors = test_case.run()
    
    if errors:
        pytest.fail(f"Test failed:\n" + "\n".join(errors))


def test_variable_assignment():
    """Test variable assignment and substitution."""
    
    mdl_content = '''// variable_test.mdl
pack "Variable Test" "Testing variables" 82;

namespace "test";

var num score = 0;
var num health = 100;

function "main" {
    score = 50;
    health = $health$ - 10;
    say "Score: $score$, Health: $health$";
}

on_load "test:main";
'''
    
    expected_files = {
        # Load function
        "data/test/function/load.mcfunction": '''execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add score dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] score 0
scoreboard objectives add health dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] health 0''',
        
        # Main function with variable assignments (no armor stand setup needed)
        "data/test/function/main.mcfunction": '''scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] score 50
scoreboard players remove @e[type=armor_stand,tag=mdl_server,limit=1] health 10
tellraw @a [{"text":"Score: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"score"}},{"text":", Health: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"health"}}]''',
        
        # Load tag
        "data/minecraft/tags/function/load.json": '''{
  "replace": false,
  "values": [
    "test:main",
    "test:load"
  ]
}'''
    }
    
    test_case = IOTestCase("variable_assignment", mdl_content, expected_files)
    errors = test_case.run()
    
    if errors:
        pytest.fail(f"Test failed:\n" + "\n".join(errors))


def test_if_statement():
    """Test if statement generation."""
    
    mdl_content = '''// if_test.mdl
pack "If Test" "Testing if statements" 82;

namespace "test";

var num value = 0;

function "main" {
    value = 5;
    if "$value$ > 3" {
        say "Value is greater than 3";
    } else {
        say "Value is 3 or less";
    }
}

on_load "test:main";
'''
    
    expected_files = {
        # Load function
        "data/test/function/load.mcfunction": '''execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add value dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] value 0''',
        
        # Main function with if statement (no armor stand setup needed)
        "data/test/function/main.mcfunction": '''scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] value 5''',
        
        # Load tag
        "data/minecraft/tags/function/load.json": '''{
  "replace": false,
  "values": [
    "test:main",
    "test:load"
  ]
}'''
    }
    
    test_case = IOTestCase("if_statement", mdl_content, expected_files)
    errors = test_case.run()
    
    if errors:
        pytest.fail(f"Test failed:\n" + "\n".join(errors))


def test_while_loop():
    """Test while loop generation."""
    
    mdl_content = '''// while_test.mdl
pack "While Test" "Testing while loops" 82;

namespace "test";

var num counter = 0;

function "main" {
    while "$counter$ < 3" {
        say "Counter: $counter$";
        counter = $counter$ + 1;
    }
}

on_load "test:main";
'''
    
    expected_files = {
        # Load function
        "data/test/function/load.mcfunction": '''execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] counter 0''',
        
        # Main function with while loop (no armor stand setup needed)
        "data/test/function/main.mcfunction": '''''',
        
        # Load tag
        "data/minecraft/tags/function/load.json": '''{
  "replace": false,
  "values": [
    "test:main",
    "test:load"
  ]
}'''
    }
    
    test_case = IOTestCase("while_loop", mdl_content, expected_files)
    errors = test_case.run()
    
    if errors:
        pytest.fail(f"Test failed:\n" + "\n".join(errors))


def test_multi_file_project():
    """Test multi-file project with namespace handling."""
    
    # Create temporary files for multi-file test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Main file
        main_mdl = temp_path / "main.mdl"
        with open(main_mdl, 'w', encoding='utf-8') as f:
            f.write('''// main.mdl
pack "Multi Test" "Multi-file test" 82;

namespace "main";

var num global_counter = 0;

function "init" {
    say "Initializing...";
    global_counter = 10;
}

on_load "main:init";
''')
        
        # Secondary file
        other_mdl = temp_path / "other.mdl"
        with open(other_mdl, 'w', encoding='utf-8') as f:
            f.write('''// other.mdl
namespace "other";

function "helper" {
    say "Helper function called";
}
''')
        
        expected_files = {
            # Pack metadata
            "pack.mcmeta": '''{
  "pack": {
    "description": "Multi-file test",
    "pack_format": 82
  }
}''',
            
            # Main namespace load function
            "data/main/function/load.mcfunction": '''execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add global_counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 0''',
            
            # Main namespace init function
            "data/main/function/init.mcfunction": '''tellraw @a [{"text":"Initializing..."}]
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 10''',
            
            # Other namespace helper function
            "data/other/function/helper.mcfunction": '''tellraw @a [{"text":"Helper function called"}]''',
            
            # Load tag
            "data/minecraft/tags/function/load.json": '''{
  "replace": false,
  "values": [
    "main:init",
    "main:load"
  ]
}'''
        }
        
        # Build the multi-file project
        output_dir = temp_path / "output"
        try:
            build_mdl(str(temp_path), str(output_dir), verbose=False)
        except Exception as e:
            pytest.fail(f"Multi-file build failed: {e}")
        
        # Check if zip file was created
        zip_file = output_dir.parent / f"{output_dir.name}.zip"
        if not zip_file.exists():
            pytest.fail(f"Expected zip file not found: {zip_file}")
        
        # Extract and verify files
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_files = {info.filename: info for info in zip_ref.infolist()}
            
            for expected_path, expected_content in expected_files.items():
                if expected_path not in zip_files:
                    pytest.fail(f"Expected file not found: {expected_path}")
                
                actual_content = zip_ref.read(expected_path).decode('utf-8')
                expected_normalized = expected_content.replace('\r\n', '\n').strip()
                actual_normalized = actual_content.replace('\r\n', '\n').strip()
                
                if expected_normalized != actual_normalized:
                    pytest.fail(f"Content mismatch in {expected_path}:\nExpected:\n{expected_normalized}\nActual:\n{actual_normalized}")


if __name__ == "__main__":
    # Run tests directly
    test_hello_load_function()
    test_variable_assignment()
    test_if_statement()
    test_while_loop()
    test_multi_file_project()
    print("All I/O tests passed!")
