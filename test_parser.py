#!/usr/bin/env python3
"""
Comprehensive test suite for the MDL Parser
Tests all language constructs defined in language-reference.md
"""

import unittest
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.ast_nodes import *
from minecraft_datapack_language.mdl_errors import MDLParserError


class TestMDLParser(unittest.TestCase):
    """Test the MDL Parser implementation."""
    
    def setUp(self):
        """Set up parser for each test."""
        self.parser = MDLParser()
    
    def test_pack_declaration(self):
        """Test pack declaration parsing."""
        source = 'pack "MyPack" "A test datapack" 15;'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.pack, PackDeclaration)
        self.assertEqual(ast.pack.name, "MyPack")
        self.assertEqual(ast.pack.description, "A test datapack")
        self.assertEqual(ast.pack.pack_format, 15)
    
    def test_namespace_declaration(self):
        """Test namespace declaration parsing."""
        source = 'namespace "game";'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.namespace, NamespaceDeclaration)
        self.assertEqual(ast.namespace.name, "game")
    
    def test_tag_declaration(self):
        """Test tag declaration parsing."""
        source = 'tag recipe "crafting_table" "recipes/crafting_table.json";'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.tags), 1)
        tag = ast.tags[0]
        self.assertIsInstance(tag, TagDeclaration)
        self.assertEqual(tag.tag_type, "recipe")
        self.assertEqual(tag.name, "crafting_table")
        self.assertEqual(tag.file_path, "recipes/crafting_table.json")
    
    def test_variable_declaration(self):
        """Test variable declaration parsing."""
        source = 'var num score<@s> = 0;'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.variables), 1)
        var = ast.variables[0]
        self.assertIsInstance(var, VariableDeclaration)
        self.assertEqual(var.var_type, "num")
        self.assertEqual(var.name, "score")
        self.assertEqual(var.scope, "<@s>")
        self.assertIsInstance(var.initial_value, LiteralExpression)
        self.assertEqual(var.initial_value.value, 0.0)
    
    def test_variable_assignment(self):
        """Test variable assignment parsing."""
        source = 'score<@s> = 100;'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, VariableAssignment)
        self.assertEqual(stmt.name, "score")
        self.assertEqual(stmt.scope, "<@s>")
        self.assertIsInstance(stmt.value, LiteralExpression)
        self.assertEqual(stmt.value.value, 100.0)
    
    def test_function_declaration(self):
        """Test function declaration parsing."""
        source = '''
        function game:start_game<@s> {
            score<@s> = 0;
        }
        '''
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.functions), 1)
        func = ast.functions[0]
        self.assertIsInstance(func, FunctionDeclaration)
        self.assertEqual(func.namespace, "game")
        self.assertEqual(func.name, "start_game")
        self.assertEqual(func.scope, "<@s>")
        self.assertEqual(len(func.body), 1)
        self.assertIsInstance(func.body[0], VariableAssignment)
    
    def test_function_call(self):
        """Test function call parsing."""
        source = 'exec game:start_game<@s>;'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        call = ast.statements[0]
        self.assertIsInstance(call, FunctionCall)
        self.assertEqual(call.namespace, "game")
        self.assertEqual(call.name, "start_game")
        self.assertEqual(call.scope, "<@s>")
    
    def test_if_statement(self):
        """Test if statement parsing."""
        source = '''
        if $score<@s>$ > 0 {
            say "Score is positive";
        } else {
            say "Score is zero or negative";
        }
        '''
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        if_stmt = ast.statements[0]
        self.assertIsInstance(if_stmt, IfStatement)
        self.assertIsInstance(if_stmt.condition, BinaryExpression)
        self.assertEqual(len(if_stmt.then_body), 1)
        self.assertEqual(len(if_stmt.else_body), 1)
        self.assertIsInstance(if_stmt.then_body[0], SayCommand)
        self.assertIsInstance(if_stmt.else_body[0], SayCommand)
    
    def test_while_loop(self):
        """Test while loop parsing."""
        source = '''
        while $score<@s>$ > 0 {
            score<@s> = $score<@s>$ - 1;
        }
        '''
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        while_loop = ast.statements[0]
        self.assertIsInstance(while_loop, WhileLoop)
        self.assertIsInstance(while_loop.condition, BinaryExpression)
        self.assertEqual(len(while_loop.body), 1)
        self.assertIsInstance(while_loop.body[0], VariableAssignment)
    
    def test_hook_declaration(self):
        """Test hook declaration parsing."""
        source = 'on_load game:init;'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.hooks), 1)
        hook = ast.hooks[0]
        self.assertIsInstance(hook, HookDeclaration)
        self.assertEqual(hook.hook_type, "on_load")
        self.assertEqual(hook.namespace, "game")
        self.assertEqual(hook.name, "init")
        self.assertIsNone(hook.scope)
    
    def test_raw_block(self):
        """Test raw block parsing."""
        source = '''
        $!raw
        tellraw @a {"text":"Hello World","color":"green"}
        raw!$
        '''
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        raw = ast.statements[0]
        self.assertIsInstance(raw, RawBlock)
        self.assertIn("tellraw @a", raw.content)
        self.assertIn("Hello World", raw.content)
    
    def test_say_command(self):
        """Test say command parsing."""
        source = 'say "Hello $name<@s>$!";'
        ast = self.parser.parse(source)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        say = ast.statements[0]
        self.assertIsInstance(say, SayCommand)
        self.assertEqual(say.message, "Hello $name<@s>$!")
        self.assertEqual(len(say.variables), 1)
        self.assertEqual(say.variables[0].name, "name")
        self.assertEqual(say.variables[0].scope, "<@s>")
    
    def test_variable_substitution(self):
        """Test variable substitution parsing."""
        source = '$score<@s>$'
        # This would be part of an expression, so we'll test it in context
        source_with_context = 'var num temp<@s> = $score<@s>$;'
        ast = self.parser.parse(source_with_context)
        
        self.assertIsInstance(ast, Program)
        var = ast.variables[0]
        self.assertIsInstance(var.initial_value, VariableSubstitution)
        self.assertEqual(var.initial_value.name, "score")
        self.assertEqual(var.initial_value.scope, "<@s>")
    
    def test_complex_program(self):
        """Test parsing a complex program with multiple constructs."""
        source = '''
        pack "ComplexGame" "A complex game datapack" 15;
        namespace "game";
        
        tag recipe "sword" "recipes/sword.json";
        tag loot_table "chest" "loot_tables/chest.json";
        
        var num player_score<@s> = 0;
        var num game_state<@a> = 1;
        
        function game:start<@s> {
            player_score<@s> = 0;
            game_state<@a> = 1;
        }
        
        function game:update<@s> {
            if $player_score<@s>$ > 100 {
                say "You win!";
            } else {
                say "Keep going! Score: $player_score<@s>$";
            }
        }
        
        on_load game:init;
        on_tick game:update<@s>;
        
        exec game:start<@s>;
        
        $!raw
        scoreboard objectives add score dummy "Score"
        raw!$
        '''
        
        ast = self.parser.parse(source)
        
        # Verify all components are parsed
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.pack, PackDeclaration)
        self.assertIsInstance(ast.namespace, NamespaceDeclaration)
        self.assertEqual(len(ast.tags), 2)
        self.assertEqual(len(ast.variables), 2)
        self.assertEqual(len(ast.functions), 2)
        self.assertEqual(len(ast.hooks), 2)
        self.assertEqual(len(ast.statements), 2)  # exec + raw block
    
    def test_scope_selectors(self):
        """Test various scope selector formats."""
        test_cases = [
            ("<@s>", "<@s>"),
            ("<@a[team=red]>", "<@a[team=red]>"),
            ("<@p[distance=..5]>", "<@p[distance=..5]>"),
            ("<@r[gamemode=creative]>", "<@r[gamemode=creative]>"),
        ]
        
        for scope_input, expected in test_cases:
            with self.subTest(scope=scope_input):
                source = f'var num test{scope_input} = 0;'
                ast = self.parser.parse(source)
                var = ast.variables[0]
                self.assertEqual(var.scope, expected)
    
    def test_expression_parsing(self):
        """Test expression parsing capabilities."""
        # Test number literals
        source = 'var num x<@s> = 42;'
        ast = self.parser.parse(source)
        var = ast.variables[0]
        self.assertIsInstance(var.initial_value, LiteralExpression)
        self.assertEqual(var.initial_value.value, 42.0)
        self.assertEqual(var.initial_value.type, "number")
        
        # Test string literals
        source = 'var num x<@s> = "hello";'
        ast = self.parser.parse(source)
        var = ast.variables[0]
        self.assertIsInstance(var.initial_value, LiteralExpression)
        self.assertEqual(var.initial_value.value, "hello")
        self.assertEqual(var.initial_value.type, "string")
        
        # Test parenthesized expressions
        source = 'var num x<@s> = (42);'
        ast = self.parser.parse(source)
        var = ast.variables[0]
        self.assertIsInstance(var.initial_value, ParenthesizedExpression)
        self.assertIsInstance(var.initial_value.expression, LiteralExpression)
    
    def test_error_handling_missing_semicolon(self):
        """Test parser error handling for missing semicolon."""
        with self.assertRaises(MDLParserError) as context:
            self.parser.parse('var num x<@s> = 0')
        self.assertIn("Expected semicolon", str(context.exception))
    
    def test_error_handling_missing_brace(self):
        """Test parser error handling for missing closing brace."""
        with self.assertRaises(MDLParserError) as context:
            self.parser.parse('function game:test<@s> { var num x<@s> = 0;')
        self.assertIn("Expected '}' to end function body", str(context.exception))
    
    def test_error_handling_invalid_tag(self):
        """Test parser error handling for invalid tag type."""
        with self.assertRaises(MDLParserError) as context:
            self.parser.parse('tag invalid "name" "path";')
        self.assertIn("Expected tag type", str(context.exception))
    
    def test_valid_syntax(self):
        """Test that valid syntax doesn't raise errors."""
        try:
            self.parser.parse('var num x<@s> = 0;')
            print("✅ Valid syntax parsed successfully")
        except Exception as e:
            self.fail(f"Valid syntax should not raise an error: {e}")


if __name__ == '__main__':
    unittest.main()
