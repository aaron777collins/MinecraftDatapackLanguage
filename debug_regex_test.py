#!/usr/bin/env python3

import re

def test_regex():
    test_cases = [
        'say Hello, Minecraft !',
        'say Counter: $counter$',
        'say "Hello, World!"',
        'say Counter: $counter$;',
    ]
    
    for test_case in test_cases:
        print(f"Testing: '{test_case}'")
        
        # Test quoted pattern
        text_match = re.search(r'say "([^"]*)"', test_case)
        if text_match:
            print(f"  Quoted match: '{text_match.group(1)}'")
        else:
            # Test unquoted pattern
            text_match = re.search(r'say (.+?);?$', test_case)
            if text_match:
                text_content = text_match.group(1).rstrip(';')
                print(f"  Unquoted match: '{text_content}'")
            else:
                print(f"  No match found")

if __name__ == "__main__":
    test_regex()
