"""
MDL CLI - Simplified Minecraft Datapack Language Compiler
Handles basic control structures and number variables only
"""

import argparse
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Any

from .mdl_lexer_js import lex_mdl_js
from .mdl_parser_js import parse_mdl_js
from .expression_processor import expression_processor
from .dir_map import get_dir_map

# Global variable to store conditional functions
conditional_functions = []


def _process_variable_substitutions(command: str, selector: str = "@s") -> str:
    """Process $variable$ substitutions in commands."""
    import re
    
    # Find all variable substitutions
    var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$'
    
    def replace_var(match):
        var_name = match.group(1)
        return f'{{"score":{{"name":"{selector}","objective":"{var_name}"}}}}'
    
    # Replace variable substitutions in the command
    return re.sub(var_pattern, replace_var, command)


def _convert_condition_to_minecraft_syntax(condition: str, selector: str = "@s") -> str:
    """Convert MDL conditions to proper Minecraft scoreboard syntax."""
    import re
    
    # Process variable substitutions in conditions
    if '$' in condition:
        condition = _process_variable_substitutions(condition, selector)
    
    # Handle dynamic variable references using @{variable_name} syntax
    # This converts @{var_name} to selector var_name for scoreboard references
    pattern = r'@\{([^}]+)\}'
    def replace_var_ref(match):
        var_name = match.group(1)
        return f"{selector} {var_name}"
    
    condition = re.sub(pattern, replace_var_ref, condition)
    
    # Convert MDL conditions to Minecraft scoreboard syntax
    # Pattern: "$variable$ > 50" -> "score selector variable matches 51.."
    # Pattern: "$variable$ < 10" -> "score selector variable matches ..9"
    # Pattern: "$variable$ >= 5" -> "score selector variable matches 5.."
    # Pattern: "$variable$ <= 20" -> "score selector variable matches ..20"
    # Pattern: "$variable$ == 100" -> "score selector variable matches 100"
    # Pattern: "$variable$ != 0" -> "score selector variable matches ..-1 1.."
    
    # Match patterns like "$variable$ > 50" or "$variable$ < 10"
    score_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$\s*([><=!]+)\s*(\d+)'
    
    # Also match patterns like '{"score":{"name":"selector","objective":"variable"}} > 50'
    score_pattern_substituted = r'\{"score":\{"name":"[^"]*","objective":"([a-zA-Z_][a-zA-Z0-9_]*)"\}\}\s*([><=!]+)\s*(\d+)'
    
    def convert_score_comparison(match):
        var_name = match.group(1)
        operator = match.group(2)
        value = int(match.group(3))
        
        if operator == '>':
            return f"score {selector} {var_name} matches {value + 1}.."
        elif operator == '>=':
            return f"score {selector} {var_name} matches {value}.."
        elif operator == '<':
            return f"score {selector} {var_name} matches ..{value - 1}"
        elif operator == '<=':
            return f"score {selector} {var_name} matches ..{value}"
        elif operator == '==':
            return f"score {selector} {var_name} matches {value}"
        elif operator == '!=':
            return f"score {selector} {var_name} matches ..{value - 1} {value + 1}.."
        else:
            # Fallback for unknown operators
            return f"score {selector} {var_name} matches {value}"
    
    # Apply the conversion for both patterns
    condition = re.sub(score_pattern, convert_score_comparison, condition)
    condition = re.sub(score_pattern_substituted, convert_score_comparison, condition)
    
    return condition


def _find_mdl_files(directory: Path) -> List[Path]:
    """Find all .mdl files in the directory."""
    return list(directory.glob("*.mdl"))


def _merge_mdl_files(files: List[Path], verbose: bool = False) -> Optional[Dict[str, Any]]:
    """Merge multiple MDL files into a single AST."""
    if not files:
        return None
    
    # Read and parse the first file
    with open(files[0], 'r', encoding='utf-8') as f:
        source = f.read()
    
    root_pack = parse_mdl_js(source)
    
    # Ensure root_pack has required keys
    if 'functions' not in root_pack:
        root_pack['functions'] = []
    if 'hooks' not in root_pack:
        root_pack['hooks'] = []
    if 'tags' not in root_pack:
        root_pack['tags'] = []
    if 'variables' not in root_pack:
        root_pack['variables'] = []
    
    # Merge additional files
    for file_path in files[1:]:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        ast = parse_mdl_js(source)
        
        # Merge functions
        if ast.get('functions'):
            root_pack['functions'].extend(ast['functions'])
        
        # Merge hooks
        if ast.get('hooks'):
            root_pack['hooks'].extend(ast['hooks'])
        
        # Merge tags
        if ast.get('tags'):
            root_pack['tags'].extend(ast['tags'])
        
        # Merge variables
        if ast.get('variables'):
            root_pack['variables'].extend(ast['variables'])
    
    if verbose:
        print(f"Successfully merged {len(files)} file(s) into datapack: {root_pack.get('pack', {}).get('name', 'unknown')}")
    return root_pack


