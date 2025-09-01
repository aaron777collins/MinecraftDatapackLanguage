#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_comprehensive():
    """Test various edge cases and scenarios."""
    
    test_cases = [
        {
            "name": "Basic raw block",
            "source": '''pack test
function test {
    $!raw
    say Hello
    raw!$
}''',
            "expected_raw_tokens": 3
        },
        {
            "name": "Raw block with empty content",
            "source": '''pack test
function test {
    $!raw
    raw!$
}''',
            "expected_raw_tokens": 2  # No RAW token for empty content
        },
        {
            "name": "Raw block with only whitespace",
            "source": '''pack test
function test {
    $!raw
    
    raw!$
}''',
            "expected_raw_tokens": 2  # No RAW token for whitespace-only content
        },
        {
            "name": "Raw block with complex content",
            "source": '''pack test
function test {
    $!raw
    execute as @a at @s run say "Hello World!"
    execute as @a run give @s diamond_sword
    raw!$
}''',
            "expected_raw_tokens": 3
        },
        {
            "name": "Multiple raw blocks",
            "source": '''pack test
function test {
    $!raw
    say First block
    raw!$
    
    $!raw
    say Second block
    raw!$
}''',
            "expected_raw_tokens": 6
        },
        {
            "name": "Raw block with variables",
            "source": '''pack test
function test {
    var message = "Hello"
    $!raw
    say $message$
    raw!$
}''',
            "expected_raw_tokens": 3
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test {i+1}: {test_case['name']} ===")
        
        try:
            tokens = lex_mdl_js(test_case['source'])
            raw_tokens = [t for t in tokens if t.type in ['RAW_START', 'RAW', 'RAW_END']]
            
            print(f"Total tokens: {len(tokens)}")
            print(f"Raw tokens: {len(raw_tokens)}")
            
            # Check raw token count
            if len(raw_tokens) == test_case['expected_raw_tokens']:
                print("✓ Raw token count correct")
            else:
                print(f"✗ Expected {test_case['expected_raw_tokens']} raw tokens, got {len(raw_tokens)}")
                all_passed = False
            
            # Check token positions
            position_errors = []
            for token in tokens:
                if token.column <= 0:
                    position_errors.append(f"{token.type}: column {token.column}")
            
            if position_errors:
                print(f"✗ Position errors: {position_errors}")
                all_passed = False
            else:
                print("✓ All token positions valid")
            
            # Show raw tokens
            print("Raw tokens:")
            for token in raw_tokens:
                print(f"  {token.type}: {repr(token.value)} (line {token.line}, col {token.column})")
                
        except Exception as e:
            print(f"✗ Error during lexing: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print(f"\n=== Overall Result: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'} ===")
    return all_passed

if __name__ == "__main__":
    test_comprehensive()
