#!/usr/bin/env python3
"""
Comprehensive test suite for Minecraft Datapack Language (MDL)
Tests all aspects of the language directly without requiring the compiled mdl command.
"""

import unittest
import tempfile
import os
import json
import zipfile
from pathlib import Path

# Import all MDL components
from minecraft_datapack_language.mdl_lexer_js import MDLLexer, TokenType
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js
from minecraft_datapack_language.mdl_linter import MDLLinter
from minecraft_datapack_language.expression_processor import ExpressionProcessor
from minecraft_datapack_language.cli import _merge_mdl_files, _ast_to_pack


class TestMDLLexer(unittest.TestCase):
    """Test the MDL lexer functionality"""
    
    def test_basic_tokens(self):
        """Test basic token recognition"""
        lexer = MDLLexer()
        tokens = lexer.lex('pack "test" "description" 82;')
        
        # Check token types
        self.assertEqual(tokens[0].type, TokenType.PACK)
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[2].type, TokenType.STRING)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[4].type, TokenType.SEMICOLON)
    
    def test_variable_substitution(self):
        """Test variable substitution tokenization"""
        lexer = MDLLexer()
        tokens = lexer.lex('counter = $counter$ + 1;')  # Variable substitution outside string
        
        # Find variable substitution token
        var_tokens = [t for t in tokens if t.type == TokenType.VARIABLE_SUB]
        self.assertEqual(len(var_tokens), 1)
        self.assertEqual(var_tokens[0].value, 'counter')
    
    def test_operators(self):
        """Test operator tokenization"""
        lexer = MDLLexer()
        tokens = lexer.lex('counter = $counter$ + 1;')
        
        # Check for assignment and addition operators
        token_values = [t.value for t in tokens]
        self.assertIn('=', token_values)
        self.assertIn('+', token_values)
    
    def test_strings(self):
        """Test string tokenization"""
        lexer = MDLLexer()
        tokens = lexer.lex('say "Hello, World!";')
        
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(string_tokens), 1)
        self.assertEqual(string_tokens[0].value, '"Hello, World!"')  # Includes quotes
    
    def test_numbers(self):
        """Test number tokenization"""
        lexer = MDLLexer()
        tokens = lexer.lex('var num counter = 42;')
        
        number_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
        self.assertEqual(len(number_tokens), 1)
        self.assertEqual(number_tokens[0].value, '42')


