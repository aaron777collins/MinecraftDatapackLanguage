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
    """Generate function files with support for different pack format directory structures."""
    pack_info = ast.get('pack', {})
    pack_format = pack_info.get('pack_format', 82)
    
    # Use new directory name for pack format 45+ (functions -> function)
    if pack_format >= 45:
        functions_dir = output_dir / "data" / namespace / "function"
    else:
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
    """Generate hook files (load.json, tick.json) with support for different pack format directory structures."""
    pack_info = ast.get('pack', {})
    pack_format = pack_info.get('pack_format', 82)
    
    # Use new directory name for pack format 45+ (tags/functions -> tags/function)
    if pack_format >= 45:
        tags_dir = output_dir / "data" / "minecraft" / "tags" / "function"
    else:
        tags_dir = output_dir / "data" / "minecraft" / "tags" / "functions"
    
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    load_functions = []
    tick_functions = []
    
    for hook in ast.get('hooks', []):
        if hook['hook_type'] == "load":
            load_functions.append(f"{namespace}:{hook['function_name']}")
        elif hook['hook_type'] == "tick":
            tick_functions.append(f"{namespace}:{hook['function_name']}")
    
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
    """Generate tag files with support for different pack format directory structures."""
    pack_info = ast.get('pack', {})
    pack_format = pack_info.get('pack_format', 82)
    
    # Use new directory name for pack format 45+ (tags/functions -> tags/function)
    if pack_format >= 45:
        tags_dir = output_dir / "data" / namespace / "tags" / "function"
    else:
        tags_dir = output_dir / "data" / namespace / "tags" / "functions"
    
    tags_dir.mkdir(parents=True, exist_ok=True)
    
    for tag in ast.get('tags', []):
        tag_file = tags_dir / f"{tag['name']}.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write('{"values": [' + ', '.join(f'"{value}"' for value in tag['values']) + ']}')


def _validate_pack_format(pack_format: int) -> None:
    """Validate pack format and provide helpful information."""
    if pack_format < 1:
        raise SystemExit(f"Invalid pack format: {pack_format}. Must be >= 1")
    
    print(f"✓ Pack format {pack_format}")
    
    # Directory structure changes
    if pack_format >= 45:
        print("  - Functions: data/<namespace>/function/ (45+)")
        print("  - Tags: data/minecraft/tags/function/ (45+)")
    else:
        print("  - Functions: data/<namespace>/functions/ (<45)")
        print("  - Tags: data/minecraft/tags/functions/ (<45)")
    
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
    
    // For loop to iterate over players
    for player in "@a" {{
        say "Hello $player$!";
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
    tellraw @s [{{"text":"Score: "}},{{"score":{{"name":"@s","objective":"player_score"}}}}];
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
