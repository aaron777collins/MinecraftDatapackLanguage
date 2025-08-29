#!/usr/bin/env python3

import re

def fix_selectors():
    with open('minecraft_datapack_language/expression_processor.py', 'r') as f:
        content = f.read()
    
    # Find the generate_binary_operation method
    method_start = content.find('def generate_binary_operation(self, operator: str, left: str, right: str, target: str, selector: str = "@s") -> str:')
    if method_start == -1:
        print("Could not find generate_binary_operation method")
        return
    
    # Find the end of the method (next method or end of file)
    method_end = content.find('\n    def ', method_start + 1)
    if method_end == -1:
        method_end = len(content)
    
    # Extract the method content
    before_method = content[:method_start]
    method_content = content[method_start:method_end]
    after_method = content[method_end:]
    
    # Replace all @s with {selector} in the method content
    # But be careful not to replace @s in string literals that are meant to be @s
    # We only want to replace @s in scoreboard commands
    
    # Pattern to match scoreboard commands with @s
    pattern = r'scoreboard players ([a-z]+) @s '
    replacement = r'scoreboard players \1 {selector} '
    
    method_content = re.sub(pattern, replacement, method_content)
    
    # Also replace @s in scoreboard operations
    pattern2 = r'@s ([a-zA-Z_][a-zA-Z0-9_]*)'
    replacement2 = r'{selector} \1'
    
    method_content = re.sub(pattern2, replacement2, method_content)
    
    # Write back the file
    new_content = before_method + method_content + after_method
    
    with open('minecraft_datapack_language/expression_processor.py', 'w') as f:
        f.write(new_content)
    
    print("Updated generate_binary_operation method")

if __name__ == "__main__":
    fix_selectors()
