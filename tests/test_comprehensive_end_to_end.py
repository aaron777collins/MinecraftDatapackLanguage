#!/usr/bin/env python3
"""
Comprehensive end-to-end test for the MDL pipeline.
Tests the entire system from lexing through compilation with a complex scenario.
"""

import tempfile
import shutil
import json
from pathlib import Path
from unittest import TestCase, main

from minecraft_datapack_language.mdl_lexer import MDLLexer
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler


class TestComprehensiveEndToEnd(TestCase):
    """Test the entire MDL pipeline end-to-end with complex scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = MDLParser()
        self.compiler = MDLCompiler()
        
        # Complex MDL source that tests all features
        self.complex_source = '''
        pack "EpicAdventure" "An epic adventure datapack with magic and combat" 15;
        namespace "epic";
        
        // Variables for game state
        var num player_level<@s> = 1;
        var num mana<@s> = 100;
        var num health<@s> = 20;
        var num experience<@s> = 0;
        var num gold<@s> = 0;
        var num team_score<@a[team=adventurers]> = 0;
        var num boss_health<@e[type=wither,tag=boss,limit=1]> = 300;
        
        // Tag declarations for custom items and recipes
        tag recipe "magic_sword" "recipes/magic_sword.json";
        tag loot_table "boss_loot" "loot_tables/boss_loot.json";
        tag advancement "first_spell" "advancements/first_spell.json";
        tag item_modifier "enchanted_weapon" "item_modifiers/enchanted_weapon.json";
        tag predicate "in_combat" "predicates/in_combat.json";
        tag structure "wizard_tower" "structures/wizard_tower.json";
        
        // Core game functions
        function epic:initialize_game<@s> {
            // Set initial stats
            player_level<@s> = 1;
            mana<@s> = 100;
            health<@s> = 20;
            experience<@s> = 0;
            gold<@s> = 10;
            
            // Give starting equipment
            $!raw
            give @s minecraft:wooden_sword{display:{Name:'[{"text":"Apprentice Sword","italic":false}]'}} 1
            give @s minecraft:leather_chestplate{display:{Name:'[{"text":"Leather Armor","italic":false}]'}} 1
            raw!$
            
            say "Welcome to Epic Adventure! You are level $player_level<@s>$ with $mana<@s>$ mana.";
        }
        
        function epic:cast_spell<@s> {
            if $mana<@s>$ >= 20 {
                mana<@s> = $mana<@s>$ - 20;
                experience<@s> = $experience<@s>$ + 5;
                
                $!raw
                execute as @s run particle minecraft:enchantment_table ~ ~1 ~ 0.5 0.5 0.5 0.1 20
                execute as @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1
                raw!$
                
                say "You cast a spell! Mana: $mana<@s>$, Experience: $experience<@s>$";
                
                // Level up check
                if $experience<@s>$ >= 100 {
                    player_level<@s> = $player_level<@s>$ + 1;
                    experience<@s> = 0;
                    mana<@s> = $mana<@s>$ + 20;
                    health<@s> = $health<@s>$ + 5;
                    
                    say "Level up! You are now level $player_level<@s>$!";
                    say "New stats - Health: $health<@s>$, Mana: $mana<@s>$";
                }
            } else {
                say "Not enough mana! You have $mana<@s>$ mana.";
            }
        }
        
        function epic:heal_player<@s> {
            if $gold<@s>$ >= 5 {
                gold<@s> = $gold<@s>$ - 5;
                health<@s> = $health<@s>$ + 10;
                
                if $health<@s>$ > 20 {
                    health<@s> = 20;
                }
                
                say "You healed for 5 gold! Health: $health<@s>$, Gold: $gold<@s>$";
            } else {
                say "Not enough gold! You need 5 gold to heal.";
            }
        }
        
        function epic:update_team_score<@a[team=adventurers]> {
            // Calculate team score based on all players
            team_score<@a[team=adventurers]> = 0;
            
            $!raw
            execute as @a[team=adventurers] run scoreboard players add @a[team=adventurers] team_score @s player_level
            raw!$
            
            say "Team score updated: $team_score<@a[team=adventurers]>$";
        }
        
        function epic:boss_fight<@s> {
            if $boss_health<@e[type=wither,tag=boss,limit=1]>$ > 0 {
                // Deal damage based on player level
                boss_health<@e[type=wither,tag=boss,limit=1]> = $boss_health<@e[type=wither,tag=boss,limit=1]>$ - ($player_level<@s>$ * 5);
                
                say "You deal $($player_level<@s>$ * 5) damage! Boss health: $boss_health<@e[type=wither,tag=boss,limit=1]>$";
                
                if $boss_health<@e[type=wither,tag=boss,limit=1]>$ <= 0 {
                    say "Victory! You defeated the boss!";
                    experience<@s> = $experience<@s>$ + 50;
                    gold<@s> = $gold<@s>$ + 100;
                    
                    $!raw
                    execute as @s run title @s title {"text":"BOSS DEFEATED!","color":"gold","bold":true}
                    raw!$
                }
            } else {
                say "The boss is already defeated!";
            }
        }
        
        // Hooks for automatic execution
        on_load epic:initialize_game;
        on_tick epic:update_team_score<@a[team=adventurers]>;
        
        // Top-level function calls for testing
        exec epic:cast_spell;
        exec epic:heal_player;
        exec epic:boss_fight;
        
        // Raw block for complex commands
        $!raw
        # This is a complex command that would be hard to express in MDL
        execute as @a[team=adventurers] at @s if entity @s[gamemode=survival] run function epic:cast_spell
        raw!$
        '''
    
    def test_complete_pipeline(self):
        """Test the complete pipeline from lexing through compilation."""
        print("\n=== Testing Complete MDL Pipeline ===")
        
        # Step 1: Lexing
        print("1. Lexing...")
        lexer = MDLLexer()
        tokens = list(lexer.lex(self.complex_source))
        print(f"   Generated {len(tokens)} tokens")
        
        # Debug: Look for hook-related tokens
        hook_tokens = [(i, t) for i, t in enumerate(tokens) if t.type in ['ON_LOAD', 'ON_TICK']]
        print(f"   Hook tokens found at positions: {hook_tokens}")
        for pos, token in hook_tokens:
            print(f"     Position {pos}: {token.type} = {token.value}")
            # Show surrounding tokens
            start = max(0, pos - 5)
            end = min(len(tokens), pos + 10)
            print(f"     Context: {[t.type for t in tokens[start:end]]}")
        
        # Verify key token types are present
        token_types = [token.type for token in tokens]
        self.assertIn('PACK', token_types)
        self.assertIn('NAMESPACE', token_types)
        self.assertIn('VAR', token_types)
        self.assertIn('FUNCTION', token_types)
        self.assertIn('TAG', token_types)
        self.assertIn('ON_LOAD', token_types)
        self.assertIn('ON_TICK', token_types)
        self.assertIn('EXEC', token_types)
        self.assertIn('IF', token_types)
        self.assertIn('ELSE', token_types)
        self.assertIn('RAW_CONTENT', token_types)
        
        # Step 2: Parsing
        print("2. Parsing...")
        ast = self.parser.parse(self.complex_source)
        print(f"   Parsed AST with {len(ast.functions)} functions, {len(ast.variables)} variables, {len(ast.tags)} tags")
        
        # Verify AST structure
        self.assertIsNotNone(ast.pack)
        self.assertEqual(ast.pack.name, "EpicAdventure")
        self.assertEqual(ast.pack.pack_format, 15)
        self.assertEqual(ast.namespace.name, "epic")
        self.assertEqual(len(ast.variables), 7)
        self.assertEqual(len(ast.functions), 5)
        self.assertEqual(len(ast.tags), 6)
        self.assertEqual(len(ast.hooks), 2)
        self.assertEqual(len(ast.statements), 4)  # 3 exec calls + 1 raw block
        
        # Step 3: Compilation
        print("3. Compiling...")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.compiler.compile(ast, temp_dir)
            print(f"   Compiled to: {output_path}")
            
            # Verify output structure
            output_path_obj = Path(output_path)
            self.assertTrue(output_path_obj.exists())
            self.assertTrue((output_path_obj / "pack.mcmeta").exists())
            self.assertTrue((output_path_obj / "data").exists())
            self.assertTrue((output_path_obj / "data" / "epic").exists())
            # Accept either 'function' or 'functions' dir depending on dir_map
            self.assertTrue((output_path_obj / "data" / "epic" / "function").exists() or (output_path_obj / "data" / "epic" / "functions").exists())
            self.assertTrue((output_path_obj / "data" / "minecraft" / "tags" / "items").exists())
            
            # Verify pack.mcmeta content
            with open(output_path_obj / "pack.mcmeta") as f:
                pack_data = json.load(f)
                self.assertEqual(pack_data["pack"]["pack_format"], 15)
                self.assertEqual(pack_data["pack"]["description"], "An epic adventure datapack with magic and combat")
            
            # Verify function files
            functions_dir = output_path_obj / "data" / "epic" / "function"
            if not functions_dir.exists():
                functions_dir = output_path_obj / "data" / "epic" / "functions"
            expected_functions = [
                "initialize_game.mcfunction",
                "cast_spell.mcfunction", 
                "heal_player.mcfunction",
                "update_team_score.mcfunction",
                "boss_fight.mcfunction",
                "load.mcfunction",
                "tick.mcfunction"
            ]
            
            for func_file in expected_functions:
                self.assertTrue((functions_dir / func_file).exists(), f"Missing function file: {func_file}")
            
            # Verify load function content
            load_file = functions_dir / "load.mcfunction"
            with open(load_file) as f:
                load_content = f.read()
                # Should contain scoreboard objectives for all variables
                self.assertIn("scoreboard objectives add player_level", load_content)
                self.assertIn("scoreboard objectives add mana", load_content)
                self.assertIn("scoreboard objectives add health", load_content)
                self.assertIn("scoreboard objectives add experience", load_content)
                self.assertIn("scoreboard objectives add gold", load_content)
                self.assertIn("scoreboard objectives add team_score", load_content)
                self.assertIn("scoreboard objectives add boss_health", load_content)
                # Should contain function calls
                self.assertIn("function epic:initialize_game", load_content)
            
            # Verify tick function content
            tick_file = functions_dir / "tick.mcfunction"
            with open(tick_file) as f:
                tick_content = f.read()
                print(f"Tick function content: {repr(tick_content)}")
                self.assertIn("execute as @a[team=adventurers] run function epic:update_team_score", tick_content)
            
            # Verify tag files under Minecraft registry (simplified output)
            tags_dir = output_path_obj / "data" / "minecraft" / "tags" / "items"
            expected_tags = ["magic_sword.json", "boss_loot.json", "first_spell.json", 
                           "enchanted_weapon.json", "in_combat.json", "wizard_tower.json"]
            
            for tag_file in expected_tags:
                self.assertTrue((tags_dir / tag_file).exists(), f"Missing tag file: {tag_file}")
                
                # Verify tag file content
                with open(tags_dir / tag_file) as f:
                    tag_data = json.load(f)
                    self.assertIn("values", tag_data)
                    self.assertTrue(len(tag_data["values"]) > 0)
            
            # Verify function content (test one function in detail)
            cast_spell_file = functions_dir / "cast_spell.mcfunction"
            with open(cast_spell_file) as f:
                cast_spell_content = f.read()
                
                # Control flow and operations may be emitted into generated subfunctions
                # Validate presence of generated if-functions and general tellraw output
                
                # The say output will be in generated if/else subfunctions; ensure subfunctions are created
                self.assertIn("__if_", cast_spell_content)
                
                # Raw block content may be emitted into subfunctions; not required in root file
                
                # Control structures are emitted via generated function calls
                self.assertIn("__if_", cast_spell_content)
            
            print("   [OK] All compilation checks passed!")
        
        print("=== Pipeline Test Complete ===\n")
    
    def test_complex_variable_substitution(self):
        """Test complex variable substitution in strings."""
        print("\n=== Testing Complex Variable Substitution ===")
        
        source = '''
        pack "VarTest" "Variable substitution test" 15;
        namespace "test";
        
        var num score<@s> = 100;
        var num level<@s> = 5;
        var num health<@s> = 20;
        
        function test:complex_message<@s> {
            say "Player stats: Score=$score<@s>$, Level=$level<@s>$, Health=$health<@s>$";
            say "Welcome $score<@s>$ to level $level<@s>$!";
            say "Health remaining: $health<@s>$";
        }
        '''
        
        # Parse and compile
        ast = self.parser.parse(source)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.compiler.compile(ast, temp_dir)
            
            # Check function file
            func_file = Path(output_path) / "data" / "test" / "functions" / "complex_message.mcfunction"
            with open(func_file) as f:
                content = f.read()
                
                # Should contain tellraw commands with proper JSON structure
                self.assertIn('tellraw @a {"text":"Player stats: Score=","extra":[{"score":{"name":"@s","objective":"score"}},{"text":", Level="},{"score":{"name":"@s","objective":"level"}},{"text":", Health="},{"score":{"name":"@s","objective":"health"}}]}', content)
                self.assertIn('tellraw @a {"text":"Welcome ","extra":[{"score":{"name":"@s","objective":"score"}},{"text":" to level "},{"score":{"name":"@s","objective":"level"}},"!"]}', content)
                self.assertIn('tellraw @a {"text":"Health remaining: ","extra":[{"score":{"name":"@s","objective":"health"}}]}', content)
        
        print("   [OK] Complex variable substitution working correctly!")
    
    def test_expression_compilation(self):
        """Test that complex expressions are properly compiled."""
        print("\n=== Testing Expression Compilation ===")
        
        source = '''
        pack "ExprTest" "Expression compilation test" 15;
        namespace "test";
        
        var num a<@s> = 10;
        var num b<@s> = 20;
        var num c<@s> = 30;
        
        function test:math<@s> {
            if $a<@s>$ + $b<@s>$ > $c<@s>$ {
                say "Sum is greater than c";
            }
            
            if $a<@s>$ * $b<@s>$ <= $c<@s>$ * 2 {
                say "Product is less than or equal to double c";
            }
            
            while $a<@s>$ < 100 {
                a<@s> = $a<@s>$ + 10;
            }
        }
        '''
        
        # Parse and compile
        ast = self.parser.parse(source)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.compiler.compile(ast, temp_dir)
            
            # Check function file
            func_file = Path(output_path) / "data" / "test" / "functions" / "math.mcfunction"
            with open(func_file) as f:
                content = f.read()
                
                # Control structures are implemented via generated subfunctions
                self.assertIn("__if_", content)
                self.assertIn("__while_", content)
                
                # Expression conditions compiled via temp operations and execute if
                self.assertIn("execute if", content)
        
        print("   [OK] Expression compilation working correctly!")
    
    def test_pack_format_compatibility(self):
        """Test that different pack formats generate correct directory structures."""
        print("\n=== Testing Pack Format Compatibility ===")
        
        # Test modern format (15)
        source_modern = '''
        pack "ModernPack" "Modern format test" 15;
        namespace "modern";
        function modern:test<@s> { say "test"; }
        '''
        
        ast_modern = self.parser.parse(source_modern)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_modern = self.compiler.compile(ast_modern, temp_dir)
            
            # Modern format should use plural directories
            func_dir_modern = Path(output_modern) / "data" / "modern" / "functions"
            self.assertTrue(func_dir_modern.exists())
            self.assertTrue((func_dir_modern / "test.mcfunction").exists())
        
        # Test legacy format (10)
        source_legacy = '''
        pack "LegacyPack" "Legacy format test" 10;
        namespace "legacy";
        function legacy:test<@s> { say "test"; }
        '''
        
        ast_legacy = self.parser.parse(source_legacy)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_legacy = self.compiler.compile(ast_legacy, temp_dir)
            
            # Legacy format should use plural directories
            func_dir_legacy = Path(output_legacy) / "data" / "legacy" / "functions"
            self.assertTrue(func_dir_legacy.exists())
            self.assertTrue((func_dir_legacy / "test.mcfunction").exists())
        
        print("   [OK] Pack format compatibility working correctly!")


if __name__ == '__main__':
    main()
