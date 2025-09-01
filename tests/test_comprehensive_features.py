#!/usr/bin/env python3
"""
Comprehensive feature test suite for Minecraft Datapack Language (MDL)
Tests every feature mentioned in the language reference and CLI documentation.
"""

import unittest
import tempfile
import os
import json
import zipfile
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Import all MDL components
from minecraft_datapack_language.mdl_lexer_js import MDLLexer, TokenType
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_linter import MDLLinter
from minecraft_datapack_language.expression_processor import ExpressionProcessor
from minecraft_datapack_language.cli_build import build_mdl, _merge_mdl_files, _ast_to_pack
from minecraft_datapack_language.mdl_errors import MDLParserError, MDLLexerError, MDLSyntaxError


class TestBasicSyntaxFeatures(unittest.TestCase):
    """Test all basic syntax features from language reference"""
    
    def test_pack_declaration(self):
        """Test pack declaration with all variations"""
        test_cases = [
            'pack "test" "description" 82;',
            'pack "my_pack" "A test pack" 15;',
            'pack "complex_name_123" "Complex description with spaces" 82;'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIn('pack', ast)
                self.assertIn('name', ast['pack'])
                self.assertIn('description', ast['pack'])
                self.assertIn('pack_format', ast['pack'])
    
    def test_namespace_declaration(self):
        """Test namespace declaration"""
        code = 'namespace "test";'
        ast = parse_mdl_js(code)
        self.assertIn('namespace', ast)
        self.assertEqual(ast['namespace']['name'], 'test')
    
    def test_variable_declarations(self):
        """Test all variable declaration types and scopes"""
        test_cases = [
            # Basic variable declarations
            'var num counter = 0;',
            'var num playerScore = 100;',
            'var num health = 20;',
            
            # Global scope variables
            'var num globalCounter scope<global> = 0;',
            'var num serverTimer scope<global> = 0;',
            
            # Player-specific scope (default)
            'var num playerHealth = 20;',  # Should default to player scope
            'var num playerScore = 0;',    # Should default to player scope
            
            # Team-specific scope
            'var num teamScore scope<@a[team=red]> = 0;',
            'var num blueTeamScore scope<@a[team=blue]> = 0;',
            
            # Custom entity scope
            'var num entityCounter scope<@e[type=armor_stand,tag=something,limit=1]> = 0;'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIn('variables', ast)
                self.assertGreater(len(ast['variables']), 0)
    
    def test_variable_assignments(self):
        """Test variable assignment operations"""
        test_cases = [
            'counter = 42;',
            'playerScore = playerScore + 10;',
            'health = health - 5;',
            'globalTimer = globalTimer + 1;',
            'teamScore = teamScore * 2;',
            'counter = $counter$ + 1;'  # Variable substitution in assignment
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                # These should parse without errors
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestVariableSubstitutionFeatures(unittest.TestCase):
    """Test variable substitution in various contexts"""
    
    def test_variable_substitution_in_strings(self):
        """Test variable substitution in say commands"""
        test_cases = [
            'say Counter: $counter$;',
            'say Score: $playerScore$;',
            'say Health: $health$;',
            'say "Counter: $counter$";',  # With quotes
            'say "Score: $playerScore$";'  # With quotes
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_variable_substitution_in_tellraw(self):
        """Test variable substitution in tellraw commands"""
        test_cases = [
            'tellraw @a {"text":"Score: $playerScore$","color":"gold"};',
            'tellraw @a {"text":"Counter: $counter$","color":"green"};',
            'tellraw @a {"text":"Health: $health$","color":"red"};',
            'tellraw @a {"text":"Timer: $globalTimer$","color":"blue"};'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_variable_substitution_in_conditions(self):
        """Test variable substitution in conditional expressions"""
        test_cases = [
            'if "$playerScore$ > 100" { say "High score!"; }',
            'if "$health$ < 10" { say "Low health!"; }',
            'if "$counter$ == 0" { say "Counter is zero"; }',
            'while "$globalTimer$ < 10" { globalTimer = $globalTimer$ + 1; }'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestFunctionFeatures(unittest.TestCase):
    """Test function declaration and calling features"""
    
    def test_basic_function_declaration(self):
        """Test basic function declarations"""
        code = '''
        function "test_function" {
            say "Hello World";
            tellraw @a {"text":"Welcome!","color":"green"};
        }
        '''
        ast = parse_mdl_js(code)
        self.assertIn('functions', ast)
        self.assertEqual(len(ast['functions']), 1)
        self.assertEqual(ast['functions'][0]['name'], 'test_function')
    
    def test_function_calls(self):
        """Test function calling syntax"""
        test_cases = [
            'function "namespace:function_name";',
            'function "test:main";',
            'function "game:start";'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_scoped_function_calls(self):
        """Test function calls with scope selectors"""
        test_cases = [
            'function "namespace:function_name<@a>";',           # All players
            'function "namespace:function_name<@s>";',           # Current player
            'function "namespace:function_name<@a[team=red]>";', # Red team players
            'function "test:main<@a>";',                         # All players
            'function "game:start<@s>";'                         # Current player
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestControlStructuresFeatures(unittest.TestCase):
    """Test all control structure features"""
    
    def test_if_statements(self):
        """Test if statement variations"""
        test_cases = [
            'if "$counter$ > 5" { say "Counter is high!"; }',
            'if "$health$ < 10" { say "Health is low!"; } else { say "Health is good"; }',
            'if "$score$ >= 100" { say "High score!"; }',
            'if "$timer$ <= 0" { say "Time\'s up!"; }',
            'if "$value$ == 42" { say "The answer!"; }',
            'if "$flag$ != 0" { say "Flag is set!"; }'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_while_loops(self):
        """Test while loop variations"""
        test_cases = [
            'while "$counter$ < 10" { counter = $counter$ + 1; say "Counter: $counter$"; }',
            'while "$timer$ > 0" { timer = $timer$ - 1; }',
            'while "$flag$ == 1" { say "Looping..."; flag = 0; }'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestRawBlockFeatures(unittest.TestCase):
    """Test raw block functionality - the complex feature"""
    
    def test_basic_raw_blocks(self):
        """Test basic raw block syntax"""
        test_cases = [
            # Multi-line raw blocks
            '''
            $!raw
            scoreboard players set @s player_timer_enabled 1
            execute as @a run function mypack:increase_tick_per_player
            say "Raw commands bypass MDL syntax checking"
            raw!$
            ''',
            
            # Single-line raw commands
            '$!raw scoreboard players add @s player_tick_counter 1 raw!$',
            
            # Mixed MDL and raw
            '''
            say "This is MDL syntax";
            $!raw scoreboard players set @s player_timer_enabled 1 raw!$
            say "Back to MDL syntax";
            '''
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_raw_blocks_with_complex_commands(self):
        """Test raw blocks with complex Minecraft commands"""
        test_cases = [
            # Complex execute commands
            '''
            $!raw
            execute as @a[team=red] at @s run particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
            execute as @a[team=blue] at @s run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
            raw!$
            ''',
            
            # Scoreboard operations
            '''
            $!raw
            scoreboard objectives add player_score dummy "Player Score"
            scoreboard players set @a player_score 0
            scoreboard players add @a player_score 10
            raw!$
            ''',
            
            # Effect and sound commands
            '''
            $!raw
            effect give @a minecraft:speed 10 1
            effect give @a minecraft:glowing 5 1 true
            playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1
            raw!$
            '''
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_raw_blocks_with_special_characters(self):
        """Test raw blocks with special characters that might conflict with MDL"""
        test_cases = [
            # Commands with quotes and special characters
            '''
            $!raw
            tellraw @a {"text":"Special chars: $@#%^&*()","color":"gold"}
            execute as @a run data modify entity @s CustomName set value "Complex Name"
            raw!$
            ''',
            
            # Commands with curly braces
            '''
            $!raw
            data modify entity @e[type=armor_stand,limit=1] CustomName set value {"text":"Test","color":"red"}
            raw!$
            '''
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestHooksFeatures(unittest.TestCase):
    """Test on_load and on_tick hooks"""
    
    def test_hooks_declaration(self):
        """Test hook declarations"""
        test_cases = [
            'on_load "namespace:function_name";',
            'on_tick "namespace:function_name";',
            'on_load "test:main";',
            'on_tick "game:tick";'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
                if 'on_load' in code:
                    self.assertIn('hooks', ast)
                    self.assertTrue(any(hook.get('hook_type') == 'load' for hook in ast['hooks']))
                if 'on_tick' in code:
                    self.assertIn('hooks', ast)
                    self.assertTrue(any(hook.get('hook_type') == 'tick' for hook in ast['hooks']))


class TestScopeSystemFeatures(unittest.TestCase):
    """Test the scope system - the 'weird' part"""
    
    def test_variable_scopes(self):
        """Test all variable scope types"""
        test_cases = [
            # No scope specified - should default to player-specific
            'var num playerScore = 0;',
            
            # Global scope
            'var num globalCounter scope<global> = 0;',
            
            # All players scope
            'var num allPlayersScore scope<@a> = 0;',
            
            # Team-specific scope
            'var num redTeamScore scope<@a[team=red]> = 0;',
            'var num blueTeamScore scope<@a[team=blue]> = 0;',
            
            # Custom entity scope
            'var num entityCounter scope<@e[type=armor_stand,tag=something,limit=1]> = 0;'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIn('variables', ast)
                self.assertGreater(len(ast['variables']), 0)
    
    def test_function_call_scopes(self):
        """Test function calls with different scopes"""
        test_cases = [
            # Execute as specific selector
            'function "namespace:function_name<@a>";',           # All players
            'function "namespace:function_name<@s>";',           # Current player
            'function "namespace:function_name<@a[team=red]>";', # Red team players
            'function "test:main<@a>";',                         # All players
            'function "game:start<@s>";'                         # Current player
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestSayTellrawFeatures(unittest.TestCase):
    """Test say and tellraw commands - the potentially weird ones"""
    
    def test_say_commands(self):
        """Test say command variations"""
        test_cases = [
            'say Hello, Minecraft!;',
            'say "Hello, World!";',
            'say Counter: $counter$;',
            'say "Score: $playerScore$";',
            'say Welcome to my datapack!;'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_tellraw_commands(self):
        """Test tellraw command variations"""
        test_cases = [
            'tellraw @a {"text":"Welcome!","color":"green"};',
            'tellraw @a {"text":"Score: $playerScore$","color":"gold"};',
            'tellraw @a {"text":"Counter: $counter$","color":"yellow"};',
            'tellraw @a {"text":"Health: $health$","color":"red"};',
            'tellraw @a {"text":"Timer: $globalTimer$","color":"blue"};'
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_complex_tellraw_commands(self):
        """Test complex tellraw commands with multiple components"""
        test_cases = [
            # Multiple text components
            '''
            tellraw @a [
                {"text":"Score: ","color":"green"},
                {"text":"$playerScore$","color":"gold"},
                {"text":" / 100","color":"gray"}
            ];
            ''',
            
            # With hover and click events
            '''
            tellraw @a {
                "text":"Click me!",
                "color":"blue",
                "hoverEvent":{"action":"show_text","contents":{"text":"Hover text"}},
                "clickEvent":{"action":"run_command","value":"/say clicked"}
            };
            '''
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestComplexIntegrationFeatures(unittest.TestCase):
    """Test complex integration scenarios combining multiple features"""
    
    def test_complete_game_example(self):
        """Test the complete game example from language reference"""
        code = '''
        pack "game" "Complete game example" 82;
        namespace "game";

        // Variables with different scopes
        var num score = 0;  // Defaults to player-specific scope
        var num level = 1;  // Defaults to player-specific scope
        var num globalTimer scope<global> = 0;

        // Main game function
        function "start_game" {
            score = 0;
            level = 1;
            say Game started! Level: $level$, Score: $score$;
        }

        // Level up function
        function "level_up" {
            if "$score$ >= 100" {
                level = level + 1;
                score = score - 100;
                say Level up! New level: $level$;
                tellraw @a {"text":"Player leveled up!","color":"gold"};
            }
        }

        // Timer function
        function "update_timer" {
            globalTimer = globalTimer + 1;
            if "$globalTimer$ >= 1200" {  // 60 seconds
                globalTimer = 0;
                say Time's up! Final score: $score$;
            }
        }

        // Raw commands for special effects
        function "special_effects" {
            $!raw
            effect give @a minecraft:glowing 10 1 true
            particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
            playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1
            raw!$
        }

        // Hooks
        on_load "game:start_game";
        on_tick "game:update_timer";
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
        
        # Check that all components are present
        self.assertIn('pack', ast)
        self.assertIn('namespace', ast)
        self.assertIn('variables', ast)
        self.assertIn('functions', ast)
        self.assertIn('hooks', ast)
        self.assertTrue(any(hook.get('hook_type') == 'load' for hook in ast['hooks']))
        self.assertTrue(any(hook.get('hook_type') == 'tick' for hook in ast['hooks']))
    
    def test_multi_namespace_project(self):
        """Test multi-namespace project with complex interactions"""
        code = '''
        pack "multi_namespace" "Multi-namespace test" 82;
        
        // Main namespace
        namespace "main";
        var num globalCounter scope<global> = 0;
        
        function "main_start" {
            globalCounter = 0;
            say "Starting multi-namespace test";
            function "ui:show_welcome<@a>";
        }
        
        // UI namespace
        namespace "ui";
        var num playerHealth = 20;
        
        function "show_welcome" {
            tellraw @a {"text":"Welcome!","color":"green"};
            if "$playerHealth$ < 10" {
                tellraw @a {"text":"Low health!","color":"red"};
            }
        }
        
        // Game namespace
        namespace "game";
        var num playerScore = 0;
        
        function "update_score" {
            playerScore = playerScore + 10;
            say Score: $playerScore$;
            function "ui:show_welcome<@s>";
        }
        
        on_load "main:main_start";
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
        
        # Check that multiple namespaces are handled
        self.assertIn('namespace', ast)
        self.assertIn('functions', ast)
        self.assertIn('variables', ast)


class TestCLIFeatures(unittest.TestCase):
    """Test CLI functionality"""
    
    def test_build_command_basic(self):
        """Test basic build command functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple MDL file
            mdl_file = Path(temp_dir) / "test.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "test" "Test pack" 82;
                namespace "test";
                function "main" {
                    say Hello, World!;
                }
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                build_mdl(str(mdl_file), str(output_dir), verbose=False)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                self.assertTrue((output_dir / "pack.mcmeta").exists())
                self.assertTrue((output_dir / "data" / "test" / "function" / "main.mcfunction").exists())
                
            except Exception as e:
                self.fail(f"Build command failed: {e}")
    
    def test_build_command_with_raw_blocks(self):
        """Test build command with raw blocks"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with raw blocks
            mdl_file = Path(temp_dir) / "test_raw.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "test" "Test pack with raw blocks" 82;
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
                build_mdl(str(mdl_file), str(output_dir), verbose=False)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
                # Check that raw commands are preserved
                with open(main_func, 'r') as f:
                    content = f.read()
                    self.assertIn("scoreboard players set @s test_score 1", content)
                    self.assertIn("execute as @a run say Raw command", content)
                
            except Exception as e:
                self.fail(f"Build command with raw blocks failed: {e}")
    
    def test_build_command_with_scopes(self):
        """Test build command with variable scopes"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with scoped variables
            mdl_file = Path(temp_dir) / "test_scopes.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "test" "Test pack with scopes" 82;
                namespace "test";
                
                var num playerScore = 0;  // Player-specific scope
                var num globalTimer scope<global> = 0;  // Global scope
                var num teamScore scope<@a[team=red]> = 0;  // Team scope
                
                function "main" {
                    playerScore = 100;
                    globalTimer = 0;
                    teamScore = 50;
                    say "Player score: $playerScore$";
                    say "Global timer: $globalTimer$";
                    say "Team score: $teamScore$";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                build_mdl(str(mdl_file), str(output_dir), verbose=False)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
            except Exception as e:
                self.fail(f"Build command with scopes failed: {e}")


class TestErrorHandlingFeatures(unittest.TestCase):
    """Test error handling for various scenarios"""
    
    def test_invalid_syntax_handling(self):
        """Test handling of invalid syntax"""
        invalid_codes = [
            'pack "test" description 82;',  # Missing quotes around description
            'var num counter = 0',          # Missing semicolon
            'function "test" { say "Hello"', # Missing closing brace
            'if "$counter$ > 5" { say "Test"', # Missing closing brace
            'say "Unterminated string',     # Unterminated string
        ]
        
        for code in invalid_codes:
            with self.assertRaises((MDLParserError, MDLLexerError, MDLSyntaxError)):
                parse_mdl_js(code)
    
    def test_undefined_variable_handling(self):
        """Test handling of undefined variables"""
        code = '''
        function "test" {
            say "Value: $undefined_var$";
        }
        '''
        
        # Should handle gracefully (linter will catch this)
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)


class TestLexerSpecificFeatures(unittest.TestCase):
    """Test specific lexer functionality"""
    
    def test_raw_block_lexing(self):
        """Test that raw blocks are properly tokenized"""
        lexer = MDLLexer()
        
        # Test raw block start
        tokens = lexer.lex('$!raw')
        raw_start_tokens = [t for t in tokens if t.type == TokenType.RAW_START]
        self.assertEqual(len(raw_start_tokens), 1)
        
        # Test raw block content
        code = '''
        $!raw
        scoreboard players set @s test 1
        say Raw command
        raw!$
        '''
        tokens = lexer.lex(code)
        raw_tokens = [t for t in tokens if t.type == TokenType.RAW]
        self.assertGreater(len(raw_tokens), 0)
        
        # Test raw block end
        tokens = lexer.lex('raw!$')
        raw_end_tokens = [t for t in tokens if t.type == TokenType.RAW_END]
        self.assertEqual(len(raw_end_tokens), 1)
    
    def test_say_command_lexing(self):
        """Test that say commands are properly tokenized"""
        lexer = MDLLexer()
        
        # Test basic say command
        tokens = lexer.lex('say "Hello, World!";')
        say_tokens = [t for t in tokens if t.type == TokenType.SAY]
        self.assertEqual(len(say_tokens), 1)
        self.assertIn('Hello, World!', say_tokens[0].value)
        
        # Test say command with variable substitution
        tokens = lexer.lex('say "Counter: $counter$";')
        say_tokens = [t for t in tokens if t.type == TokenType.SAY]
        self.assertEqual(len(say_tokens), 1)
        self.assertIn('$counter$', say_tokens[0].value)
    
    def test_variable_substitution_lexing(self):
        """Test that variable substitutions are properly tokenized"""
        lexer = MDLLexer()
        
        # Test basic variable substitution
        tokens = lexer.lex('counter = $counter$ + 1;')
        var_tokens = [t for t in tokens if t.type == TokenType.VARIABLE_SUB]
        self.assertEqual(len(var_tokens), 1)
        self.assertEqual(var_tokens[0].value, 'counter')
        
        # Test scoped variable substitution
        tokens = lexer.lex('globalTimer = $globalTimer<global>$ + 1;')
        var_tokens = [t for t in tokens if t.type == TokenType.VARIABLE_SUB]
        self.assertEqual(len(var_tokens), 1)
        self.assertEqual(var_tokens[0].value, 'globalTimer<global>')


def run_comprehensive_feature_tests():
    """Run all comprehensive feature tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBasicSyntaxFeatures,
        TestVariableSubstitutionFeatures,
        TestFunctionFeatures,
        TestControlStructuresFeatures,
        TestRawBlockFeatures,
        TestHooksFeatures,
        TestScopeSystemFeatures,
        TestSayTellrawFeatures,
        TestComplexIntegrationFeatures,
        TestCLIFeatures,
        TestErrorHandlingFeatures,
        TestLexerSpecificFeatures
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_comprehensive_feature_tests()
    exit(0 if success else 1)
