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


def _process_variable_substitutions(command: str) -> str:
    """Process $variable$ substitutions in commands."""
    import re
    
    # Find all variable substitutions
    var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$'
    
    def replace_var(match):
        var_name = match.group(1)
        return f'{{"score":{{"name":"@s","objective":"{var_name}"}}}}'
    
    # Replace variable substitutions in the command
    return re.sub(var_pattern, replace_var, command)


def _convert_condition_to_minecraft_syntax(condition: str) -> str:
    """Convert regular comparison operators to Minecraft matches syntax and handle variable substitutions."""
    processed_condition = condition
    
    # Process variable substitutions in conditions
    if '$' in processed_condition:
        processed_condition = _process_variable_substitutions(processed_condition)
    
    # Handle dynamic variable references using @{variable_name} syntax
    # This converts @{var_name} to @s var_name for scoreboard references
    import re
    pattern = r'@\{([^}]+)\}'
    def replace_var_ref(match):
        var_name = match.group(1)
        return f"@s {var_name}"
    
    processed_condition = re.sub(pattern, replace_var_ref, processed_condition)
    
    # Convert comparison operators to Minecraft syntax
    processed_condition = processed_condition.replace('==', '=')
    processed_condition = processed_condition.replace('!=', '=')
    processed_condition = processed_condition.replace('<=', '=')
    processed_condition = processed_condition.replace('>=', '=')
    
    return processed_condition


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
    
    if verbose:
        print(f"Successfully merged {len(files)} file(s) into datapack: {root_pack.get('pack', {}).get('name', 'unknown')}")
    return root_pack


def _generate_scoreboard_objectives(ast: Dict[str, Any], output_dir: Path) -> List[str]:
    """Generate scoreboard objectives for all variables."""
    objectives = set()
    
    # Find all variable declarations
    for function in ast.get('functions', []):
        for statement in function.get('body', []):
            if hasattr(statement, 'name') and hasattr(statement, 'data_type'):
                objectives.add(statement.name)
    
    # Generate scoreboard commands
    commands = []
    for objective in objectives:
        commands.append(f"scoreboard objectives add {objective} dummy")
    
    return commands


def _process_statement(statement: Any, namespace: str, function_name: str) -> List[str]:
    """Process a single statement into Minecraft commands."""
    commands = []
    
    if hasattr(statement, '__class__'):
        class_name = statement.__class__.__name__
        
        if class_name == 'VariableDeclaration':
            # Handle variable declaration
            if statement.value:
                # Process the expression
                result = expression_processor.process_expression(statement.value, statement.name)
                commands.extend(result.temp_assignments)
                if result.final_command:
                    commands.append(result.final_command)
            else:
                # Initialize to 0
                commands.append(f"scoreboard players set @s {statement.name} 0")
        
        elif class_name == 'VariableAssignment':
            # Handle variable assignment
            result = expression_processor.process_expression(statement.value, statement.name)
            commands.extend(result.temp_assignments)
            if result.final_command:
                commands.append(result.final_command)
        
        elif class_name == 'IfStatement':
            # Handle if statement
            condition = _convert_condition_to_minecraft_syntax(statement.condition)
            
            # Generate unique labels
            if_label = f"{namespace}_{function_name}_if_{len(commands)}"
            end_label = f"{namespace}_{function_name}_if_end_{len(commands)}"
            
            # Add condition check
            commands.append(f"execute if {condition} run function {namespace}:{if_label}")
            
            # Add else if branches
            for i, elif_branch in enumerate(statement.elif_branches):
                elif_label = f"{namespace}_{function_name}_elif_{len(commands)}_{i}"
                elif_condition = _convert_condition_to_minecraft_syntax(elif_branch.condition)
                commands.append(f"execute unless {condition} if {elif_condition} run function {namespace}:{elif_label}")
            
            # Add else branch
            if statement.else_body:
                else_label = f"{namespace}_{function_name}_else_{len(commands)}"
                commands.append(f"execute unless {condition} run function {namespace}:{else_label}")
            
            # Add end label
            commands.append(f"function {namespace}:{end_label}")
        
        elif class_name == 'WhileLoop':
            # Handle while loop
            condition = _convert_condition_to_minecraft_syntax(statement.condition.condition_string)
            
            # Generate unique labels
            loop_label = f"{namespace}_{function_name}_while_{len(commands)}"
            end_label = f"{namespace}_{function_name}_while_end_{len(commands)}"
            
            # Add loop start
            commands.append(f"execute if {condition} run function {namespace}:{loop_label}")
            commands.append(f"function {namespace}:{end_label}")
        
        elif class_name == 'ForLoop':
            # Handle for loop (entity iteration)
            commands.append(f"execute as {statement.selector} run function {namespace}:{function_name}_for_{len(commands)}")
        
        elif class_name == 'Command':
            # Handle regular command
            command = statement.command
            
            # Process variable substitutions in strings
            if '$' in command:
                # Handle variable substitutions in tellraw commands
                if command.startswith('tellraw') and '{"text":"' in command:
                    # Convert tellraw with variable substitution to proper JSON format
                    import re
                    var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)\$'
                    
                    def replace_var_in_tellraw(match):
                        var_name = match.group(1)
                        return f'{{"score":{{"name":"@s","objective":"{var_name}"}}}}'
                    
                    # Replace variable substitutions
                    command = re.sub(var_pattern, replace_var_in_tellraw, command)
                else:
                    # Simple variable substitution
                    command = _process_variable_substitutions(command)
            
            commands.append(command)
        
        else:
            # Unknown statement type
            commands.append(f"# Unknown statement type: {class_name}")
    
    return commands


