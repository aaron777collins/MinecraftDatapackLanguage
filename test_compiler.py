#!/usr/bin/env python3
"""
Comprehensive test suite for the MDL Compiler
Tests all compilation features including directory structure, file generation, and Minecraft command output
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler
from minecraft_datapack_language.ast_nodes import *


class TestMDLCompiler(unittest.TestCase):
    """Test the MDL Compiler implementation."""
    
    def setUp(self):
        """Set up parser and compiler for each test."""
        self.parser = MDLParser()
        self.temp_dir = tempfile.mkdtemp()
        self.compiler = MDLCompiler(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_basic_compilation(self):
        """Test basic compilation of a simple MDL program."""
        source = '''
        pack "TestPack" "A test datapack" 15;
        namespace "test";
        
        var num player_score<@s> = 0;
        
        function test:main<@s> {
            player_score<@s> = 100;
            say "Your score is $player_score<@s>$!";
        }
        
        on_load test:main;
        '''
        
        # Parse and compile
        ast = self.parser.parse(source)
        result_path = self.compiler.compile(ast)
        
        # Verify output structure
        test_path = Path(result_path)
        self.assertTrue(test_path.exists())
        
        # Test Path operations step by step to avoid chaining issues
        pack_mcmeta_path = test_path / "pack.mcmeta"
        data_path = test_path / "data"
        functions_path = data_path / "test" / "functions"
        
        self.assertTrue(pack_mcmeta_path.exists())
        self.assertTrue(data_path.exists())
        self.assertTrue(functions_path.exists())
        
        # Verify pack.mcmeta
        with open(Path(result_path) / "pack.mcmeta") as f:
            pack_data = json.load(f)
            self.assertEqual(pack_data["pack"]["pack_format"], 15)
            self.assertEqual(pack_data["pack"]["description"], "A test datapack")
        
        # Verify function file
        func_file = Path(result_path) / "data" / "test" / "functions" / "main.mcfunction"
        self.assertTrue(func_file.exists())
        
        with open(func_file) as f:
            content = f.read()
            self.assertIn("scoreboard players set @s player_score 100", content)
            self.assertIn("tellraw @a", content)
    
    def test_complex_compilation(self):
        """Test compilation of a complex MDL program with all features."""
        source = '''
        pack "ComplexGame" "A complex game datapack" 15;
        namespace "game";
        
        // Tag declarations
        tag recipe "diamond_sword" "recipes/diamond_sword.json";
        tag loot_table "epic_loot" "loot_tables/epic_loot.json";
        tag advancement "first_spell" "advancements/first_spell.json";
        
        // Variables with complex scopes
        var num global_score<@a> = 0;
        var num player_level<@s> = 1;
        var num team_score<@a[team=red]> = 0;
        
        // Complex function with nested control
        function game:start_game<@s> {
            player_level<@s> = 1;
            global_score<@a> = $global_score<@a>$ + 10;
            
            if $player_level<@s>$ > 0 {
                say "Game started! Level: $player_level<@s>$";
                team_score<@a[team=red]> = 0;
            }
        }
        
        // Function with complex expressions
        function game:update_score<@s> {
            var num bonus<@s> = ($player_level<@s>$ * 2) + 5;
            player_level<@s> = $player_level<@s>$ + $bonus<@s>$;
            
            if $player_level<@s>$ > 10 {
                say "Level up! New level: $player_level<@s>$";
            }
        }
        
        // Hooks
        on_load game:start_game;
        on_tick game:update_score<@s>;
        
        // Top-level statements
        exec game:start_game<@a>;
        
        // Raw block
        $!raw
        scoreboard objectives add game_timer dummy "Game Timer"
        raw!$
        '''
        
        # Parse and compile
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Verify complex structure
        functions_dir = Path(output_path) / "data" / "game" / "functions"
        self.assertTrue(functions_dir.exists())
        
        # Verify function files
        start_game_file = functions_dir / "start_game.mcfunction"
        update_score_file = functions_dir / "update_score.mcfunction"
        
        self.assertTrue(start_game_file.exists())
        self.assertTrue(update_score_file.exists())
        
        # Verify load and tick functions
        load_file = functions_dir / "load.mcfunction"
        tick_file = functions_dir / "tick.mcfunction"
        
        self.assertTrue(load_file.exists())
        self.assertTrue(tick_file.exists())
        
        # Check load function content
        with open(load_file) as f:
            content = f.read()
            self.assertIn("scoreboard objectives add global_score", content)
            self.assertIn("scoreboard objectives add player_level", content)
            self.assertIn("scoreboard objectives add team_score", content)
            self.assertIn("function game:start_game", content)
    
    def test_pack_format_directory_mapping(self):
        """Test that different pack formats use correct directory structures."""
        # Test pack format 15 (modern)
        source_modern = '''
        pack "ModernPack" "Modern format" 15;
        namespace "modern";
        function modern:test<@s> { say "test"; }
        '''
        
        ast_modern = self.parser.parse(source_modern)
        output_modern = self.compiler.compile(ast_modern)
        
        # Modern format should use plural directories (pack format 15)
        func_dir_modern = Path(output_modern) / "data" / "modern" / "functions"
        self.assertTrue(func_dir_modern.exists())
        
        # Test pack format 10 (legacy)
        source_legacy = '''
        pack "LegacyPack" "Legacy format" 10;
        namespace "legacy";
        function legacy:test<@s> { say "test"; }
        '''
        
        ast_legacy = self.parser.parse(source_legacy)
        output_legacy = self.compiler.compile(ast_legacy)
        
        # Legacy format should use plural directories
        func_dir_legacy = Path(output_legacy) / "data" / "legacy" / "functions"
        self.assertTrue(func_dir_legacy.exists())
    
    def test_variable_compilation(self):
        """Test that variables are properly compiled to scoreboard objectives."""
        source = '''
        pack "VarTest" "Variable test" 15;
        namespace "test";
        
        var num score<@s> = 0;
        var num health<@a> = 20;
        var num level<@p> = 1;
        
        function test:set_vars<@s> {
            score<@s> = 100;
            health<@a> = 25;
            level<@p> = 5;
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check that variables are registered
        self.assertIn("score", self.compiler.variables)
        self.assertIn("health", self.compiler.variables)
        self.assertIn("level", self.compiler.variables)
        
        # Check load function has scoreboard objectives
        load_file = Path(output_path) / "data" / "test" / "functions" / "load.mcfunction"
        with open(load_file) as f:
            content = f.read()
            self.assertIn("scoreboard objectives add score", content)
            self.assertIn("scoreboard objectives add health", content)
            self.assertIn("scoreboard objectives add level", content)
    
    def test_say_command_compilation(self):
        """Test that say commands are properly converted to tellraw commands."""
        source = '''
        pack "SayTest" "Say command test" 15;
        namespace "test";
        
        var num score<@s> = 0;
        
        function test:say_test<@s> {
            say "Hello World!";
            say "Your score is $score<@s>$!";
            say "Welcome $score<@s>$ to the game!";
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check function file
        func_file = Path(output_path) / "data" / "test" / "functions" / "say_test.mcfunction"
        with open(func_file) as f:
            content = f.read()
            
            # Simple say command
            self.assertIn('tellraw @a {"text":"Hello World!"}', content)
            
            # Say command with variable
            self.assertIn('tellraw @a {"text":"Your score is ","extra":[{"score":{"name":"@s","objective":"score"}},"!"]}', content)
    
    def test_raw_block_compilation(self):
        """Test that raw blocks are properly passed through."""
        source = '''
        pack "RawTest" "Raw block test" 15;
        namespace "test";
        
        function test:raw_test<@s> {
            $!raw
            execute as @a run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
            execute as @a run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1
            raw!$
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check function file
        func_file = Path(output_path) / "data" / "test" / "functions" / "raw_test.mcfunction"
        with open(func_file) as f:
            content = f.read()
            self.assertIn("execute as @a run particle minecraft:explosion", content)
            self.assertIn("execute as @a run playsound minecraft:entity.player.levelup", content)
    
    def test_control_structure_compilation(self):
        """Test that control structures are properly compiled."""
        source = '''
        pack "ControlTest" "Control structure test" 15;
        namespace "test";
        
        var num counter<@s> = 0;
        
        function test:control_test<@s> {
            if $counter<@s>$ > 0 {
                counter<@s> = $counter<@s>$ - 1;
                say "Counter: $counter<@s>$";
            }
            
            while $counter<@s>$ < 10 {
                counter<@s> = $counter<@s>$ + 1;
            }
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check function file
        func_file = Path(output_path) / "data" / "test" / "functions" / "control_test.mcfunction"
        with open(func_file) as f:
            content = f.read()
            # Control structures should be converted to comments for now
            self.assertIn("# if", content)
            self.assertIn("# while", content)
    
    def test_function_call_compilation(self):
        """Test that function calls are properly compiled."""
        source = '''
        pack "CallTest" "Function call test" 15;
        namespace "test";
        
        function test:helper<@s> {
            say "Helper called!";
        }
        
        function test:main<@s> {
            exec test:helper<@s>;
            exec test:helper;
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check main function file
        main_file = Path(output_path) / "data" / "test" / "functions" / "main.mcfunction"
        with open(main_file) as f:
            content = f.read()
            self.assertIn("execute as @s run function test:helper", content)
            self.assertIn("function test:helper", content)
    
    def test_hook_compilation(self):
        """Test that hooks are properly compiled to load/tick functions."""
        source = '''
        pack "HookTest" "Hook test" 15;
        namespace "test";
        
        function test:init<@s> {
            say "Initializing...";
        }
        
        function test:update<@s> {
            say "Updating...";
        }
        
        on_load test:init;
        on_tick test:update<@s>;
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check load function
        load_file = Path(output_path) / "data" / "test" / "functions" / "load.mcfunction"
        with open(load_file) as f:
            content = f.read()
            self.assertIn("function test:init", content)
        
        # Check tick function
        tick_file = Path(output_path) / "data" / "test" / "functions" / "tick.mcfunction"
        with open(tick_file) as f:
            content = f.read()
            self.assertIn("execute as @s run function test:update", content)
    
    def test_tag_compilation(self):
        """Test that tag declarations are properly compiled."""
        source = '''
        pack "TagTest" "Tag test" 15;
        namespace "test";
        
        tag recipe "sword" "recipes/sword.json";
        tag loot_table "chest" "loot_tables/chest.json";
        tag advancement "win" "advancements/win.json";
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check that tag directories are created
        tags_dir = Path(output_path) / "data" / "minecraft" / "tags" / "items"
        self.assertTrue(tags_dir.exists())
        
        # Check tag files
        sword_tag = tags_dir / "sword.json"
        chest_tag = tags_dir / "chest.json"
        win_tag = tags_dir / "win.json"
        
        self.assertTrue(sword_tag.exists())
        self.assertTrue(chest_tag.exists())
        self.assertTrue(win_tag.exists())
        
        # Check tag file content
        with open(sword_tag) as f:
            tag_data = json.load(f)
            self.assertIn("values", tag_data)
            self.assertIn("test:sword", tag_data["values"])
    
    def test_complex_scope_handling(self):
        """Test compilation with complex scope selectors."""
        source = '''
        pack "ScopeTest" "Complex scope test" 15;
        namespace "test";
        
        var num team_score<@a[team=red]> = 0;
        var num player_data<@e[type=armor_stand,tag=server,limit=1]> = 0;
        var num nearby_score<@a[distance=..10]> = 0;
        
        function test:scope_test<@s> {
            team_score<@a[team=red]> = 100;
            player_data<@e[type=armor_stand,tag=server,limit=1]> = 42;
            nearby_score<@a[distance=..10]> = $nearby_score<@a[distance=..10]>$ + 1;
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check function file
        func_file = Path(output_path) / "data" / "test" / "functions" / "scope_test.mcfunction"
        with open(func_file) as f:
            content = f.read()
            self.assertIn("scoreboard players set @a[team=red] team_score 100", content)
            self.assertIn("scoreboard players set @e[type=armor_stand,tag=server,limit=1] player_data 42", content)
    
    def test_expression_compilation(self):
        """Test that complex expressions are properly compiled."""
        source = '''
        pack "ExprTest" "Expression test" 15;
        namespace "test";
        
        var num a<@s> = 10;
        var num b<@s> = 20;
        var num c<@s> = 30;
        
        function test:expr_test<@s> {
            var num result<@s> = ($a<@s>$ + $b<@s>$) * $c<@s>$;
            var num complex<@s> = (($a<@s>$ * $b<@s>$) + $c<@s>$) / 2;
        }
        '''
        
        ast = self.parser.parse(source)
        output_path = self.compiler.compile(ast)
        
        # Check function file
        func_file = Path(output_path) / "data" / "test" / "functions" / "expr_test.mcfunction"
        with open(func_file) as f:
            content = f.read()
            # Expressions should be converted to scoreboard operations
            self.assertIn("scoreboard players set @s result", content)
            self.assertIn("scoreboard players set @s complex", content)
    
    def test_error_handling(self):
        """Test that compilation errors are properly handled."""
        # Test with invalid AST (missing required fields)
        invalid_ast = Program(
            pack=None,
            namespace=None,
            tags=[],
            variables=[],
            functions=[],
            hooks=[],
            statements=[]
        )
        
        # This should not raise an error, but create a default pack
        try:
            output_path = self.compiler.compile(invalid_ast)
            self.assertTrue(Path(output_path).exists())
            
            # Check default pack.mcmeta
            pack_file = Path(output_path) / "pack.mcmeta"
            with open(pack_file) as f:
                pack_data = json.load(f)
                self.assertEqual(pack_data["pack"]["pack_format"], 15)
                self.assertEqual(pack_data["pack"]["description"], "MDL Generated Datapack")
        except Exception as e:
            self.fail(f"Compilation should handle invalid AST gracefully: {e}")


if __name__ == '__main__':
    print("🧪 Running MDL Compiler Tests...")
    unittest.main(verbosity=2)