class TestMDLParser(unittest.TestCase):
    """Test the MDL parser functionality"""
    
    def test_pack_declaration(self):
        """Test pack declaration parsing"""
        code = 'pack "test" "description" 82;'
        ast = parse_mdl_js(code)
        
        self.assertIn('pack', ast)
        self.assertEqual(ast['pack']['name'], 'test')
        self.assertEqual(ast['pack']['description'], 'description')
        self.assertEqual(ast['pack']['pack_format'], 82)
    
    def test_namespace_declaration(self):
        """Test namespace declaration parsing"""
        code = 'namespace "test";'
        ast = parse_mdl_js(code)
        
        self.assertIn('namespace', ast)
        self.assertEqual(ast['namespace'], 'test')
    
    def test_variable_declaration(self):
        """Test variable declaration parsing"""
        code = 'var num counter = 0;'
        ast = parse_mdl_js(code)
        
        self.assertIn('variables', ast)
        self.assertEqual(len(ast['variables']), 1)
        self.assertEqual(ast['variables'][0]['name'], 'counter')
        self.assertEqual(ast['variables'][0]['type'], 'num')
        self.assertEqual(ast['variables'][0]['value'], 0)
    
    def test_function_declaration(self):
        """Test function declaration parsing"""
        code = '''
        function "test_func" {
            say "Hello";
        }
        '''
        ast = parse_mdl_js(code)
        
        self.assertIn('functions', ast)
        self.assertEqual(len(ast['functions']), 1)
        self.assertEqual(ast['functions'][0]['name'], 'test_func')
        self.assertIn('statements', ast['functions'][0])
    
    def test_command_parsing(self):
        """Test command parsing within functions"""
        code = '''
        function "test" {
            say "Hello, World!";
            tellraw @a {"text":"Test"};
        }
        '''
        ast = parse_mdl_js(code)
        
        function = ast['functions'][0]
        statements = function['statements']
        
        # Check that commands are parsed
        command_statements = [s for s in statements if s.get('type') == 'Command']
        self.assertGreater(len(command_statements), 0)
    
    def test_variable_substitution_in_commands(self):
        """Test variable substitution in commands"""
        code = '''
        function "test" {
            say "Counter: $counter$";
        }
        '''
        ast = parse_mdl_js(code)
        
        function = ast['functions'][0]
        statements = function['statements']
        
        # Check that variable substitution is preserved
        command = statements[0]['command']
        self.assertIn('$counter$', command)
    
    def test_control_structures(self):
        """Test control structure parsing"""
        code = '''
        if "$test$ > 0" {
            say "Positive";
        }
        '''
        ast = parse_mdl_js(code)
        
        self.assertIn('control_structures', ast)
        self.assertEqual(len(ast['control_structures']), 1)
        self.assertEqual(ast['control_structures'][0]['type'], 'if')
    
    def test_while_loops(self):
        """Test while loop parsing"""
        code = '''
        while "$counter$ < 10" {
            counter = $counter$ + 1;
        }
        '''
        ast = parse_mdl_js(code)
        
        self.assertIn('control_structures', ast)
        while_loops = [cs for cs in ast['control_structures'] if cs['type'] == 'while']
        self.assertEqual(len(while_loops), 1)
    
    def test_registry_declarations(self):
        """Test registry declaration parsing"""
        code = '''
        recipe "test_recipe" {
            "type": "crafting_shaped",
            "pattern": ["XX", "XX"],
            "key": {"X": {"item": "minecraft:diamond"}},
            "result": {"item": "minecraft:diamond_block", "count": 1}
        }
        '''
        ast = parse_mdl_js(code)
        
        self.assertIn('registry', ast)
        self.assertIn('recipes', ast['registry'])
        self.assertEqual(len(ast['registry']['recipes']), 1)
    
    def test_on_load_on_tick(self):
        """Test on_load and on_tick parsing"""
        code = '''
        on_load "test:main";
        on_tick "test:tick";
        '''
        ast = parse_mdl_js(code)
        
        self.assertIn('on_load', ast)
        self.assertIn('on_tick', ast)
        self.assertEqual(ast['on_load'], 'test:main')
        self.assertEqual(ast['on_tick'], 'test:tick')


