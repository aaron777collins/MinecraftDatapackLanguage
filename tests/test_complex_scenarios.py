#!/usr/bin/env python3
"""
Complex scenario tests for the MDL pipeline.
Tests advanced language features and edge cases to ensure production readiness.
"""

import tempfile
import json
from pathlib import Path
from unittest import TestCase, main

from minecraft_datapack_language.mdl_lexer import MDLLexer
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler


class TestComplexScenarios(TestCase):
    """Test complex MDL scenarios and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = MDLParser()
        self.compiler = MDLCompiler()
        
        # Complex MDL source with advanced features
        self.complex_source = '''
        pack "ComplexTest" "Testing complex MDL features" 15;
        namespace "complex";
        
        var num player_health<@s> = 20;
        var num player_mana<@s> = 100;
        var num team_score<@a[team=red]> = 0;
        
        tag recipe "magic_sword" "recipes/magic_sword.json";
        tag loot_table "boss_loot" "loot_tables/boss_loot.json";
        
        function complex:combat<@s> {
            if $player_health<@s>$ > 10 {
                if $player_mana<@s>$ >= 20 {
                    player_mana<@s> = $player_mana<@s>$ - 20;
                    team_score<@a[team=red]> = $team_score<@a[team=red]>$ + 5;
                    say "Spell cast!";
                }
            }
        }
        
        on_load complex:combat<@s>;
        exec complex:combat<@s>;
        '''
    
    def test_complex_lexing(self):
        """Test that complex MDL source is properly tokenized."""
        print("\n=== Testing Complex Lexing ===")
        
        lexer = MDLLexer()
        tokens = list(lexer.lex(self.complex_source))
        print(f"   Generated {len(tokens)} tokens")
        
        # Verify all expected token types are present
        token_types = [token.type for token in tokens]
        
        # Keywords
        self.assertIn('PACK', token_types)
        self.assertIn('NAMESPACE', token_types)
        self.assertIn('VAR', token_types)
        self.assertIn('FUNCTION', token_types)
        self.assertIn('TAG', token_types)
        self.assertIn('ON_LOAD', token_types)
        self.assertIn('EXEC', token_types)
        self.assertIn('IF', token_types)
        
        print("   [OK] Complex lexing working correctly!")
    
    def test_complex_parsing(self):
        """Test that complex MDL source is properly parsed into AST."""
        print("\n=== Testing Complex Parsing ===")
        
        ast = self.parser.parse(self.complex_source)
        print(f"   Parsed AST with {len(ast.functions)} functions, {len(ast.variables)} variables, {len(ast.tags)} tags")
        
        # Verify AST structure
        self.assertIsNotNone(ast.pack)
        self.assertEqual(ast.pack.name, "ComplexTest")
        self.assertEqual(ast.pack.pack_format, 15)
        self.assertEqual(ast.namespace.name, "complex")
        
        # Should have variables, functions, tags, and hooks
        self.assertGreaterEqual(len(ast.variables), 3)
        self.assertGreaterEqual(len(ast.functions), 1)
        self.assertGreaterEqual(len(ast.tags), 2)
        self.assertEqual(len(ast.hooks), 1)
        self.assertGreaterEqual(len(ast.statements), 1)
        
        print("   [OK] Complex parsing working correctly!")
    
    def test_complex_compilation(self):
        """Test that complex MDL source compiles to functional datapack."""
        print("\n=== Testing Complex Compilation ===")
        
        ast = self.parser.parse(self.complex_source)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.compiler.compile(ast, temp_dir)
            print(f"   Compiled to: {output_path}")
            
            # Verify output structure
            output_path_obj = Path(output_path)
            self.assertTrue(output_path_obj.exists())
            self.assertTrue((output_path_obj / "pack.mcmeta").exists())
            self.assertTrue((output_path_obj / "data").exists())
            self.assertTrue((output_path_obj / "data" / "complex").exists())
            self.assertTrue((output_path_obj / "data" / "complex" / "functions").exists())
            self.assertTrue((output_path_obj / "data" / "minecraft" / "tags" / "items").exists())
            
            # Verify pack.mcmeta content
            with open(output_path_obj / "pack.mcmeta") as f:
                pack_data = json.load(f)
                self.assertEqual(pack_data["pack"]["pack_format"], 15)
                self.assertEqual(pack_data["pack"]["description"], "Testing complex MDL features")
            
            # Verify function files
            functions_dir = output_path_obj / "data" / "complex" / "functions"
            expected_functions = ["combat.mcfunction", "load.mcfunction"]
            
            for func_file in expected_functions:
                self.assertTrue((functions_dir / func_file).exists(), f"Missing function file: {func_file}")
            
            # Verify tag files
            tags_dir = output_path_obj / "data" / "minecraft" / "tags" / "items"
            expected_tags = ["magic_sword.json", "boss_loot.json"]
            
            for tag_file in expected_tags:
                self.assertTrue((tags_dir / tag_file).exists(), f"Missing tag file: {tag_file}")
                
                # Verify tag file content
                with open(tags_dir / tag_file) as f:
                    tag_data = json.load(f)
                    self.assertIn("values", tag_data)
                    self.assertTrue(len(tag_data["values"]) > 0)
            
            print("   [OK] Complex compilation working correctly!")
    
    def test_nested_control_structures(self):
        """Test deeply nested control structures compile correctly."""
        print("\n=== Testing Nested Control Structures ===")
        
        source = '''
        pack "NestedTest" "Testing nested control structures" 15;
        namespace "nested";
        
        var num a<@s> = 10;
        var num b<@s> = 20;
        
        function nested:logic<@s> {
            if $a<@s>$ > 5 {
                if $b<@s>$ > 15 {
                    say "All conditions met!";
                    while $a<@s>$ > 0 {
                        a<@s> = $a<@s>$ - 1;
                    }
                }
            }
        }
        '''
        
        ast = self.parser.parse(source)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.compiler.compile(ast, temp_dir)
            
            # Check function file
            func_file = Path(output_path) / "data" / "nested" / "functions" / "logic.mcfunction"
            with open(func_file) as f:
                content = f.read()
                
                # Should contain control structure comments
                self.assertIn("# if", content)
                self.assertIn("# while", content)
                
                # Should contain variable operations
                self.assertIn("scoreboard players set @s a", content)
        
        print("   [OK] Nested control structures working correctly!")
    
    def test_error_recovery(self):
        """Test that the system gracefully handles various error conditions."""
        print("\n=== Testing Error Recovery ===")
        
        # Test with valid source first
        valid_source = '''
        pack "ValidTest" "Testing valid source" 15;
        namespace "valid";
        
        var num test<@s> = 0;
        
        function valid:test<@s> {
            test<@s> = 5;
            say "This should work";
        }
        '''
        
        # This should work
        ast = self.parser.parse(valid_source)
        self.assertIsNotNone(ast)
        
        # Test with lexer error - invalid character
        lexer_error_source = '''
        pack "LexerTest" "Testing lexer errors" 15;
        namespace "lexer";
        
        var num test<@s> = 0;
        
        function lexer:test<@s> {
            test<@s> = 5;
            say "This should work";
        }
        
        // Invalid character that should cause lexer error
        ~
        '''
        
        # This should raise a lexer error - test that error handling works
        from minecraft_datapack_language.mdl_errors import MDLLexerError
        
        with self.assertRaises(MDLLexerError) as context:
            self.parser.parse(lexer_error_source)
        
        # Verify the error message contains the expected content
        error_msg = str(context.exception)
        self.assertIn("Unknown character", error_msg)
        self.assertIn("~", error_msg)
        print(f"   [OK] Caught expected lexer error: {context.exception}")
        
        print("   [OK] Error recovery working correctly!")


if __name__ == '__main__':
    main()
