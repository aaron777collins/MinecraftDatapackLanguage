"""
CLI Utilities - Helper functions for the MDL CLI
"""

import os
import json
import re
from pathlib import Path
from typing import Any, List


def ensure_dir(path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)


def write_json(path: str, data: Any) -> None:
    """Write JSON data to a file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def _process_variable_substitutions(command: str, selector: str = "@s") -> str:
    """Process $variable$ and $variable<selector>$ substitutions in commands."""
    
    # Check if this is a tellraw command with JSON
    if command.strip().startswith('tellraw'):
        # Special handling for tellraw commands with variable substitutions
        try:
            # Find the JSON part of the tellraw command
            json_start = command.find('[')
            if json_start == -1:
                json_start = command.find('{')
            json_end = command.rfind(']') + 1
            if json_end == 0:
                json_end = command.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                prefix = command[:json_start]
                json_part = command[json_start:json_end]
                suffix = command[json_end:]
                
                # Parse the JSON to handle variable substitutions properly
                try:
                    data = json.loads(json_part)
                    
                    # Handle both single object and array formats
                    if isinstance(data, list):
                        # JSON array format - process each element
                        for item in data:
                            if isinstance(item, dict) and 'score' in item and 'name' in item['score']:
                                # Resolve scope selector in score components
                                name = item['score']['name']
                                if name == "global":
                                    item['score']['name'] = _resolve_selector("global")
                        
                        # Return the processed JSON
                        new_json = json.dumps(data)
                        return f"{prefix}{new_json}{suffix}"
                    
                    elif isinstance(data, dict) and 'text' in data and '$' in data['text']:
                        # Single object format with variable substitutions
                        # Split the text into parts before and after variables
                        text = data['text']
                        parts = []
                        current_pos = 0
                        
                        # Find all variable substitutions (including scoped ones)
                        var_pattern = r'\$([^$]+)\$'
                        for match in re.finditer(var_pattern, text):
                            start, end = match.span()
                            var_name = match.group(1)
                            
                            # Add text before the variable
                            if start > current_pos:
                                parts.append(text[current_pos:start])
                            
                            # Process the variable
                            if '<' in var_name and '>' in var_name:
                                # Scoped variable: $var<selector>$
                                base_name, scope = var_name.split('<', 1)
                                scope = scope.rstrip('>')
                                resolved_scope = _resolve_selector(scope)
                                parts.append(f"${{{base_name}}}")
                                # Replace the scope in the command
                                command = command.replace(f"${{{base_name}}}", f"${{{base_name}}}")
                            else:
                                # Simple variable: $var$
                                parts.append(f"${{{var_name}}}")
                            
                            current_pos = end
                        
                        # Add remaining text
                        if current_pos < len(text):
                            parts.append(text[current_pos:])
                        
                        # Update the text in the JSON
                        data['text'] = ''.join(parts)
                        new_json = json.dumps(data)
                        return f"{prefix}{new_json}{suffix}"
                    
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to simple substitution
                    pass
    
    # Simple variable substitution for non-JSON commands
    # Handle scoped variables: $variable<selector>$
    scoped_pattern = r'\$([^$<]+)<([^>]+)>\$'
    command = re.sub(scoped_pattern, lambda m: f"${{{m.group(1)}}}", command)
    
    # Handle simple variables: $variable$
    simple_pattern = r'\$([^$]+)\$'
    command = re.sub(simple_pattern, lambda m: f"${{{m.group(1)}}}", command)
    
    return command


def _convert_condition_to_minecraft_syntax(condition: str, selector: str = "@s") -> str:
    """Convert MDL condition syntax to Minecraft scoreboard syntax."""
    # Remove extra whitespace and normalize
    condition = condition.strip()
    
    # Handle common patterns
    if '==' in condition:
        var1, var2 = condition.split('==', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        # Check if var2 is a number
        try:
            value = int(var2)
            return f"score {var1} {selector} matches {value}"
        except ValueError:
            # Both are variables, compare them
            return f"score {var1} {selector} = {var2} {selector}"
    
    elif '!=' in condition:
        var1, var2 = condition.split('!=', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        try:
            value = int(var2)
            return f"score {var1} {selector} matches ..{value-1} {value+1}.."
        except ValueError:
            return f"score {var1} {selector} != {var2} {selector}"
    
    elif '>' in condition:
        var1, var2 = condition.split('>', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        try:
            value = int(var2)
            return f"score {var1} {selector} matches {value+1}.."
        except ValueError:
            return f"score {var1} {selector} > {var2} {selector}"
    
    elif '<' in condition:
        var1, var2 = condition.split('<', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        try:
            value = int(var2)
            return f"score {var1} {selector} matches ..{value-1}"
        except ValueError:
            return f"score {var1} {selector} < {var2} {selector}"
    
    elif '>=' in condition:
        var1, var2 = condition.split('>=', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        try:
            value = int(var2)
            return f"score {var1} {selector} matches {value}.."
        except ValueError:
            return f"score {var1} {selector} >= {var2} {selector}"
    
    elif '<=' in condition:
        var1, var2 = condition.split('<=', 1)
        var1 = var1.strip()
        var2 = var2.strip()
        
        try:
            value = int(var2)
            return f"score {var1} {selector} matches ..{value}"
        except ValueError:
            return f"score {var1} {selector} <= {var2} {selector}"
    
    # Default: treat as a variable that should be non-zero
    return f"score {condition} {selector} matches 1.."


def _find_mdl_files(directory: Path) -> List[Path]:
    """Find all .mdl files in a directory recursively."""
    mdl_files = []
    if directory.is_file():
        if directory.suffix == '.mdl':
            mdl_files.append(directory)
    else:
        for file_path in directory.rglob('*.mdl'):
            mdl_files.append(file_path)
    
    return sorted(mdl_files)


def _validate_selector(selector: str, variable_name: str) -> None:
    """Validate a selector string."""
    valid_selectors = ['@s', '@p', '@a', '@r', '@e', 'global']
    if selector not in valid_selectors:
        raise ValueError(f"Invalid selector '{selector}' for variable '{variable_name}'. Valid selectors: {', '.join(valid_selectors)}")


def _resolve_selector(selector: str) -> str:
    """Resolve a selector to its Minecraft equivalent."""
    if selector == "global":
        return "global"
    return selector


def _extract_base_variable_name(var_name: str) -> str:
    """Extract the base variable name from a scoped variable."""
    if '<' in var_name and '>' in var_name:
        return var_name.split('<')[0]
    return var_name


def _slugify(name: str) -> str:
    """Convert a string to a valid namespace/identifier."""
    # Remove special characters and replace spaces with underscores
    import re
    slug = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove multiple consecutive underscores
    slug = re.sub(r'_+', '_', slug)
    # Remove leading/trailing underscores
    slug = slug.strip('_')
    # Ensure it starts with a letter or underscore
    if slug and not slug[0].isalpha() and slug[0] != '_':
        slug = '_' + slug
    return slug.lower()