def _generate_load_function(scoreboard_commands: List[str], output_dir: Path, namespace: str, ast: Dict[str, Any]) -> None:
    """Generate a load function with scoreboard objectives."""
    pack_info = ast.get('pack', {}) or {}
    pack_format = pack_info.get('pack_format', 82)
    
    # Use directory mapping based on pack format
    dir_map = get_dir_map(pack_format)
    functions_dir = output_dir / "data" / namespace / dir_map.function
    
    functions_dir.mkdir(parents=True, exist_ok=True)
    
    # Add armor stand creation for server-run functions
    load_commands = scoreboard_commands.copy()
    load_commands.append("execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}")
    
    # Write scoreboard commands to load.mcfunction
    load_file = functions_dir / "load.mcfunction"
    with open(load_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(load_commands))
    
    # Add load function as a hook to the AST
    if 'hooks' not in ast:
        ast['hooks'] = []
    
    # Always add the automatic load function for scoreboard initialization
    # This ensures scoreboard setup runs even when user has custom load hooks
    ast['hooks'].append({
        'hook_type': 'load',
        'function_name': 'load'
    })


def _generate_scoreboard_objectives(ast: Dict[str, Any], output_dir: Path) -> List[str]:
    """Generate scoreboard objectives for all variables."""
    objectives = set()
    
    # Find all variable declarations and assignments in functions
    for function in ast.get('functions', []):
        # Handle both dict and AST node objects
        if isinstance(function, dict):
            body = function.get('body', [])
        else:
            body = getattr(function, 'body', [])
        
        for statement in body:
            # Handle both dict and AST node objects
            if hasattr(statement, 'name') and hasattr(statement, 'data_type'):
                objectives.add(statement.name)
            elif hasattr(statement, 'name') and hasattr(statement, 'value'):
                # Variable assignment
                objectives.add(statement.name)
            elif isinstance(statement, dict):
                if 'name' in statement and 'data_type' in statement:
                    objectives.add(statement['name'])
                elif 'name' in statement and 'value' in statement:
                    objectives.add(statement['name'])
    
    # Also look for top-level variable declarations (outside functions)
    for variable in ast.get('variables', []):
        if hasattr(variable, 'name'):
            objectives.add(variable.name)
    
    # Generate scoreboard commands
    commands = []
    for objective in objectives:
        commands.append(f"scoreboard objectives add {objective} dummy")
    
    return commands


