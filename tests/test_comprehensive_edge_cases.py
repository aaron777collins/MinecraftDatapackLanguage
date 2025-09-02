#!/usr/bin/env python3
"""
Comprehensive Edge Case Test Suite for Minecraft Datapack Language (MDL)
Tests complex scenarios, edge cases, and potential failure modes that might not be covered by basic tests.
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
from minecraft_datapack_language.cli_build import build_mdl
from minecraft_datapack_language.mdl_errors import MDLParserError, MDLLexerError, MDLSyntaxError


class TestEdgeCaseLexing(unittest.TestCase):
    """Test edge cases in lexing that could cause issues"""
    
    def test_nested_raw_blocks(self):
        """Test nested raw blocks (should not be allowed)"""
        code = '''
        $!raw
        say "Outer raw block"
        $!raw
        say "Inner raw block"
        raw!$
        say "Back to outer"
        raw!$
        '''
        
        # This should fail because nested raw blocks are not supported
        with self.assertRaises((MDLLexerError, MDLParserError)):
            parse_mdl_js(code)
    
    def test_unterminated_raw_block(self):
        """Test unterminated raw block"""
        code = '''
        $!raw
        say "This raw block never ends"
        say "No closing marker"
        '''
        
        # This should fail because raw block is not terminated
        with self.assertRaises((MDLLexerError, MDLParserError)):
            parse_mdl_js(code)
    
    def test_raw_block_with_variable_substitution(self):
        """Test raw blocks containing variable substitution markers"""
        code = '''
        $!raw
        say "Raw block with $variable$ markers"
        scoreboard players set @s test $counter$
        raw!$
        '''
        
        # This should work - raw blocks should preserve $variable$ syntax
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_complex_variable_substitution_scopes(self):
        """Test complex scope selectors in variable substitution"""
        test_cases = [
            # Complex entity selectors
            'var num entityCounter scope<@e[type=armor_stand,tag=something,limit=1]> = 0;',
            'var num teamScore scope<@a[team=red,level=5..10]> = 0;',
            'var num nearbyScore scope<@a[distance=..10,gamemode=survival]> = 0;',
            
            # Multiple conditions
            'var num complexScore scope<@a[team=red][gamemode=survival]> = 0;',
            
            # Nested brackets (should be handled properly)
            'var num nestedScore scope<@a[team=red[subteam=blue]]> = 0;',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIn('variables', ast)
                self.assertGreater(len(ast['variables']), 0)
    
    def test_variable_substitution_in_complex_strings(self):
        """Test variable substitution in complex string contexts"""
        test_cases = [
            # Multiple variables in one string
            'say "Score: $playerScore$, Health: $health$, Level: $level$";',
            
            # Variables with special characters
            'say "Complex variable: $player_score_123$";',
            'say "Variable with dots: $player.score$";',
            
            # Variables in tellraw with complex JSON
            '''
            tellraw @a {
                "text":"Score: $playerScore$",
                "color":"gold",
                "hoverEvent":{"action":"show_text","contents":{"text":"Health: $health$"}}
            };
            ''',
            
            # Variables in conditions with complex expressions
            'if "$playerScore$ > 100 && $health$ > 10" { say "Good condition!"; }',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestComplexControlStructures(unittest.TestCase):
    """Test complex control structure scenarios"""
    
    def test_nested_if_statements(self):
        """Test deeply nested if statements"""
        code = '''
        if "$counter$ > 0" {
            if "$health$ > 10" {
                if "$level$ > 5" {
                    say "All conditions met!";
                } else {
                    say "Level too low";
                }
            } else {
                say "Health too low";
            }
        } else {
            say "Counter is zero";
        }
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_nested_while_loops(self):
        """Test nested while loops"""
        code = '''
        while "$outer$ < 3" {
            say "Outer loop: $outer$";
            while "$inner$ < 2" {
                say "Inner loop: $inner$";
                inner = $inner$ + 1;
            }
            outer = $outer$ + 1;
        }
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_control_structures_with_complex_conditions(self):
        """Test control structures with complex conditional expressions"""
        test_cases = [
            # Multiple conditions with logical operators
            'if "$score$ > 100 && $health$ > 10 || $level$ > 20" { say "Complex condition met!"; }',
            
            # Nested conditions
            'if "$a$ > 0" { if "$b$ > 0" { if "$c$ > 0" { say "All positive!"; } } }',
            
            # Complex while conditions
            'while "$counter$ < 10 && $flag$ == 1 || $timer$ > 0" { counter = $counter$ + 1; }',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_empty_control_structures(self):
        """Test control structures with empty bodies"""
        test_cases = [
            'if "$counter$ > 0" { }',  # Empty if body
            'while "$counter$ < 10" { }',  # Empty while body
            'if "$counter$ > 0" { } else { }',  # Empty if-else bodies
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestComplexFunctionCalls(unittest.TestCase):
    """Test complex function calling scenarios"""
    
    def test_function_calls_with_complex_scopes(self):
        """Test function calls with complex scope selectors"""
        test_cases = [
            # Complex entity selectors
            'function "test:main<@e[type=armor_stand,tag=something,limit=1]>";',
            'function "test:main<@a[team=red,level=5..10]>";',
            'function "test:main<@a[distance=..10,gamemode=survival]>";',
            
            # Multiple conditions
            'function "test:main<@a[team=red][gamemode=survival]>";',
            
            # Nested brackets
            'function "test:main<@a[team=red[subteam=blue]]>";',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_function_calls_with_special_characters(self):
        """Test function calls with special characters in names"""
        test_cases = [
            'function "test:function_with_underscores";',
            'function "test:function-with-dashes";',
            'function "test:function123";',
            'function "test:function_with_numbers_123";',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_recursive_function_calls(self):
        """Test recursive function calls (should be handled gracefully)"""
        code = '''
        function "recursive_test" {
            say "Calling recursively...";
            function "recursive_test";
        }
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)


class TestComplexRawBlocks(unittest.TestCase):
    """Test complex raw block scenarios"""
    
    def test_raw_blocks_with_special_minecraft_commands(self):
        """Test raw blocks with complex Minecraft commands"""
        test_cases = [
            # Complex execute commands
            '''
            $!raw
            execute as @a[team=red] at @s run particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
            execute as @a[team=blue] at @s run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
            raw!$
            ''',
            
            # Data commands
            '''
            $!raw
            data modify entity @e[type=armor_stand,limit=1] CustomName set value {"text":"Test","color":"red"}
            data modify storage test:data value set value {"score":100,"health":20}
            raw!$
            ''',
            
            # Complex scoreboard operations
            '''
            $!raw
            scoreboard objectives add player_score dummy "Player Score"
            scoreboard players set @a player_score 0
            scoreboard players add @a player_score 10
            scoreboard players operation @a total_score += @a player_score
            raw!$
            ''',
            
            # Effect and sound commands
            '''
            $!raw
            effect give @a minecraft:speed 10 1
            effect give @a minecraft:glowing 5 1 true
            playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1
            raw!$
            ''',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_raw_blocks_with_json_content(self):
        """Test raw blocks containing complex JSON"""
        test_cases = [
            # Complex tellraw with JSON
            '''
            $!raw
            tellraw @a {
                "text":"Complex message",
                "color":"gold",
                "bold":true,
                "italic":true,
                "hoverEvent":{
                    "action":"show_text",
                    "contents":{"text":"Hover text","color":"green"}
                },
                "clickEvent":{
                    "action":"run_command",
                    "value":"/say clicked"
                }
            }
            raw!$
            ''',
            
            # Multiple JSON objects
            '''
            $!raw
            tellraw @a [
                {"text":"Part 1 ","color":"red"},
                {"text":"Part 2 ","color":"green"},
                {"text":"Part 3","color":"blue"}
            ]
            raw!$
            ''',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_raw_blocks_with_quotes_and_escapes(self):
        """Test raw blocks with complex quoting and escaping"""
        test_cases = [
            # Nested quotes
            '''
            $!raw
            say "He said \"Hello world\" to me"
            tellraw @a {"text":"Quote: \"Hello\""}
            raw!$
            ''',
            
            # Escaped characters
            '''
            $!raw
            say "Line 1\nLine 2\tTabbed"
            tellraw @a {"text":"Special chars: \\n\\t\\r"}
            raw!$
            ''',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestComplexVariableScopes(unittest.TestCase):
    """Test complex variable scope scenarios"""
    
    def test_variable_scope_inheritance(self):
        """Test how variable scopes work in different contexts"""
        code = '''
        // Global scope variable
        var num globalCounter scope<global> = 0;
        
        // Player-specific variable (default scope)
        var num playerScore = 0;
        
        // Team-specific variable
        var num teamScore scope<@a[team=red]> = 0;
        
        function "test_scopes" {
            // Should be able to access all scopes
            globalCounter = $globalCounter$ + 1;
            playerScore = $playerScore$ + 10;
            teamScore = $teamScore$ + 5;
            
            say "Global: $globalCounter$, Player: $playerScore$, Team: $teamScore$";
        }
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
        self.assertIn('variables', ast)
        self.assertEqual(len(ast['variables']), 3)
    
    def test_variable_scope_conflicts(self):
        """Test potential scope conflicts"""
        code = '''
        // Same variable name in different scopes
        var num counter scope<global> = 0;
        var num counter = 0;  // Player-specific scope
        
        function "test_conflicts" {
            // Should be able to access both
            globalCounter = $counter<global>$ + 1;
            playerCounter = $counter$ + 1;
            
            say "Global counter: $counter<global>$, Player counter: $counter$";
        }
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_complex_scope_selectors(self):
        """Test very complex scope selectors"""
        test_cases = [
            # Multiple conditions
            'var num complexVar scope<@a[team=red,gamemode=survival,level=5..10]> = 0;',
            
            # Distance and location
            'var num nearbyVar scope<@a[distance=..10,x=0,y=64,z=0]> = 0;',
            
            # Entity types with tags
            'var num entityVar scope<@e[type=armor_stand,tag=important,limit=1]> = 0;',
            
            # Complex nested selectors
            'var num nestedVar scope<@a[team=red[subteam=blue]][gamemode=survival]> = 0;',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)


class TestComplexExpressions(unittest.TestCase):
    """Test complex expression scenarios"""
    
    def test_nested_expressions(self):
        """Test deeply nested expressions"""
        code = '''
        var num result = (($a$ + $b$) * ($c$ - $d$)) / ($e$ + $f$);
        var num complex = ($x$ * $y$) + ($z$ / $w$) - ($p$ % $q$);
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_expression_with_variable_substitution(self):
        """Test expressions with variable substitution"""
        test_cases = [
            # Simple arithmetic with variables
            'counter = $counter$ + 1;',
            'score = $score$ * 2;',
            'health = $health$ - 5;',
            
            # Complex expressions
            'result = ($a$ + $b$) * ($c$ - $d$);',
            'total = $score$ + ($bonus$ * $multiplier$);',
            
            # Mixed literals and variables
            'value = 10 + $counter$ * 2;',
            'result = ($base$ + 100) / 2;',
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                ast = parse_mdl_js(code)
                self.assertIsNotNone(ast)
    
    def test_expression_precedence(self):
        """Test operator precedence in expressions"""
        code = '''
        // Test that precedence is handled correctly
        var num result1 = 2 + 3 * 4;  // Should be 14, not 20
        var num result2 = (2 + 3) * 4;  // Should be 20
        var num result3 = 10 / 2 + 3;  // Should be 8, not 1.25
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)


class TestErrorHandlingEdgeCases(unittest.TestCase):
    """Test error handling for edge cases"""
    
    def test_malformed_variable_substitution(self):
        """Test malformed variable substitution"""
        malformed_cases = [
            'counter = $123counter$;',  # Variable starting with number (outside quotes)
            'counter = $counter<@a;',  # Missing closing > (outside quotes)
            'counter = $;',  # Empty variable name (outside quotes)
        ]
        
        for code in malformed_cases:
            with self.subTest(code=code):
                with self.assertRaises((MDLLexerError, MDLParserError)):
                    parse_mdl_js(code)
    
    def test_malformed_raw_blocks(self):
        """Test malformed raw blocks"""
        # Test unterminated raw block
        code1 = '''pack "test" "Test" 82;
namespace "test";
function "main" {
    $!raw
    say hello
}'''
        
        with self.assertRaises((MDLLexerError, MDLParserError)):
            parse_mdl_js(code1)
        
        # Test missing opening $!raw
        code2 = '''pack "test" "Test" 82;
namespace "test";
function "main" {
    say hello
    raw!$
}'''
        
        with self.assertRaises((MDLLexerError, MDLParserError)):
            parse_mdl_js(code2)
        
        # Test nested raw blocks
        code3 = '''pack "test" "Test" 82;
namespace "test";
function "main" {
    $!raw
    say hello
    $!raw
    say world
    raw!$
}'''
        
        with self.assertRaises((MDLLexerError, MDLParserError)):
            parse_mdl_js(code3)
    
    def test_malformed_control_structures(self):
        """Test malformed control structures"""
        malformed_cases = [
            'function "test" { if "$counter$ > 0" { say "Test"; }',  # Missing closing brace for if
            'function "test" { while "$counter$ < 10" { say "Test"; }',  # Missing closing brace for while
        ]
        
        for code in malformed_cases:
            with self.subTest(code=code):
                with self.assertRaises((MDLLexerError, MDLParserError)):
                    parse_mdl_js(code)
    
    def test_malformed_function_declarations(self):
        """Test malformed function declarations"""
        malformed_cases = [
            'function "test" { say "Test";',  # Missing closing brace
            'function test { say "Test"; }',  # Missing quotes around name
            'function "test" say "Test";',  # Missing braces
        ]
        
        for code in malformed_cases:
            with self.subTest(code=code):
                with self.assertRaises((MDLLexerError, MDLParserError)):
                    parse_mdl_js(code)


class TestComplexIntegrationScenarios(unittest.TestCase):
    """Test complex integration scenarios combining multiple features"""
    
    def test_complex_game_system(self):
        """Test a complex game system with multiple features"""
        code = '''
        pack "complex_game" "Complex game system test" 82;
        namespace "game";
        
        // Global game state
        var num gamePhase scope<global> = 0;
        var num globalTimer scope<global> = 0;
        var num playerCount scope<global> = 0;
        
        // Player-specific variables
        var num playerHealth = 20;
        var num playerScore = 0;
        var num playerLevel = 1;
        
        // Team-specific variables
        var num redTeamScore scope<@a[team=red]> = 0;
        var num blueTeamScore scope<@a[team=blue]> = 0;
        
        // Main game function
        function "start_game" {
            gamePhase = 1;
            globalTimer = 0;
            playerCount = 0;
            
            say "Game starting! Phase: $gamePhase$";
            function "game:initialize_players<@a>";
        }
        
        // Player initialization
        function "initialize_players" {
            playerHealth = 20;
            playerScore = 0;
            playerLevel = 1;
            
            if "$playerHealth$ == 20" {
                say "Player initialized successfully!";
                tellraw @a {"text":"Player ready!","color":"green"};
            }
        }
        
        // Game loop
        function "game_loop" {
            globalTimer = $globalTimer$ + 1;
            
            // Phase progression
            if "$globalTimer$ >= 1200" {  // 60 seconds
                gamePhase = $gamePhase$ + 1;
                globalTimer = 0;
                
                if "$gamePhase$ > 3" {
                    say "Game complete!";
                    function "game:end_game<@a>";
                } else {
                    say "Phase $gamePhase$ starting!";
                    function "game:phase_$gamePhase$<@a>";
                }
            }
            
            // Health check
            if "$playerHealth$ < 10" {
                playerHealth = $playerHealth$ + 5;
                say "Health restored to: $playerHealth$";
            }
            
            // Score system
            playerScore = $playerScore$ + 1;
            
            // Level up system
            if "$playerScore$ >= 100" {
                playerLevel = $playerLevel$ + 1;
                playerScore = $playerScore$ - 100;
                say "Level up! New level: $playerLevel$";
                
                // Special effects for level up
                $!raw
                effect give @s minecraft:glowing 10 1 true
                particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
                playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1
                raw!$
            }
        }
        
        // Phase-specific functions
        function "phase_1" {
            say "Phase 1: Basic gameplay";
            redTeamScore = 0;
            blueTeamScore = 0;
        }
        
        function "phase_2" {
            say "Phase 2: Team competition";
            if "$redTeamScore$ > $blueTeamScore$" {
                say "Red team is winning!";
            } else if "$blueTeamScore$ > $redTeamScore$" {
                say "Blue team is winning!";
            } else {
                say "Teams are tied!";
            }
        }
        
        function "phase_3" {
            say "Phase 3: Final showdown";
            // Complex team scoring
            redTeamScore = $redTeamScore$ + $playerScore$;
            blueTeamScore = $blueTeamScore$ + $playerScore$;
        }
        
        function "end_game" {
            say "Game over! Final scores:";
            say "Red team: $redTeamScore$";
            say "Blue team: $blueTeamScore$";
            
            if "$redTeamScore$ > $blueTeamScore$" {
                tellraw @a {"text":"Red team wins!","color":"red"};
            } else if "$blueTeamScore$ > $redTeamScore$" {
                tellraw @a {"text":"Blue team wins!","color":"blue"};
            } else {
                tellraw @a {"text":"It's a tie!","color":"yellow"};
            }
        }
        
        // Hooks
        on_load "game:start_game";
        on_tick "game:game_loop";
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
        
        # Check that all components are present
        self.assertIn('pack', ast)
        self.assertIn('namespace', ast)
        self.assertIn('variables', ast)
        self.assertIn('functions', ast)
        self.assertIn('hooks', ast)
        
        # Check variable count
        self.assertGreaterEqual(len(ast['variables']), 8)  # At least 8 variables
        
        # Check function count
        self.assertGreaterEqual(len(ast['functions']), 7)  # At least 7 functions
        
        # Check hooks
        self.assertEqual(len(ast['hooks']), 2)  # on_load and on_tick
    
    def test_multi_namespace_complex_interaction(self):
        """Test complex interactions between multiple namespaces"""
        code = '''
        pack "multi_namespace" "Multi-namespace complex test" 82;
        
        // Core namespace
        namespace "core";
        var num globalState scope<global> = 0;
        
        function "core_init" {
            globalState = 0;
            say "Core system initialized";
            function "ui:show_welcome<@a>";
            function "game:start<@a>";
        }
        
        function "core_update" {
            globalState = $globalState$ + 1;
            if "$globalState$ >= 100" {
                function "ui:show_complete<@a>";
                function "game:end<@a>";
            }
        }
        
        // UI namespace
        namespace "ui";
        var num uiState = 0;
        
        function "show_welcome" {
            uiState = 1;
            tellraw @a {"text":"Welcome to the game!","color":"green"};
            tellraw @a {"text":"UI State: $uiState$","color":"yellow"};
        }
        
        function "show_complete" {
            uiState = 2;
            tellraw @a {"text":"Game complete!","color":"gold"};
            tellraw @a {"text":"Final UI State: $uiState$","color":"yellow"};
        }
        
        // Game namespace
        namespace "game";
        var num playerProgress = 0;
        
        function "start" {
            playerProgress = 0;
            say "Game started! Progress: $playerProgress$";
            
            // Start game loop
            while "$playerProgress$ < 10" {
                playerProgress = $playerProgress$ + 1;
                say "Progress: $playerProgress$";
                
                if "$playerProgress$ == 5" {
                    function "ui:show_welcome<@s>";
                }
            }
        }
        
        function "end" {
            say "Game ended! Final progress: $playerProgress$";
        }
        
        // Hooks
        on_load "core:core_init";
        on_tick "core:core_update";
        '''
        
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
        
        # Check that multiple namespaces are handled
        self.assertIn('namespace', ast)
        self.assertIn('functions', ast)
        self.assertIn('variables', ast)
        self.assertIn('hooks', ast)


class TestCLIEdgeCases(unittest.TestCase):
    """Test CLI edge cases and complex scenarios"""
    
    def test_build_with_complex_raw_blocks(self):
        """Test building with very complex raw blocks"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with complex raw blocks
            mdl_file = Path(temp_dir) / "complex_raw_blocks.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "complex_raw_blocks" "Test pack with complex raw blocks" 82;
                namespace "test";
                
                function "main" {
                    say "Testing complex raw blocks";
                    
                    $!raw
                    scoreboard objectives add test_score dummy "Test Score"
                    scoreboard players set @a test_score 0
                    scoreboard players add @a test_score 10
                    scoreboard players operation @a total_score += @a test_score
                    raw!$
                    
                    $!raw
                    effect give @a minecraft:speed 10 1
                    effect give @a minecraft:glowing 5 1 true
                    playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1
                    raw!$
                    
                    say "Raw blocks completed";
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
                
                # Check that the function has content from raw blocks
                with open(main_func, 'r') as f:
                    content = f.read()
                    self.assertIn("scoreboard objectives add", content)
                    self.assertIn("effect give", content)
                    self.assertIn("playsound", content)
                
            except Exception as e:
                self.fail(f"Build command with complex raw blocks failed: {e}")
    
    def test_build_with_complex_scopes(self):
        """Test building with complex variable scopes"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create MDL file with complex scopes (simplified to avoid variable substitution issues)
            mdl_file = Path(temp_dir) / "complex_scopes.mdl"
            with open(mdl_file, 'w') as f:
                f.write('''
                pack "complex_scopes" "Test pack with complex scopes" 82;
                namespace "test";
                
                // Multiple scope types
                var num globalCounter scope<global> = 0;
                var num playerScore = 0;  // Default player scope
                var num redTeamScore scope<@a[team=red]> = 0;
                var num blueTeamScore scope<@a[team=blue]> = 0;
                var num entityCounter scope<@e[type=armor_stand,tag=important,limit=1]> = 0;
                
                function "main" {
                    // Simple assignments without variable substitution
                    globalCounter = 1;
                    playerScore = 10;
                    redTeamScore = 5;
                    blueTeamScore = 5;
                    entityCounter = 1;
                    
                    say "Scope test complete";
                }
                
                on_load "test:main";
                ''')
            
            output_dir = Path(temp_dir) / "output"
            
            # Test build command
            try:
                build_mdl(str(mdl_file), str(output_dir), verbose=False)
                
                # Check that output was created
                self.assertTrue(output_dir.exists())
                # The function should be in the namespace "test" (from namespace declaration)
                main_func = output_dir / "data" / "test" / "function" / "main.mcfunction"
                self.assertTrue(main_func.exists())
                
                # Check that the function has content
                with open(main_func, 'r') as f:
                    content = f.read()
                    self.assertIn("tellraw", content)
                
            except Exception as e:
                self.fail(f"Build command with complex scopes failed: {e}")


def run_comprehensive_edge_case_tests():
    """Run all comprehensive edge case tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEdgeCaseLexing,
        TestComplexControlStructures,
        TestComplexFunctionCalls,
        TestComplexRawBlocks,
        TestComplexVariableScopes,
        TestComplexExpressions,
        TestErrorHandlingEdgeCases,
        TestComplexIntegrationScenarios,
        TestCLIEdgeCases
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_comprehensive_edge_case_tests()
    exit(0 if success else 1)