def _generate_function_file(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate function files from AST."""
    functions_dir = output_dir / "data" / namespace / "functions"
    functions_dir.mkdir(parents=True, exist_ok=True)
    
    for function in ast.get('functions', []):
        function_name = function['name']
        function_file = functions_dir / f"{function_name}.mcfunction"
        
        commands = []
        
        # Process each statement in the function
        for statement in function.get('body', []):
            commands.extend(_process_statement(statement, namespace, function_name))
        
        # Write the function file
        with open(function_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(commands))


def _generate_hook_files(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate hook files (load.json, tick.json)."""
    tags_dir = output_dir / "data" / "minecraft" / "tags" / "functions"
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    load_functions = []
    tick_functions = []
    
    for hook in ast.get('hooks', []):
        if hook.hook_type == "load":
            load_functions.append(f"{namespace}:{hook.function_name}")
        elif hook.hook_type == "tick":
            tick_functions.append(f"{namespace}:{hook.function_name}")
    
    # Generate load.json
    if load_functions:
        load_file = tags_dir / "load.json"
        with open(load_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{func}"' for func in load_functions) + ']}')
    
    # Generate tick.json
    if tick_functions:
        tick_file = tags_dir / "tick.json"
        with open(tick_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{func}"' for func in tick_functions) + ']}')


def _generate_tag_files(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate tag files."""
    tags_dir = output_dir / "data" / namespace / "tags" / "functions"
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    for tag in ast.get('tags', []):
        tag_file = tags_dir / f"{tag.name}.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{value}"' for value in tag.values) + ']}')


def _generate_pack_mcmeta(ast: Dict[str, Any], output_dir: Path) -> None:
    """Generate pack.mcmeta file."""
    pack_info = ast.get('pack')
    if not pack_info:
        pack_info = {'name': 'mdl_pack', 'description': 'Generated MDL pack', 'pack_format': 82}
    
    pack_mcmeta = {
        "pack": {
            "pack_format": pack_info['pack_format'],
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
    
    # Generate function files
    _generate_function_file(ast, output_dir, namespace)
    
    # Generate hook files
    _generate_hook_files(ast, output_dir, namespace)
    
    # Generate tag files
    _generate_tag_files(ast, output_dir, namespace)
    
    # Generate pack.mcmeta
    _generate_pack_mcmeta(ast, output_dir)
    
    if verbose:
        print(f"Successfully built datapack: {output_dir}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="MDL - Minecraft Datapack Language Compiler")
    parser.add_argument("command", choices=["build"], help="Command to execute")
    parser.add_argument("--mdl", "-m", required=True, help="Input MDL file or directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.command == "build":
        build_mdl(args.mdl, args.output, args.verbose)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
