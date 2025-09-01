#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js

def test_lexer():
    # Test basic raw block functionality
    source = '''pack test
function test {
    $!raw
    say Hello, this is raw content!
    execute as @a run say More raw content
    raw!$
    
    var myVar = 42
}'''
    
    try:
        tokens = lex_mdl_js(source)
        print("Lexing successful!")
        print(f"Total tokens: {len(tokens)}")
        print("\nTokens:")
        for i, token in enumerate(tokens):
            print(f"{i:2d}: {token.type:15} | {repr(token.value):30} | line {token.line:2d}, col {token.column:2d}")
        
        # Check for raw block tokens
        raw_tokens = [t for t in tokens if t.type in ['RAW_START', 'RAW', 'RAW_END']]
        print(f"\nRaw block tokens found: {len(raw_tokens)}")
        for token in raw_tokens:
            print(f"  {token.type}: {repr(token.value)}")
            
    except Exception as e:
        print(f"Error during lexing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lexer()