def _process_statement(statement: Any, namespace: str, function_name: str, statement_index: int = 0, is_tag_function: bool = False, selector: str = "@s") -> List[str]:
    """Process a single statement into Minecraft commands."""
    commands = []
    
    if hasattr(statement, '__class__'):
        class_name = statement.__class__.__name__
        
        if class_name == 'VariableDeclaration':
            # Handle variable declaration
            if statement.value:
                # Check if it's a simple 0 value (which will be handled in load function)
                if hasattr(statement.value, 'value') and statement.value.value == 0:
                    # Skip initialization for 0 values - they're handled in load function
                    pass
                else:
                    # Process the expression for non-zero values
                    result = expression_processor.process_expression(statement.value, statement.name, selector)
                    commands.extend(result.temp_assignments)
                    if result.final_command:
                        commands.append(result.final_command)
            else:
                # Skip initialization for 0 values - they're handled in load function
                pass
        
        elif class_name == 'VariableAssignment':
            # Handle variable assignment
            # Check if it's a simple assignment to 0 (which can be optimized out)
            if hasattr(statement.value, 'value') and statement.value.value == 0:
                # Skip assignment to 0 - it's handled in load function
                pass
            else:
                # Process the expression for non-zero values
                result = expression_processor.process_expression(statement.value, statement.name, selector)
                temp_commands = []
                temp_commands.extend(result.temp_assignments)
                if result.final_command:
                    temp_commands.append(result.final_command)
                
                # Split any commands that contain newlines
                for cmd in temp_commands:
                    if '\n' in cmd:
                        commands.extend(cmd.split('\n'))
                    else:
                        commands.append(cmd)
        
        elif class_name == 'IfStatement':
            # Handle if statement with proper execute commands
            # Get the condition string from the condition object
            if hasattr(statement.condition, 'condition_string'):
                condition_str = statement.condition.condition_string
            else:
                condition_str = str(statement.condition)
            condition = _convert_condition_to_minecraft_syntax(condition_str, selector)
            
            # Generate unique labels for this if statement
            if_label = f"{namespace}_{function_name}_if_{statement_index}"
            end_label = f"{namespace}_{function_name}_if_end_{statement_index}"
            
            # Add condition check - if true, run the if body
            commands.append(f"execute if {condition} run function {namespace}:{if_label}")
            
            # Process else if branches
            for i, elif_branch in enumerate(statement.elif_branches):
                elif_label = f"{namespace}_{function_name}_elif_{statement_index}_{i}"
                # Get the condition string from the elif condition object
                if hasattr(elif_branch.condition, 'condition_string'):
                    elif_condition_str = elif_branch.condition.condition_string
                else:
                    elif_condition_str = str(elif_branch.condition)
                elif_condition = _convert_condition_to_minecraft_syntax(elif_condition_str, selector)
                # Only run elif if previous conditions were false
                commands.append(f"execute unless {condition} if {elif_condition} run function {namespace}:{elif_label}")
            
            # Process else body
            if statement.else_body:
                else_label = f"{namespace}_{function_name}_else_{statement_index}"
                commands.append(f"execute unless {condition} run function {namespace}:{else_label}")
            
            # Add end label
            commands.append(f"function {namespace}:{end_label}")
        
        elif class_name == 'WhileLoop':
            # Handle while loop with method selection
            condition = _convert_condition_to_minecraft_syntax(statement.condition.condition_string, selector)
            method = getattr(statement, 'method', 'recursion')  # Default to recursion
            
            if method == "recursion":
                # Use current recursion approach (creates multiple function files)
                commands.extend(_process_while_loop_recursion(statement, namespace, function_name, statement_index, is_tag_function, selector))
            elif method == "schedule":
                # Use schedule-based approach (single function with counter)
                commands.extend(_process_while_loop_schedule(statement, namespace, function_name, statement_index, is_tag_function, selector))
            else:
                raise ValueError(f"Unknown while loop method: {method}")
        

        
        elif class_name == 'Command':
            # Handle regular command
            command = statement.command
            
            # Always convert say commands to tellraw first
            if command.startswith('say'):
                import re
                var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$'
                
                # Extract the text content from say command
                text_match = re.search(r'say "([^"]*)"', command)
                if text_match:
                    text_content = text_match.group(1)
                    
                    # Check if there are variable substitutions
                    if '$' in text_content:
                        # Build JSON array with text and scoreboard components
                        var_matches = list(re.finditer(var_pattern, text_content))
                        json_parts = []
                        last_end = 0
                        
                        for match in var_matches:
                            # Add text before the variable
                            if match.start() > last_end:
                                text_before = text_content[last_end:match.start()]
                                if text_before:
                                    json_parts.append(f'{{"text":"{text_before}"}}')
                            
                            # Add the variable
                            var_name = match.group(1)
                            json_parts.append(f'{{"score":{{"name":"{selector}","objective":"{var_name}"}}}}')
                            last_end = match.end()
                        
                        # Add any remaining text
                        if last_end < len(text_content):
                            text_after = text_content[last_end:]
                            if text_after:
                                json_parts.append(f'{{"text":"{text_after}"}}')
                        
                        command = f'tellraw @a [{",".join(json_parts)}]'
                    else:
                        # No variables, simple conversion
                        command = f'tellraw @a [{{"text":"{text_content}"}}]'
                else:
                    # Fallback: if regex doesn't match, still convert to tellraw
                    command = command.replace('say "', f'tellraw @a [{{"text":"')
                    command = command.replace('"', '"}]')
                

            
            # Process variable substitutions in strings for other commands
            elif '$' in command:
                # Handle variable substitutions in tellraw commands
                if command.startswith('tellraw'):
                    # Convert tellraw with variable substitution to proper JSON format
                    import re
                    var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$'
                    
                    def replace_var_in_tellraw(match):
                        var_name = match.group(1)
                        return f'{{"score":{{"name":"{selector}","objective":"{var_name}"}}}}'
                    
                    # Replace variable substitutions
                    command = re.sub(var_pattern, replace_var_in_tellraw, command)
                    
                    # Clean up extra spaces in tellraw commands
                    command = command.replace(' @ s ', ' @s ')
                    command = command.replace(' , ', ', ')
                    command = command.replace(' { ', ' {')
                    command = command.replace(' } ', ' }')
                    command = command.replace(' : ', ': ')
                else:
                    # Simple variable substitution for other commands
                    command = _process_variable_substitutions(command, selector)
            elif command.startswith('tellraw'):
                # For tellraw commands, only replace @s with @a, leave @a unchanged
                command = command.replace('tellraw @s ', 'tellraw @a ')
                # Clean up spacing
                command = command.replace(' @ s ', ' @s ')
                command = command.replace(' , ', ', ')
                command = command.replace(' { ', ' {')
                command = command.replace(' } ', ' }')
                command = command.replace(' : ', ': ')
            
            commands.append(command)
        
        else:
            # Unknown statement type - try to handle as string
            if isinstance(statement, str):
                commands.append(statement)
            else:
                commands.append(f"# Unknown statement type: {class_name}")
    
    return commands




