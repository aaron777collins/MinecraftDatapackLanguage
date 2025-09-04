#!/usr/bin/env python3

from minecraft_datapack_language.mdl_lexer import MDLLexer
from minecraft_datapack_language.mdl_parser import MDLParser

def test_raw_block():
    source = '$!raw\ngive @s minecraft:wooden_sword 1\nraw!$'
    print(f"Source: {repr(source)}")
    
    lexer = MDLLexer()
    try:
        tokens = list(lexer.lex(source))
        print(f"Generated {len(tokens)} tokens:")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token.type}: {repr(token.value)}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_scope_selector():
    source = 'on_tick epic:update_team_score<@a[team=adventurers]>;'
    print(f"\nSource: {repr(source)}")
    
    lexer = MDLLexer()
    try:
        tokens = list(lexer.lex(source))
        print(f"Generated {len(tokens)} tokens:")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token.type}: {repr(token.value)}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_parser():
    source = 'on_tick epic:update_team_score<@a[team=adventurers]>;'
    print(f"\nTesting parser with: {repr(source)}")
    
    parser = MDLParser()
    try:
        ast = parser.parse(source)
        print(f"Parsed AST with {len(ast.hooks)} hooks")
        if ast.hooks:
            hook = ast.hooks[0]
            print(f"  Hook type: {hook.hook_type}")
            print(f"  Hook namespace: {hook.namespace}")
            print(f"  Hook name: {hook.name}")
            print(f"  Hook scope: {hook.scope}")
    except Exception as e:
        print(f"Parser error: {e}")
        import traceback
        traceback.print_exc()

def test_complex_source():
    source = '''function epic:initialize_game<@s> {
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
        }'''
    
    print(f"\nTesting complex source with raw block:")
    print(f"Source: {repr(source)}")
    
    lexer = MDLLexer()
    try:
        tokens = list(lexer.lex(source))
        print(f"Generated {len(tokens)} tokens:")
        
        # Look for raw block tokens
        raw_tokens = [(i, t) for i, t in enumerate(tokens) if t.type == 'RAW_CONTENT']
        print(f"Raw content tokens found at positions: {raw_tokens}")
        
        for i, token in enumerate(tokens):
            if token.type in ['DOLLAR', 'EXCLAMATION', 'IDENTIFIER', 'RAW_CONTENT']:
                print(f"  {i}: {token.type}: {repr(token.value)}")
                
    except Exception as e:
        print(f"Lexer error: {e}")
        import traceback
        traceback.print_exc()

def test_raw_block_parsing():
    source = '$!raw\ngive @s minecraft:wooden_sword 1\nraw!$'
    print(f"\nTesting raw block parsing:")
    print(f"Source: {repr(source)}")
    
    parser = MDLParser()
    try:
        ast = parser.parse(source)
        print(f"Parsed AST with {len(ast.statements)} statements")
        if ast.statements:
            for i, stmt in enumerate(ast.statements):
                print(f"  Statement {i}: {type(stmt).__name__}")
                if hasattr(stmt, 'content'):
                    print(f"    Content: {repr(stmt.content)}")
    except Exception as e:
        print(f"Parser error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_function():
    source = '''function test:simple<@s> {
        score<@s> = 10;
        say "Hello!";
    }'''
    
    print(f"\nTesting simple function parsing:")
    print(f"Source: {repr(source)}")
    
    parser = MDLParser()
    try:
        ast = parser.parse(source)
        print(f"Parsed AST with {len(ast.functions)} functions")
        if ast.functions:
            func = ast.functions[0]
            print(f"  Function: {func.namespace}:{func.name}")
            print(f"  Scope: {func.scope}")
            print(f"  Body statements: {len(func.body)}")
            for i, stmt in enumerate(func.body):
                print(f"    Statement {i}: {type(stmt).__name__}")
                if hasattr(stmt, 'name'):
                    print(f"      Name: {stmt.name}")
                if hasattr(stmt, 'message'):
                    print(f"      Message: {stmt.message}")
    except Exception as e:
        print(f"Parser error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_raw_block()
    test_scope_selector()
    test_parser()
    test_complex_source()
    test_raw_block_parsing()
    test_simple_function()