class TestMDLLinter(unittest.TestCase):
    """Test the MDL linter functionality"""
    
    def test_valid_syntax(self):
        """Test that valid syntax passes linting"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        var num counter = 0;
        function "main" {
            say "Hello";
        }
        '''
        
        linter = MDLLinter()
        errors = linter.lint(code)
        self.assertEqual(len(errors), 0)
    
    def test_invalid_pack_declaration(self):
        """Test invalid pack declaration detection"""
        code = 'pack "test" description "desc" 82;'  # Missing quotes around description
        
        linter = MDLLinter()
        errors = linter.lint(code)
        self.assertGreater(len(errors), 0)
    
    def test_missing_semicolon(self):
        """Test missing semicolon detection"""
        code = 'var num counter = 0'  # Missing semicolon
        
        linter = MDLLinter()
        errors = linter.lint(code)
        self.assertGreater(len(errors), 0)
    
    def test_undefined_variable(self):
        """Test undefined variable detection"""
        code = '''
        function "test" {
            say "Value: $undefined_var$";
        }
        '''
        
        linter = MDLLinter()
        errors = linter.lint(code)
        # Should detect undefined variable
        self.assertGreater(len(errors), 0)


class TestExpressionProcessor(unittest.TestCase):
    """Test the expression processor functionality"""
    
    def test_simple_expression(self):
        """Test simple expression processing"""
        processor = ExpressionProcessor()
        result = processor.process_expression('5 + 3')
        
        self.assertIsNotNone(result)
        self.assertIn('commands', result)
    
    def test_variable_expression(self):
        """Test variable expression processing"""
        processor = ExpressionProcessor()
        result = processor.process_expression('$counter$ + 1')
        
        self.assertIsNotNone(result)
        self.assertIn('commands', result)
    
    def test_complex_expression(self):
        """Test complex expression processing"""
        processor = ExpressionProcessor()
        result = processor.process_expression('($a$ + $b$) * 2')
        
        self.assertIsNotNone(result)
        self.assertIn('commands', result)


class TestCLIProcessing(unittest.TestCase):
    """Test CLI processing functionality"""
    
    def test_file_merging(self):
        """Test merging multiple MDL files"""
        file1_content = '''
        pack "test" "description" 82;
        namespace "main";
        recipe "main_recipe" {
            "type": "crafting_shaped",
            "pattern": ["X"],
            "key": {"X": {"item": "minecraft:diamond"}},
            "result": {"item": "minecraft:diamond_block"}
        }
        '''
        
        file2_content = '''
        namespace "other";
        function "other_func" {
            say "Hello from other";
        }
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f1:
            f1.write(file1_content)
            f1_path = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f2:
            f2.write(file2_content)
            f2_path = f2.name
        
        try:
            # Test merging
            ast = _merge_mdl_files([f1_path, f2_path], verbose=False)
            
            # Check that both namespaces are preserved
            self.assertIn('registry', ast)
            self.assertIn('recipes', ast['registry'])
            self.assertIn('functions', ast)
            
            # Check namespace assignment
            recipes = ast['registry']['recipes']
            functions = ast['functions']
            
            # Should have recipes in main namespace and functions in other namespace
            self.assertGreater(len(recipes), 0)
            self.assertGreater(len(functions), 0)
            
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)
    
    def test_ast_to_pack_conversion(self):
        """Test AST to Pack conversion"""
        ast = {
            'pack': {'name': 'test', 'description': 'Test pack', 'format': 82},
            'namespace': 'test',
            'variables': [{'name': 'counter', 'type': 'num', 'value': 0}],
            'functions': [{
                'name': 'main',
                'statements': [{'type': 'Command', 'command': 'say "Hello"'}]
            }],
            'on_load': 'test:main'
        }
        
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        self.assertEqual(pack.name, 'test')
        self.assertEqual(pack.description, 'Test pack')
        self.assertEqual(pack.format, 82)


class TestVariableSubstitution(unittest.TestCase):
    """Test variable substitution functionality"""
    
    def test_say_command_variable_substitution(self):
        """Test variable substitution in say commands"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        var num counter = 0;
        function "main" {
            say "Counter: $counter$";
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        # Check that the function was created
        self.assertIsNotNone(pack)
        
        # Check that the namespace was created
        namespace = pack.namespace('test')
        self.assertIsNotNone(namespace)
        
        # Check that the function was created
        function = namespace.function('main')
        self.assertIsNotNone(function)
        
        # Check the generated commands
        commands = function.commands
        self.assertGreater(len(commands), 0)
        
        # The say command should be converted to tellraw with JSON score
        tellraw_commands = [cmd for cmd in commands if cmd.startswith('tellraw')]
        self.assertGreater(len(tellraw_commands), 0)
        
        # Check for scoreboard score in the tellraw command
        score_commands = [cmd for cmd in tellraw_commands if '"score"' in cmd]
        self.assertGreater(len(score_commands), 0)
    
    def test_tellraw_command_variable_substitution(self):
        """Test variable substitution in tellraw commands"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        var num counter = 0;
        function "main" {
            tellraw @a {"text":"Counter: ","color":"green"};
            tellraw @a {"text":"$counter$","color":"yellow"};
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        # Check that commands are processed
        namespace = pack.namespace('test')
        function = namespace.function('main')
        commands = function.commands
        
        # Should have tellraw commands with score components
        score_commands = [cmd for cmd in commands if '"score"' in cmd]
        self.assertGreater(len(score_commands), 0)


class TestRegistryTypes(unittest.TestCase):
    """Test registry type functionality"""
    
    def test_recipe_registry(self):
        """Test recipe registry creation"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        recipe "test_recipe" {
            "type": "crafting_shaped",
            "pattern": ["XX", "XX"],
            "key": {"X": {"item": "minecraft:diamond"}},
            "result": {"item": "minecraft:diamond_block", "count": 1}
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        namespace = pack.namespace('test')
        
        # Check that recipe was created
        recipe_files = list(namespace.recipe_dir.glob('*.json'))
        self.assertGreater(len(recipe_files), 0)
        
        # Check recipe content
        with open(recipe_files[0], 'r') as f:
            recipe_data = json.load(f)
        
        self.assertEqual(recipe_data['type'], 'crafting_shaped')
        self.assertIn('pattern', recipe_data)
        self.assertIn('key', recipe_data)
        self.assertIn('result', recipe_data)
    
    def test_loot_table_registry(self):
        """Test loot table registry creation"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        loot_table "test_loot" {
            "type": "minecraft:block",
            "pools": [{
                "rolls": 1,
                "entries": [{
                    "type": "minecraft:item",
                    "name": "minecraft:diamond"
                }]
            }]
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        namespace = pack.namespace('test')
        
        # Check that loot table was created
        loot_files = list(namespace.loot_table_dir.glob('*.json'))
        self.assertGreater(len(loot_files), 0)
        
        # Check loot table content
        with open(loot_files[0], 'r') as f:
            loot_data = json.load(f)
        
        self.assertEqual(loot_data['type'], 'minecraft:block')
        self.assertIn('pools', loot_data)
    
    def test_advancement_registry(self):
        """Test advancement registry creation"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        advancement "test_advancement" {
            "display": {
                "title": {"text": "Test"},
                "description": {"text": "Test description"},
                "icon": {"item": "minecraft:diamond"}
            },
            "criteria": {
                "requirement": {
                    "trigger": "minecraft:impossible"
                }
            }
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        namespace = pack.namespace('test')
        
        # Check that advancement was created
        advancement_files = list(namespace.advancement_dir.glob('*.json'))
        self.assertGreater(len(advancement_files), 0)
        
        # Check advancement content
        with open(advancement_files[0], 'r') as f:
            advancement_data = json.load(f)
        
        self.assertIn('display', advancement_data)
        self.assertIn('criteria', advancement_data)


class TestControlStructures(unittest.TestCase):
    """Test control structure functionality"""
    
    def test_if_statement(self):
        """Test if statement processing"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        var num counter = 5;
        if "$counter$ > 0" {
            say "Positive";
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        namespace = pack.namespace('test')
        
        # Check that functions were created for the if statement
        function_files = list(namespace.function_dir.glob('*.mcfunction'))
        self.assertGreater(len(function_files), 0)
    
    def test_while_loop(self):
        """Test while loop processing"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        var num counter = 0;
        while "$counter$ < 5" {
            counter = $counter$ + 1;
            say "Counter: $counter$";
        }
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        namespace = pack.namespace('test')
        
        # Check that functions were created for the while loop
        function_files = list(namespace.function_dir.glob('*.mcfunction'))
        self.assertGreater(len(function_files), 0)


class TestMultiFileProjects(unittest.TestCase):
    """Test multi-file project functionality"""
    
    def test_namespace_preservation(self):
        """Test that namespaces are preserved across multiple files"""
        file1_content = '''
        pack "test" "description" 82;
        namespace "main";
        recipe "main_recipe" {
            "type": "crafting_shaped",
            "pattern": ["X"],
            "key": {"X": {"item": "minecraft:diamond"}},
            "result": {"item": "minecraft:diamond_block"}
        }
        '''
        
        file2_content = '''
        namespace "other";
        function "other_func" {
            say "Hello from other namespace";
        }
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f1:
            f1.write(file1_content)
            f1_path = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdl', delete=False) as f2:
            f2.write(file2_content)
            f2_path = f2.name
        
        try:
            ast = _merge_mdl_files([f1_path, f2_path], verbose=False)
            pack = _ast_to_pack(ast)
            
            # Check that both namespaces exist
            main_namespace = pack.namespace('main')
            other_namespace = pack.namespace('other')
            
            self.assertIsNotNone(main_namespace)
            self.assertIsNotNone(other_namespace)
            
            # Check that recipes are in main namespace
            main_recipe_files = list(main_namespace.recipe_dir.glob('*.json'))
            self.assertGreater(len(main_recipe_files), 0)
            
            # Check that functions are in other namespace
            other_function_files = list(other_namespace.function_dir.glob('*.mcfunction'))
            self.assertGreater(len(other_function_files), 0)
            
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)


class TestErrorHandling(unittest.TestCase):
    """Test error handling functionality"""
    
    def test_invalid_syntax(self):
        """Test handling of invalid syntax"""
        code = 'invalid syntax {'
        
        with self.assertRaises(Exception):
            parse_mdl_js(code)
    
    def test_missing_pack_declaration(self):
        """Test handling of missing pack declaration"""
        code = '''
        namespace "test";
        function "main" {
            say "Hello";
        }
        '''
        
        # Should not raise an error, but should handle gracefully
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)
    
    def test_undefined_variables(self):
        """Test handling of undefined variables"""
        code = '''
        pack "test" "description" 82;
        namespace "test";
        function "main" {
            say "Value: $undefined_var$";
        }
        '''
        
        # Should handle gracefully (linter will catch this)
        ast = parse_mdl_js(code)
        self.assertIsNotNone(ast)


class TestIntegration(unittest.TestCase):
    """Test integration scenarios"""
    
    def test_complete_datapack(self):
        """Test a complete datapack with all features"""
        code = '''
        pack "integration_test" "Integration test pack" 82;
        namespace "test";
        
        var num counter = 0;
        var num health = 20;
        
        recipe "test_recipe" {
            "type": "crafting_shaped",
            "pattern": ["X"],
            "key": {"X": {"item": "minecraft:diamond"}},
            "result": {"item": "minecraft:diamond_block"}
        }
        
        loot_table "test_loot" {
            "type": "minecraft:block",
            "pools": [{
                "rolls": 1,
                "entries": [{
                    "type": "minecraft:item",
                    "name": "minecraft:diamond"
                }]
            }]
        }
        
        function "main" {
            say "Starting integration test";
            counter = 0;
            while "$counter$ < 3" {
                counter = $counter$ + 1;
                say "Counter: $counter$";
            }
            if "$health$ > 10" {
                say "Health is good";
            }
            tellraw @a {"text":"Test complete!","color":"green"};
        }
        
        on_load "test:main";
        on_tick "test:main";
        '''
        
        ast = parse_mdl_js(code)
        pack = _ast_to_pack(ast)
        
        self.assertIsNotNone(pack)
        self.assertEqual(pack.name, 'integration_test')
        self.assertEqual(pack.description, 'Integration test pack')
        self.assertEqual(pack.format, 82)
        
        namespace = pack.namespace('test')
        
        # Check all components were created
        self.assertGreater(len(list(namespace.function_dir.glob('*.mcfunction'))), 0)
        self.assertGreater(len(list(namespace.recipe_dir.glob('*.json'))), 0)
        self.assertGreater(len(list(namespace.loot_table_dir.glob('*.json'))), 0)
        
        # Check that pack.mcmeta was created
        pack_mcmeta = pack.path / 'pack.mcmeta'
        self.assertTrue(pack_mcmeta.exists())
        
        # Check pack.mcmeta content
        with open(pack_mcmeta, 'r') as f:
            mcmeta_data = json.load(f)
        
        self.assertIn('pack', mcmeta_data)
        self.assertEqual(mcmeta_data['pack']['pack_format'], 82)
        self.assertEqual(mcmeta_data['pack']['description'], 'Integration test pack')


def run_comprehensive_tests():
    """Run all comprehensive tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestMDLLexer,
        TestMDLParser,
        TestMDLLinter,
        TestExpressionProcessor,
        TestCLIProcessing,
        TestVariableSubstitution,
        TestRegistryTypes,
        TestControlStructures,
        TestMultiFileProjects,
        TestErrorHandling,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_comprehensive_tests()
    exit(0 if success else 1)