def _generate_function_file(ast: Dict[str, Any], output_dir: Path, namespace: str, verbose: bool = False) -> None:
    """Generate function files with support for different pack format directory structures."""
    pack_info = ast.get('pack', {}) or {}
    pack_format = pack_info.get('pack_format', 82)
    
    # Use directory mapping based on pack format
    dir_map = get_dir_map(pack_format)
    functions_dir = output_dir / "data" / namespace / dir_map.function
    
    functions_dir.mkdir(parents=True, exist_ok=True)
    
    # Track all conditional functions that need to be generated
    global conditional_functions
    conditional_functions = []
    
    for function in ast.get('functions', []):
        # Handle both dict and AST node objects
        if isinstance(function, dict):
            function_name = function['name']
            body = function.get('body', [])
        else:
            function_name = getattr(function, 'name', 'unknown')
            body = getattr(function, 'body', [])
        
        function_file = functions_dir / f"{function_name}.mcfunction"
        
        commands = []
        
        # Check if this function is called via a tag (tick/load)
        is_tag_function = False
        for hook in ast.get('hooks', []):
            if hook['function_name'] == function_name or hook['function_name'] == f"{namespace}:{function_name}":
                is_tag_function = True
                break
        
        # For server-run functions (tick/load hooks), use a server armor stand
        # For player-called functions, use @s (self)
        if is_tag_function:
            # Use the server armor stand created in load function (high in the sky, invisible)
            # Add safety check to recreate if it doesn't exist (e.g., after /kill @e)
            commands.append("execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}")
            selector = "@e[type=armor_stand,tag=mdl_server,limit=1]"
        else:
            selector = "@s"
        
        # Debug output - always print
        print(f"DEBUG: Function {function_name}: is_tag_function={is_tag_function}, selector={selector}")
        print(f"DEBUG: Hooks: {ast.get('hooks', [])}")
        
        if verbose:
            print(f"Function {function_name}: is_tag_function={is_tag_function}, selector={selector}")
            print(f"  Hooks: {ast.get('hooks', [])}")
            print(f"  Looking for: {function_name} or {namespace}:{function_name}")
            print(f"  Hook function names: {[hook.get('function_name', '') for hook in ast.get('hooks', [])]}")
        
        # Process each statement in the function
        for i, statement in enumerate(body):
            if verbose:
                print(f"Processing statement: {type(statement)} = {statement}")
            commands.extend(_process_statement(statement, namespace, function_name, i, is_tag_function, selector))
            
            # Collect conditional functions for if statements
            if hasattr(statement, '__class__') and statement.__class__.__name__ == 'IfStatement':
                conditional_functions.extend(_collect_conditional_functions(statement, namespace, function_name, i, is_tag_function, selector))
        
        # Write the function file
        with open(function_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(commands))
    
    # Generate all conditional function files
    for func_name, func_body in conditional_functions:
        func_file = functions_dir / f"{func_name}.mcfunction"
        with open(func_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(func_body))


