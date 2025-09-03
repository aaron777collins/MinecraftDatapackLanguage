#!/usr/bin/env python3
"""
Comprehensive test suite for the new MDL lexer.
Tests all language constructs defined in the language reference.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from minecraft_datapack_language.mdl_lexer import MDLLexer, TokenType


def test_basic_syntax():
    """Test basic syntax elements."""
    print("=== Testing Basic Syntax ===")
    
    source = '''
pack "test_pack" "Test pack description" 82;
namespace "test";
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    expected_types = [
        TokenType.PACK, TokenType.QUOTE, TokenType.IDENTIFIER, TokenType.QUOTE,
        TokenType.QUOTE, TokenType.IDENTIFIER, TokenType.QUOTE,
        TokenType.NUMBER, TokenType.SEMICOLON,
        TokenType.NAMESPACE, TokenType.QUOTE, TokenType.IDENTIFIER, TokenType.QUOTE, TokenType.SEMICOLON,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types), f"Expected {len(expected_types)} tokens, got {len(tokens)}"
    
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: expected {expected_type}, got {token.type}"
    
    print("+ Basic syntax tokens correctly identified")


def test_tag_declarations():
    """Test tag declarations."""
    print("=== Testing Tag Declarations ===")
    
    source = '''
tag recipe "diamond_sword" "recipes/diamond_sword.json";
tag loot_table "epic_loot" "loot_tables/epic_loot.json";
tag advancement "first_spell" "advancements/first_spell.json";
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Check that we have the right token types
    tag_tokens = [t for t in tokens if t.type == TokenType.TAG]
    recipe_tokens = [t for t in tokens if t.type == TokenType.RECIPE]
    loot_table_tokens = [t for t in tokens if t.type == TokenType.LOOT_TABLE]
    advancement_tokens = [t for t in tokens if t.type == TokenType.ADVANCEMENT]
    
    assert len(tag_tokens) == 3, f"Expected 3 TAG tokens, got {len(tag_tokens)}"
    assert len(recipe_tokens) == 1, f"Expected 1 RECIPE token, got {len(recipe_tokens)}"
    assert len(loot_table_tokens) == 1, f"Expected 1 LOOT_TABLE token, got {len(loot_table_tokens)}"
    assert len(advancement_tokens) == 1, f"Expected 1 ADVANCEMENT token, got {len(advancement_tokens)}"
    
    print("+ Tag declarations correctly tokenized")


def test_variable_declarations():
    """Test variable declarations and assignments."""
    print("=== Testing Variable Declarations ===")
    
    source = '''
var num player_score<@s> = 0;
var num global_counter<@a> = 100;
player_score<@s> = $player_score<@s>$ + 1;
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Check variable declaration tokens
    var_tokens = [t for t in tokens if t.type == TokenType.VAR]
    num_tokens = [t for t in tokens if t.type == TokenType.NUM]
    assign_tokens = [t for t in tokens if t.type == TokenType.ASSIGN]
    
    assert len(var_tokens) == 2, f"Expected 2 VAR tokens, got {len(var_tokens)}"
    assert len(num_tokens) == 2, f"Expected 2 NUM tokens, got {len(num_tokens)}"
    assert len(assign_tokens) == 3, f"Expected 3 ASSIGN tokens, got {len(assign_tokens)}"
    
    print("+ Variable declarations correctly tokenized")


def test_variable_substitution():
    """Test variable substitution syntax."""
    print("=== Testing Variable Substitution ===")
    
    source = '''
$player_score<@s>$
$team_score<@a[team=red]>$
$global_counter<@e[type=armor_stand,tag=mdl_server,limit=1]>$
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Check dollar tokens (should be 6 total: 3 opening, 3 closing)
    dollar_tokens = [t for t in tokens if t.type == TokenType.DOLLAR]
    assert len(dollar_tokens) == 6, f"Expected 6 DOLLAR tokens, got {len(dollar_tokens)}"
    
    # Check angle bracket tokens
    langle_tokens = [t for t in tokens if t.type == TokenType.LANGLE]
    rangle_tokens = [t for t in tokens if t.type == TokenType.RANGLE]
    assert len(langle_tokens) == 3, f"Expected 3 LANGLE tokens, got {len(langle_tokens)}"
    assert len(rangle_tokens) == 3, f"Expected 3 RANGLE tokens, got {len(rangle_tokens)}"
    
    print("+ Variable substitution correctly tokenized")


def test_functions():
    """Test function declarations and calls."""
    print("=== Testing Functions ===")
    
    source = '''
function game:start_game {
    player_score<@s> = 0;
}

exec game:start_game;
exec game:reset_player<@s>;
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    function_tokens = [t for t in tokens if t.type == TokenType.FUNCTION]
    exec_tokens = [t for t in tokens if t.type == TokenType.EXEC]
    colon_tokens = [t for t in tokens if t.type == TokenType.COLON]
    
    assert len(function_tokens) == 1, f"Expected 1 FUNCTION token, got {len(function_tokens)}"
    assert len(exec_tokens) == 2, f"Expected 2 EXEC tokens, got {len(exec_tokens)}"
    assert len(colon_tokens) == 3, f"Expected 3 COLON tokens, got {len(colon_tokens)}"
    
    print("+ Functions correctly tokenized")


def test_control_structures():
    """Test control structures."""
    print("=== Testing Control Structures ===")
    
    source = '''
if $player_score<@s>$ > 10 {
    exec game:celebrate;
} else {
    exec game:check_health;
}

while $counter<@s>$ > 0 {
    counter<@s> = $counter<@s>$ - 1;
}
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    if_tokens = [t for t in tokens if t.type == TokenType.IF]
    else_tokens = [t for t in tokens if t.type == TokenType.ELSE]
    while_tokens = [t for t in tokens if t.type == TokenType.WHILE]
    lbrace_tokens = [t for t in tokens if t.type == TokenType.LBRACE]
    rbrace_tokens = [t for t in tokens if t.type == TokenType.RBRACE]
    
    assert len(if_tokens) == 1, f"Expected 1 IF token, got {len(if_tokens)}"
    assert len(else_tokens) == 1, f"Expected 1 ELSE token, got {len(else_tokens)}"
    assert len(while_tokens) == 1, f"Expected 1 WHILE token, got {len(while_tokens)}"
    assert len(lbrace_tokens) == 3, f"Expected 3 LBRACE tokens, got {len(lbrace_tokens)}"
    assert len(rbrace_tokens) == 3, f"Expected 3 RBRACE tokens, got {len(rbrace_tokens)}"
    
    print("+ Control structures correctly tokenized")


def test_operators():
    """Test operators."""
    print("=== Testing Operators ===")
    
    source = '''
player_score<@s> = $x<@a>$ + $y<@p>$ * $z<@r>$;
if $score<@s>$ >= 100 {
    exec game:reward;
}
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    plus_tokens = [t for t in tokens if t.type == TokenType.PLUS]
    multiply_tokens = [t for t in tokens if t.type == TokenType.MULTIPLY]
    greater_equal_tokens = [t for t in tokens if t.type == TokenType.GREATER_EQUAL]
    greater_tokens = [t for t in tokens if t.type == TokenType.GREATER]
    
    assert len(plus_tokens) == 1, f"Expected 1 PLUS token, got {len(plus_tokens)}"
    assert len(multiply_tokens) == 1, f"Expected 1 MULTIPLY token, got {len(multiply_tokens)}"
    assert len(greater_equal_tokens) == 1, f"Expected 1 GREATER_EQUAL token, got {len(greater_equal_tokens)}"
    assert len(greater_tokens) == 1, f"Expected 1 GREATER token, got {len(greater_tokens)}"
    
    print("+ Operators correctly tokenized")


def test_hooks():
    """Test hooks."""
    print("=== Testing Hooks ===")
    
    source = '''
on_load game:start_game;
on_tick game:update_timer;
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    on_load_tokens = [t for t in tokens if t.type == TokenType.ON_LOAD]
    on_tick_tokens = [t for t in tokens if t.type == TokenType.ON_TICK]
    
    assert len(on_load_tokens) == 1, f"Expected 1 ON_LOAD token, got {len(on_load_tokens)}"
    assert len(on_tick_tokens) == 1, f"Expected 1 ON_TICK token, got {len(on_tick_tokens)}"
    
    print("+ Hooks correctly tokenized")


def test_raw_blocks():
    """Test raw blocks."""
    print("=== Testing Raw Blocks ===")
    
    source = '''
$!raw
scoreboard players set @s player_timer_enabled 1
execute as @a run function game:increase_tick_per_player
say "Raw commands bypass MDL syntax checking"
raw!$
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Check raw block markers
    dollar_tokens = [t for t in tokens if t.type == TokenType.DOLLAR]
    exclamation_tokens = [t for t in tokens if t.type == TokenType.EXCLAMATION]
    raw_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER and t.value == "raw"]
    
    assert len(dollar_tokens) == 2, f"Expected 2 DOLLAR tokens, got {len(dollar_tokens)}"
    assert len(exclamation_tokens) == 2, f"Expected 2 EXCLAMATION tokens, got {len(exclamation_tokens)}"
    assert len(raw_tokens) == 2, f"Expected 2 'raw' IDENTIFIER tokens, got {len(raw_tokens)}"
    
    print("+ Raw blocks correctly tokenized")


def test_comments():
    """Test comments."""
    print("=== Testing Comments ===")
    
    source = '''
// This is a single line comment
var num score<@s> = 0;  // Inline comment

/* This is a
   multi-line comment */
player_score<@s> = 5;
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Comments should be ignored, so we should only have the actual code tokens
    var_tokens = [t for t in tokens if t.type == TokenType.VAR]
    num_tokens = [t for t in tokens if t.type == TokenType.NUM]
    assign_tokens = [t for t in tokens if t.type == TokenType.ASSIGN]
    
    assert len(var_tokens) == 1, f"Expected 1 VAR token, got {len(var_tokens)}"
    assert len(num_tokens) == 1, f"Expected 1 NUM token, got {len(num_tokens)}"
    assert len(assign_tokens) == 2, f"Expected 2 ASSIGN tokens, got {len(assign_tokens)}"
    
    print("+ Comments correctly ignored")


def test_complex_example():
    """Test a complex example from the language reference."""
    print("=== Testing Complex Example ===")
    
    source = '''
pack "counter" "Counter example" 82;
namespace "counter";

// Tag declarations
tag recipe "diamond_sword" "recipes/diamond_sword.json";
tag loot_table "sword_loot" "loot_tables/sword_loot.json";

var num global_counter<@a> = 0;
var num player_counter<@s> = 0;

function "increment" {
    global_counter<@a> = $global_counter<@a>$ + 1;
    player_counter<@s> = $player_counter<@s>$ + 1;
    
    say "Player $player_counter<@s>$ just incremented the counter!";
}

on_load "counter:increment";
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    # Get token summary
    summary = lexer.get_token_summary()
    print(f"Total tokens: {summary['total_tokens']}")
    print(f"Token counts: {summary['token_counts']}")
    
    # Verify key tokens exist
    pack_tokens = [t for t in tokens if t.type == TokenType.PACK]
    namespace_tokens = [t for t in tokens if t.type == TokenType.NAMESPACE]
    function_tokens = [t for t in tokens if t.type == TokenType.FUNCTION]
    var_tokens = [t for t in tokens if t.type == TokenType.VAR]
    tag_tokens = [t for t in tokens if t.type == TokenType.TAG]
    
    assert len(pack_tokens) == 1, "Expected 1 PACK token"
    assert len(namespace_tokens) == 1, "Expected 1 NAMESPACE token"
    assert len(function_tokens) == 1, "Expected 1 FUNCTION token"
    assert len(var_tokens) == 2, "Expected 2 VAR tokens"
    assert len(tag_tokens) == 2, "Expected 2 TAG tokens"
    
    print("+ Complex example correctly tokenized")


def run_all_tests():
    """Run all test functions."""
    print("Starting MDL Lexer Tests...\n")
    
    try:
        test_basic_syntax()
        test_tag_declarations()
        test_variable_declarations()
        test_variable_substitution()
        test_functions()
        test_control_structures()
        test_operators()
        test_hooks()
        test_raw_blocks()
        test_comments()
        test_complex_example()
        
        print("\n🎉 All tests passed! The new lexer is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
