#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js, TokenType

def test_lexer():
    test_cases = [
        'say Counter: $counter$;',
        'say "Counter: $counter$";',
        'tellraw @a [{"text":"Counter: "},{"score":{"name":"@s","objective":"counter"}}];'
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Input: {test_case}")
        
        try:
            tokens = lex_mdl_js(test_case)
            print("Tokens:")
            for j, token in enumerate(tokens):
                print(f"  {j}: {token.type} = '{token.value}' (line {token.line}, col {token.column})")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_lexer()
