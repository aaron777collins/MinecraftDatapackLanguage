#!/usr/bin/env python3
"""
Demo script showing the new MDL lexer in action.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minecraft_datapack_language'))

from mdl_lexer import MDLLexer, TokenType


def demo_basic_lexing():
    """Demonstrate basic lexing functionality."""
    print("=== Basic Lexing Demo ===")
    
    source = '''
pack "demo" "Demo pack" 82;
namespace "demo";

var num counter<@s> = 0;
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    print("Source code:")
    print(source)
    print("\nTokens generated:")
    for i, token in enumerate(tokens):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def demo_variable_substitution():
    """Demonstrate variable substitution lexing."""
    print("=== Variable Substitution Demo ===")
    
    source = '''
$player_score<@s>$
$team_score<@a[team=red]>$
$global_counter<@e[type=armor_stand,tag=mdl_server,limit=1]>$
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    print("Source code:")
    print(source)
    print("\nTokens generated:")
    for i, token in enumerate(tokens):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def demo_tag_declarations():
    """Demonstrate tag declaration lexing."""
    print("=== Tag Declarations Demo ===")
    
    source = '''
tag recipe "diamond_sword" "recipes/diamond_sword.json";
tag loot_table "epic_loot" "loot_tables/epic_loot.json";
tag advancement "first_spell" "advancements/first_spell.json";
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    print("Source code:")
    print(source)
    print("\nTokens generated:")
    for i, token in enumerate(tokens):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def demo_control_structures():
    """Demonstrate control structure lexing."""
    print("=== Control Structures Demo ===")
    
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
    
    print("Source code:")
    print(source)
    print("\nTokens generated:")
    for i, token in enumerate(tokens):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def demo_raw_blocks():
    """Demonstrate raw block lexing."""
    print("=== Raw Blocks Demo ===")
    
    source = '''
$!raw
scoreboard players set @s player_timer_enabled 1
execute as @a run function game:increase_tick_per_player
say "Raw commands bypass MDL syntax checking"
raw!$
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    print("Source code:")
    print(source)
    print("\nTokens generated:")
    for i, token in enumerate(tokens):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def demo_complex_example():
    """Demonstrate lexing a complex example."""
    print("=== Complex Example Demo ===")
    
    source = '''
pack "game" "Complex game example" 82;
namespace "game";

// Tag declarations
tag recipe "magic_wand" "recipes/magic_wand.json";
tag loot_table "magic_loot" "loot_tables/magic_loot.json";

var num player_level<@s> = 1;
var num player_exp<@s> = 0;

function "gain_experience" {
    player_exp<@s> = $player_exp<@s>$ + 10;
    
    if $player_exp<@s>$ >= 100 {
        player_level<@s> = $player_level<@s>$ + 1;
        player_exp<@s> = 0;
        say "Level up! New level: $player_level<@s>$!";
    }
}

on_tick "game:gain_experience";
'''
    
    lexer = MDLLexer()
    tokens = lexer.lex(source)
    
    print("Source code:")
    print(source)
    print("\nToken summary:")
    summary = lexer.get_token_summary()
    print(f"  Total tokens: {summary['total_tokens']}")
    print(f"  Lines processed: {summary['lines_processed']}")
    print(f"  Token counts: {summary['token_counts']}")
    
    print("\nFirst 20 tokens:")
    for i, token in enumerate(tokens[:20]):
        if token.type != TokenType.EOF:
            print(f"  {i:2d}: {token.type:15} '{token.value}' (line {token.line}, col {token.column})")
    
    print()


def main():
    """Run all demos."""
    print("🎮 MDL Lexer Demo\n")
    print("This demo shows how the new lexer tokenizes various MDL language constructs.\n")
    
    try:
        demo_basic_lexing()
        demo_variable_substitution()
        demo_tag_declarations()
        demo_control_structures()
        demo_raw_blocks()
        demo_complex_example()
        
        print("🎉 All demos completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