def _generate_hook_files(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate hook files (load.json, tick.json) with support for different pack format directory structures."""
    pack_info = ast.get('pack', {}) or {}
    pack_format = pack_info.get('pack_format', 82)
    
    # Use directory mapping based on pack format
    dir_map = get_dir_map(pack_format)
    tags_dir = output_dir / "data" / "minecraft" / dir_map.tags_function
    
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    load_functions = []
    tick_functions = []
    
    for hook in ast.get('hooks', []):
        function_name = hook['function_name']
        
        # Skip hooks for function_name "load" as this is reserved for the global load function
        if function_name == "load":
            continue
            
        # Check if function_name already contains a namespace (has a colon)
        if ':' in function_name:
            # Function name already includes namespace, use as-is
            full_function_name = function_name
        else:
            # Function name doesn't include namespace, add it
            full_function_name = f"{namespace}:{function_name}"
        
        if hook['hook_type'] == "load":
            load_functions.append(full_function_name)
        elif hook['hook_type'] == "tick":
            tick_functions.append(full_function_name)
    
    # Generate tick.json
    if tick_functions:
        tick_file = tags_dir / "tick.json"
        with open(tick_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{func}"' for func in tick_functions) + ']}')
    
    # Check if we need to generate a global load function for variable initialization
    has_variables = bool(ast.get('variables', []))
    
    # Generate load.json if there are explicit load hooks OR if we have variables to initialize
    if load_functions or has_variables:
        # Add the global load function to the list (avoid duplicates)
        global_load_function = f"{namespace}:load"
        if global_load_function not in load_functions:
            load_functions.append(global_load_function)
        load_file = tags_dir / "load.json"
        with open(load_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{func}"' for func in load_functions) + ']}')
    
    # Generate a global load function for variable initialization if we have variables
    if has_variables:
        _generate_global_load_function(ast, output_dir, namespace)


def _generate_global_load_function(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate a global load function for variable initialization."""
    pack_info = ast.get('pack', {}) or {}
    pack_format = pack_info.get('pack_format', 82)
    
    # Use directory mapping based on pack format
    dir_map = get_dir_map(pack_format)
    functions_dir = output_dir / "data" / namespace / dir_map.function
    
    functions_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all variable declarations and assignments from all functions
    variable_initializations = []
    processed_vars = set()  # Track processed variables to avoid duplicates
    
    # Add scoreboard objectives for all top-level variables
    for var in ast.get('variables', []):
        if isinstance(var, dict):
            var_name = var.get('name', 'unknown')
        else:
            var_name = getattr(var, 'name', 'unknown')
        
        if var_name and var_name not in processed_vars:
            processed_vars.add(var_name)
            # Add scoreboard objective creation
            variable_initializations.append(f"scoreboard objectives add {var_name} dummy")
            
            # Always initialize to 0 for debugging and reload consistency
            variable_initializations.append(f"scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] {var_name} 0")
    
    # Add scoreboard objectives for all variables from function declarations and assignments
    for function in ast.get('functions', []):
        if isinstance(function, dict):
            body = function.get('body', [])
        else:
            body = getattr(function, 'body', [])
        
        for statement in body:
            var_name = None
            
            # Handle variable declarations
            if hasattr(statement, '__class__') and statement.__class__.__name__ == 'VariableDeclaration':
                var_name = statement.name if hasattr(statement, 'name') else statement.get('name', 'unknown')
                
            # Handle variable assignments to capture all used variables
            elif hasattr(statement, '__class__') and statement.__class__.__name__ == 'VariableAssignment':
                var_name = statement.name if hasattr(statement, 'name') else statement.get('name', 'unknown')
            
            # Process the variable if we found one
            if var_name and var_name not in processed_vars:
                processed_vars.add(var_name)
                # Add scoreboard objective creation
                variable_initializations.append(f"scoreboard objectives add {var_name} dummy")
                
                # Always initialize to 0 for debugging and reload consistency
                variable_initializations.append(f"scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] {var_name} 0")
    
    # Add server armor stand creation
    if variable_initializations:
        variable_initializations.insert(0, "execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}")
    
    # Write the global load function
    if variable_initializations:
        load_file = functions_dir / "load.mcfunction"
        with open(load_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(variable_initializations))


def _generate_tag_files(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate tag files with support for different pack format directory structures."""
    pack_info = ast.get('pack', {}) or {}
    pack_format = pack_info.get('pack_format', 82)
    
    # Use directory mapping based on pack format
    dir_map = get_dir_map(pack_format)
    tags_dir = output_dir / "data" / namespace / dir_map.tags_function
    
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    for tag in ast.get('tags', []):
        tag_file = tags_dir / f"{tag['name']}.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{value}"' for value in tag['values']) + ']}')


def _validate_pack_format(pack_format: int) -> None:
    """Validate pack format and provide helpful information."""
    if pack_format < 1:
        raise SystemExit(f"Invalid pack format: {pack_format}. Must be >= 1")
    
    print(f"Pack format {pack_format}")
    
    # Get directory mapping for this pack format
    dir_map = get_dir_map(pack_format)
    
    # Directory structure information
    print(f"  - Functions: data/<namespace>/{dir_map.function}/")
    print(f"  - Tags: data/minecraft/{dir_map.tags_function}/")
    
    # Pack metadata format changes
    if pack_format >= 82:
        print("  - Pack metadata: min_format and max_format (82+)")
    else:
        print("  - Pack metadata: pack_format (<82)")
    
    # Tag directory changes (for other tag types)
    if pack_format >= 43:
        print("  - Tag directories: item/, block/, entity_type/, fluid/, game_event/ (43+)")
    else:
        print("  - Tag directories: items/, blocks/, entity_types/, fluids/, game_events/ (<43)")


def _collect_conditional_functions(if_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s") -> List[tuple]:
    """Collect all conditional functions from an if statement"""
    functions = []
    
    # Generate if body function
    if_label = f"{namespace}_{function_name}_if_{statement_index}"
    if_commands = []
    for j, stmt in enumerate(if_statement.body):
        if_commands.extend(_process_statement(stmt, namespace, function_name, j, is_tag_function, selector))
    functions.append((if_label, if_commands))
    
    # Generate elif body functions
    for i, elif_branch in enumerate(if_statement.elif_branches):
        elif_label = f"{namespace}_{function_name}_elif_{statement_index}_{i}"
        elif_commands = []
        for j, stmt in enumerate(elif_branch.body):
            elif_commands.extend(_process_statement(stmt, namespace, function_name, j, is_tag_function, selector))
        functions.append((elif_label, elif_commands))
    
    # Generate else body function
    if if_statement.else_body:
        else_label = f"{namespace}_{function_name}_else_{statement_index}"
        else_commands = []
        for j, stmt in enumerate(if_statement.else_body):
            else_commands.extend(_process_statement(stmt, namespace, function_name, j, is_tag_function, selector))
        functions.append((else_label, else_commands))
    
    # Generate end function (empty)
    end_label = f"{namespace}_{function_name}_if_end_{statement_index}"
    functions.append((end_label, []))
    
    return functions


def _process_while_loop_recursion(while_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s") -> List[str]:
    """Process while loop using recursion method (creates multiple function files)"""
    commands = []
    
    condition = _convert_condition_to_minecraft_syntax(while_statement.condition.condition_string, selector)
    
    # Generate loop body function
    loop_label = f"{namespace}_{function_name}_while_{statement_index}"
    loop_commands = []
    for j, stmt in enumerate(while_statement.body):
        loop_commands.extend(_process_statement(stmt, namespace, function_name, j, is_tag_function, selector))
    
    # Add recursive call to continue the loop
    loop_commands.append(f"execute if {condition} run function {namespace}:{loop_label}")
    
    # Add the loop body commands to the conditional functions list
    # (This will be handled by the _generate_function_file method)
    global conditional_functions
    conditional_functions.append((loop_label, loop_commands))
    
    # Add condition check and function call
    commands.append(f"execute if {condition} run function {namespace}:{loop_label}")
    
    return commands


def _process_while_loop_schedule(while_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s") -> List[str]:
    """Process while loop using schedule method (single function with counter)"""
    commands = []
    
    condition = _convert_condition_to_minecraft_syntax(while_statement.condition.condition_string, selector)
    
    # Generate loop body function
    loop_label = f"{namespace}_{function_name}_while_{statement_index}"
    loop_commands = []
    for j, stmt in enumerate(while_statement.body):
        loop_commands.extend(_process_statement(stmt, namespace, function_name, j, is_tag_function, selector))
    
    # Add recursive schedule call to continue the loop
    loop_commands.append(f"execute if {condition} run schedule function {namespace}:{loop_label} 1t")
    
    # Add the loop body commands to the conditional functions list
    global conditional_functions
    conditional_functions.append((loop_label, loop_commands))
    
    # Add condition check and schedule
    commands.append(f"execute if {condition} run function {namespace}:{loop_label}")
    
    return commands


def _create_zip_file(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from the datapack directory."""
    import zipfile
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                # Get the relative path from the source directory
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)


def _generate_pack_mcmeta(ast: Dict[str, Any], output_dir: Path) -> None:
    """Generate pack.mcmeta file with support for both pre-82 and post-82 formats."""
    pack_info = ast.get('pack')
    if not pack_info:
        pack_info = {'name': 'mdl_pack', 'description': 'Generated MDL pack', 'pack_format': 82}
    
    pack_format = pack_info['pack_format']
    
    # Validate pack format
    _validate_pack_format(pack_format)
    
    # Handle different pack format versions
    if pack_format >= 82:
        # Post-82 format (1.21+) with min_format and max_format
        pack_mcmeta = {
            "pack": {
                "min_format": [pack_format, 0],
                "max_format": [pack_format, 0x7fffffff],
                "description": pack_info['description']
            }
        }
    else:
        # Pre-82 format (1.20 and below) with pack_format
        pack_mcmeta = {
            "pack": {
                "pack_format": pack_format,
                "description": pack_info['description']
            }
        }
    
    import json
    with open(output_dir / "pack.mcmeta", 'w', encoding='utf-8') as f:
        json.dump(pack_mcmeta, f, indent=2)


def build_mdl(input_path: str, output_path: str, verbose: bool = False) -> None:
    """Build MDL files into a Minecraft datapack."""
    input_dir = Path(input_path)
    output_dir = Path(output_path)
    
    # Clean output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    # Find MDL files
    if input_dir.is_file() and input_dir.suffix == '.mdl':
        mdl_files = [input_dir]
    else:
        mdl_files = _find_mdl_files(input_dir)
    
    if not mdl_files:
        raise SystemExit("No .mdl files found")
    
    # Parse and merge MDL files
    ast = _merge_mdl_files(mdl_files, verbose)
    if not ast:
        raise SystemExit("Failed to parse MDL files")
    
    # Get namespace
    namespace = ast.get('namespace', {}).get('name', 'mdl') if ast.get('namespace') else 'mdl'
    
    # Generate scoreboard objectives
    scoreboard_commands = _generate_scoreboard_objectives(ast, output_dir)
    if verbose:
        print(f"Generated {len(scoreboard_commands)} scoreboard commands: {scoreboard_commands}")
    
    # Write scoreboard objectives to a load function
    if scoreboard_commands:
        if verbose:
            print(f"Generating load function with {len(scoreboard_commands)} scoreboard commands")
        _generate_load_function(scoreboard_commands, output_dir, namespace, ast)
    
    # Generate function files
    _generate_function_file(ast, output_dir, namespace, verbose)
    
    # Generate hook files
    _generate_hook_files(ast, output_dir, namespace)
    
    # Generate tag files
    _generate_tag_files(ast, output_dir, namespace)
    
    # Generate pack.mcmeta
    _generate_pack_mcmeta(ast, output_dir)
    
    # Create zip file
    _create_zip_file(output_dir, output_dir.parent / f"{output_dir.name}.zip")
    
    if verbose:
        print(f"Successfully built datapack: {output_dir}")
        print(f"Created zip file: {output_dir.parent / f'{output_dir.name}.zip'}")


def create_new_project(project_name: str, pack_name: str = None) -> None:
    """Create a new MDL project with simplified syntax."""
    if not pack_name:
        pack_name = project_name
    
    project_dir = Path(project_name)
    if project_dir.exists():
        raise SystemExit(f"Project directory '{project_name}' already exists")
    
    project_dir.mkdir(parents=True)
    
    # Create the main MDL file with simplified syntax (post-82 format)
    mdl_content = f'''// {project_name}.mdl - Simplified MDL Project (Minecraft 1.21+)
// Uses pack format 82+ with new directory structure (function/ instead of functions/)
pack "{pack_name}" "A simplified MDL datapack" 82;

namespace "{project_name}";

// Number variables for scoreboard storage
var num player_count = 0;
var num game_timer = 0;
var num player_score = 0;

function "main" {{
    // Basic variable assignment
    player_count = 0;
    game_timer = 0;
    player_score = 100;
    
    // If statement with variable substitution
    if "$player_score$ > 50" {{
        say "Player is doing well!";
    }} else {{
        say "Player needs to improve!";
    }}
    
    // While loop with counter
    while "$game_timer$ < 10" {{
        game_timer = $game_timer$ + 1;
        say "Timer: $game_timer$";
    }}
    
    // While loop example (for loops are no longer supported)
    while "$player_count$ < 5" {{
        say "Player count: $player_count$";
        player_count = $player_count$ + 1;
    }}
    
    // Conditional with variable substitution
    if "$player_count$ > 0" {{
        say "Players online: $player_count$";
    }}
}}

function "helper" {{
    var num result = 0;
    result = 5 + 3;
    say "Calculation result: $result$";
    
    // Variable substitution in tellraw
    tellraw @a [{{"text":"Score: "}},{{"score":{{"name":"@a","objective":"player_score"}}}}];
}}

// Hook to run main function every tick
on_tick "{project_name}:main";
'''
    
    # Write the MDL file
    mdl_file = project_dir / f"{project_name}.mdl"
    with open(mdl_file, 'w', encoding='utf-8') as f:
        f.write(mdl_content)
    
    # Create README
    readme_content = f'''# {project_name}

A simplified MDL (Minecraft Datapack Language) project demonstrating core features.

## Pack Format Information

This project uses **pack format 82** (Minecraft 1.21+) with the new directory structure:
- **Functions**: `data/<namespace>/function/` (not `functions/`)
- **Tags**: `data/minecraft/tags/function/` (not `functions/`)
- **Pack Metadata**: Uses `min_format` and `max_format` instead of `pack_format`

For Minecraft 1.20 and below, use pack format < 82 with legacy directory structure.

## Features Demonstrated

- **Number Variables**: Stored in scoreboard objectives
- **Variable Substitution**: Using `$variable$` syntax
- **Control Structures**: If/else statements and loops
- **For Loops**: Entity iteration with `@a` selector
- **While Loops**: Counter-based loops
- **Hooks**: Automatic execution with `on_tick`

## Building

```bash
mdl build --mdl . --output dist
```

## Simplified Syntax

This project uses the simplified MDL syntax:
- Only number variables (no strings or lists)
- Direct scoreboard integration with `$variable$`
- Simple control structures that actually work
- Focus on reliability over complexity

## Generated Commands

The compiler will generate:
- Scoreboard objectives for all variables
- Minecraft functions with proper control flow
- Hook files for automatic execution
- Pack metadata with correct format for pack version 82+

## Pack Format Examples

### Post-82 (Minecraft 1.21+)
```mdl
pack "my_pack" "My datapack" 82;
// Uses: data/<namespace>/function/ and min_format/max_format
```

### Pre-82 (Minecraft 1.20 and below)
```mdl
pack "my_pack" "My datapack" 15;
// Uses: data/<namespace>/functions/ and pack_format
```
'''
    
    readme_file = project_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Created new MDL project: {project_name}")
    print(f"  - Main file: {mdl_file}")
    print(f"  - README: {readme_file}")
    print(f"  - Build with: mdl build --mdl . --output dist")


def main():
    """Main CLI entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("MDL - Minecraft Datapack Language Compiler")
        print("Usage: mdl <command> [options]")
        print("Commands:")
        print("  build --mdl <file> --output <dir>  Build MDL files into datapack")
        print("  new <project_name> [--name <pack_name>]  Create new MDL project")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "build":
        parser = argparse.ArgumentParser(description="MDL - Build MDL files into datapack")
        parser.add_argument("--mdl", "-m", required=True, help="Input MDL file or directory")
        parser.add_argument("--output", "-o", required=True, help="Output directory")
        parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
        
        args = parser.parse_args(sys.argv[2:])
        build_mdl(args.mdl, args.output, args.verbose)
        
    elif command == "new":
        parser = argparse.ArgumentParser(description="MDL - Create new MDL project")
        parser.add_argument("project_name", help="Name of the project to create")
        parser.add_argument("--name", help="Pack name (defaults to project name)")
        
        args = parser.parse_args(sys.argv[2:])
        create_new_project(args.project_name, args.name)
        
    else:
        print(f"Unknown command: {command}")
        print("Available commands: build, new")
        sys.exit(1)


if __name__ == "__main__":
    main()
