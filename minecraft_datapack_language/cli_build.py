"""
CLI Build Functions - Core build functionality for MDL CLI
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Any

from .mdl_lexer_js import lex_mdl_js
from .mdl_parser_js import parse_mdl_js
from .expression_processor import ExpressionProcessor
from .dir_map import get_dir_map
from .pack import Pack, Namespace, Function, Tag, Recipe, Advancement, LootTable, Predicate, ItemModifier, Structure
from .mdl_errors import MDLErrorCollector, create_error, MDLBuildError, MDLFileError, MDLCompilationError, MDLSyntaxError, MDLParserError, MDLLexerError
from .cli_utils import ensure_dir, write_json, _process_variable_substitutions, _convert_condition_to_minecraft_syntax, _find_mdl_files, _validate_selector, _resolve_selector, _extract_base_variable_name, _slugify


class BuildContext:
    """Context for build operations to prevent race conditions."""
    
    def __init__(self):
        self.conditional_functions = []
        self.variable_scopes = {}
        self.namespace_functions = {}
        self.expression_processor = ExpressionProcessor()


def _merge_mdl_files(files: List[Path], verbose: bool = False, error_collector: MDLErrorCollector = None) -> Optional[Dict[str, Any]]:
    """Merge multiple MDL files into a single AST."""
    if not files:
        return None
    
    # Parse the first file to get the base AST
    try:
        if verbose:
            print(f"DEBUG: Parsing first file: {files[0]}")
        
        with open(files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast = parse_mdl_js(content, str(files[0]))
        
        if verbose:
            print(f"DEBUG: Successfully parsed {files[0]}")
    
    except MDLLexerError as e:
        if error_collector:
            error_collector.add_error(e)
        else:
            raise
        return None
    except MDLParserError as e:
        if error_collector:
            error_collector.add_error(e)
        else:
            raise
        return None
    except MDLSyntaxError as e:
        if error_collector:
            error_collector.add_error(e)
        else:
            raise
        return None
    except Exception as e:
        if error_collector:
            error_collector.add_error(create_error(
                MDLCompilationError,
                f"Failed to parse {files[0]}: {str(e)}",
                file_path=str(files[0]),
                suggestion="Check the file syntax and ensure it's a valid MDL file."
            ))
        else:
            raise
        return None
    
    # Merge additional files
    for file_path in files[1:]:
        try:
            if verbose:
                print(f"DEBUG: Parsing additional file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            additional_ast = parse_mdl_js(content, str(file_path))
            
            if verbose:
                print(f"DEBUG: Successfully parsed {file_path}")
            
            # Merge functions
            if 'functions' in additional_ast:
                if 'functions' not in ast:
                    ast['functions'] = []
                ast['functions'].extend(additional_ast['functions'])
            
            # Merge variables
            if 'variables' in additional_ast:
                if 'variables' not in ast:
                    ast['variables'] = []
                ast['variables'].extend(additional_ast['variables'])
            
            # Merge namespaces (append to existing list)
            if 'namespaces' in additional_ast:
                if 'namespaces' not in ast:
                    ast['namespaces'] = []
                ast['namespaces'].extend(additional_ast['namespaces'])
            
            # Merge registry declarations
            for registry_type in ['recipes', 'loot_tables', 'advancements', 'predicates', 'item_modifiers', 'structures']:
                if registry_type in additional_ast:
                    if registry_type not in ast:
                        ast[registry_type] = []
                    ast[registry_type].extend(additional_ast[registry_type])
            
            # Merge pack metadata (use the first one found)
            if 'pack' in additional_ast and 'pack' not in ast:
                ast['pack'] = additional_ast['pack']
        
        except MDLLexerError as e:
            if error_collector:
                error_collector.add_error(e)
            else:
                raise
            return None
        except MDLParserError as e:
            if error_collector:
                error_collector.add_error(e)
            else:
                raise
            return None
        except MDLSyntaxError as e:
            if error_collector:
                error_collector.add_error(e)
            else:
                raise
            return None
        except Exception as e:
            if error_collector:
                error_collector.add_error(create_error(
                    MDLCompilationError,
                    f"Failed to parse {file_path}: {str(e)}",
                    file_path=str(file_path),
                    suggestion="Check the file syntax and ensure it's a valid MDL file."
                ))
            else:
                raise
            return None
    
    return ast


def _generate_scoreboard_objectives(ast: Dict[str, Any], output_dir: Path) -> List[str]:
    """Generate scoreboard objectives for all variables."""
    scoreboard_commands = []
    
    # Collect all variable names
    variables = set()
    
    # From variable declarations
    if 'variables' in ast:
        for var_decl in ast['variables']:
            if 'name' in var_decl:
                variables.add(var_decl['name'])
    
    # From functions (scan for variable usage)
    if 'functions' in ast:
        for func in ast['functions']:
            if 'body' in func:
                for statement in func['body']:
                    # Look for variable assignments and usage
                    if statement['type'] == 'variable_assignment':
                        variables.add(statement['name'])
                    elif statement['type'] == 'command':
                        # Scan command for variable substitutions
                        command = statement['command']
                        import re
                        var_matches = re.findall(r'\$([^$]+)\$', command)
                        for var_name in var_matches:
                            # Extract base name from scoped variables
                            base_name = _extract_base_variable_name(var_name)
                            variables.add(base_name)
    
    # Create scoreboard objectives
    for var_name in sorted(variables):
        scoreboard_commands.append(f"scoreboard objectives add {var_name} dummy")
    
    return scoreboard_commands


def _generate_load_function(scoreboard_commands: List[str], output_dir: Path, namespace: str, ast: Dict[str, Any]) -> None:
    """Generate the load function with scoreboard setup."""
    load_content = []
    
    # Add armor stand setup for server-side operations
    load_content.append("execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}")
    
    # Add scoreboard objectives
    load_content.extend(scoreboard_commands)
    
    # Add any custom load commands from the AST
    if 'load' in ast:
        for command in ast['load']:
            load_content.append(command)
    
    # Write the load function
    load_dir = output_dir / "data" / namespace / "function"
    ensure_dir(str(load_dir))
    
    with open(load_dir / "load.mcfunction", 'w', encoding='utf-8') as f:
        f.write('\n'.join(load_content))


def _process_say_command_with_variables(content: str, selector: str) -> str:
    """Process say command content with variable substitution, converting to tellraw with score components."""
    import re
    
    print(f"DEBUG: _process_say_command_with_variables called with content: {repr(content)}, selector: {selector}")
    
    # Clean up the content - remove quotes if present
    content = content.strip()
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]  # Remove surrounding quotes
    
    # Find all variable references like $variable$ or $variable<selector>$
    var_pattern = r'\$([^$]+)\$'
    matches = re.findall(var_pattern, content)
    
    if not matches:
        # Check for common variable names that might have been processed
        # This handles the case where $counter$ was converted to just "counter"
        word_pattern = r'\b(counter|health|score|value|num|count|timer|level)\b'
        word_matches = re.findall(word_pattern, content)
        
        if word_matches:
            # Process the content by replacing each variable with a score component
            components = []
            processed_content = content
            
            # Sort variables by their position in the content to process them in order
            var_positions = []
            for var_name in set(word_matches):  # Remove duplicates
                pos = processed_content.find(var_name)
                if pos >= 0:
                    var_positions.append((pos, var_name))
            
            var_positions.sort()  # Sort by position
            
            last_pos = 0
            for pos, var_name in var_positions:
                # Add text before this variable
                if pos > last_pos:
                    text_before = processed_content[last_pos:pos]
                    if text_before:
                        components.append(f'{{"text":"{text_before}"}}')
                
                # Add score component for variable
                components.append(f'{{"score":{{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"{var_name}"}}}}')
                
                last_pos = pos + len(var_name)
            
            # Add remaining text after last variable
            if last_pos < len(processed_content):
                remaining_text = processed_content[last_pos:]
                if remaining_text:
                    components.append(f'{{"text":"{remaining_text}"}}')
            
            # Combine all components
            components_str = ','.join(components)
            return f'tellraw @a [{components_str}]'
        else:
            # No variables, return simple tellraw
            return f'tellraw @a [{{"text":"{content}"}}]'
    
    # Split content by variable references while preserving the structure
    parts = re.split(var_pattern, content)
    
    # Build tellraw components
    components = []
    var_index = 0
    
    for i, part in enumerate(parts):
        if part:  # Add text component if not empty
            components.append(f'{{"text":"{part}"}}')
        
        # Add score component if this is followed by a variable
        if i < len(parts) - 1 and var_index < len(matches):
            var_name = matches[var_index]
            
            # Check if variable has scope selector
            if '<' in var_name and var_name.endswith('>'):
                # Scoped variable: $variable<selector>$
                var_parts = var_name.split('<', 1)
                base_var = var_parts[0]
                var_selector = var_parts[1][:-1]  # Remove trailing >
                components.append(f'{{"score":{{"name":"{var_selector}","objective":"{base_var}"}}}}')
            else:
                # Simple variable: $variable$ - use server armor stand
                components.append(f'{{"score":{{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"{var_name}"}}}}')
            
            var_index += 1
    
    # Combine all components
    components_str = ','.join(components)
    return f'tellraw @a [{components_str}]'


def _process_statement(statement: Any, namespace: str, function_name: str, statement_index: int = 0, is_tag_function: bool = False, selector: str = "@s", variable_scopes: Dict[str, str] = None, build_context: BuildContext = None) -> List[str]:
    """Process a single statement and return Minecraft commands."""
    if variable_scopes is None:
        variable_scopes = {}
    
    if build_context is None:
        build_context = BuildContext()
    
    commands = []
    
    if statement['type'] == 'command':
        command = statement['command']
        
        # Handle say commands specifically
        if command.startswith('say '):
            print(f"DEBUG: Found say command: {repr(command)}")
            # Convert say command to tellraw command
            content = command[4:]  # Remove "say " prefix
            print(f"DEBUG: Say command content: {repr(content)}")
            # Convert to Minecraft tellraw format
            processed_command = _process_say_command_with_variables(content, selector)
            print(f"DEBUG: Processed say command: {repr(processed_command)}")
            commands.append(processed_command)
        elif command.startswith('tellraw @a ') or command.startswith('tellraw @ a '):
            # Fix extra space in tellraw commands
            fixed_command = command.replace('tellraw @ a ', 'tellraw @a ')
            commands.append(fixed_command)
        else:
            # Process other commands normally
            processed_command = _process_variable_substitutions(command, selector)
            commands.append(processed_command)
    
    elif statement['type'] == 'variable_assignment':
        var_name = statement['name']
        value = statement['value']
        
        # Handle different value types
        if isinstance(value, int):
            commands.append(f"scoreboard players set {selector} {var_name} {value}")
        elif isinstance(value, str) and value.startswith('$') and value.endswith('$'):
            # Variable reference
            ref_var = value[1:-1]  # Remove $ symbols
            commands.append(f"scoreboard players operation {selector} {var_name} = {selector} {ref_var}")
        elif hasattr(value, '__class__') and 'BinaryExpression' in str(value.__class__):
            # Handle complex expressions (BinaryExpression, etc.)
            # Convert to proper Minecraft scoreboard commands
            if hasattr(value, 'left') and hasattr(value, 'right') and hasattr(value, 'operator'):
                left = value.left
                right = value.right
                operator = value.operator
                
                # Handle different operators
                if operator == 'PLUS':
                    if hasattr(left, 'name') and hasattr(right, 'value'):
                        # counter = counter + 1
                        commands.append(f"scoreboard players add {selector} {var_name} {right.value}")
                    else:
                        # Complex case - use operation
                        commands.append(f"# Complex addition: {var_name} = {left} + {right}")
                elif operator == 'MINUS':
                    if hasattr(left, 'name') and hasattr(right, 'value'):
                        # health = health - 10
                        commands.append(f"scoreboard players remove {selector} {var_name} {right.value}")
                    else:
                        # Complex case - use operation
                        commands.append(f"# Complex subtraction: {var_name} = {left} - {right}")
                else:
                    # Other operators - use operation
                    commands.append(f"# Complex operation: {var_name} = {left} {operator} {right}")
            else:
                commands.append(f"# Complex assignment: {var_name} = {value}")
        else:
            # Handle LiteralExpression and other value types
            try:
                if hasattr(value, 'value'):
                    # LiteralExpression case
                    num_value = int(value.value)
                    commands.append(f"scoreboard players set {selector} {var_name} {num_value}")
                else:
                    # Direct value case
                    num_value = int(value)
                    commands.append(f"scoreboard players set {selector} {var_name} {num_value}")
            except (ValueError, TypeError):
                # If we can't convert to int, add a placeholder
                commands.append(f"# Assignment: {var_name} = {value}")
    
    elif statement['type'] == 'if_statement':
        condition = statement['condition']
        then_body = statement['then_body']
        else_body = statement.get('else_body', [])
        
        # Convert condition to Minecraft syntax
        minecraft_condition = _convert_condition_to_minecraft_syntax(condition, selector)
        
        # Generate unique function names for conditional blocks
        if_func_name = f"{function_name}_if_{statement_index}"
        else_func_name = f"{function_name}_else_{statement_index}"
        
        # Create conditional function
        if_commands = []
        for i, stmt in enumerate(then_body):
            if_commands.extend(_process_statement(stmt, namespace, if_func_name, i, is_tag_function, selector, variable_scopes, build_context))
        
        # Write conditional function
        if if_commands:
            # Use the output directory from build context
            if hasattr(build_context, 'output_dir'):
                if_dir = build_context.output_dir / "data" / namespace / "function"
            else:
                if_dir = Path(f"data/{namespace}/function")
            ensure_dir(str(if_dir))
            with open(if_dir / f"{if_func_name}.mcfunction", 'w', encoding='utf-8') as f:
                f.write('\n'.join(if_commands))
        
        # Create else function if needed
        if else_body:
            else_commands = []
            for i, stmt in enumerate(else_body):
                else_commands.extend(_process_statement(stmt, namespace, else_func_name, i, is_tag_function, selector, variable_scopes, build_context))
            
            if else_commands:
                with open(if_dir / f"{else_func_name}.mcfunction", 'w', encoding='utf-8') as f:
                    f.write('\n'.join(else_commands))
        
        # Add the conditional execution command
        if else_body:
            commands.append(f"execute if {minecraft_condition} run function {namespace}:{if_func_name}")
            commands.append(f"execute unless {minecraft_condition} run function {namespace}:{else_func_name}")
            # Add if_end function call for cleanup
            commands.append(f"function {namespace}:{function_name}_if_end_{statement_index}")
        else:
            commands.append(f"execute if {minecraft_condition} run function {namespace}:{if_func_name}")
    
    elif statement['type'] == 'while_loop' or statement['type'] == 'while_statement':
        # Handle while loops using recursion
        loop_commands = _process_while_loop_recursion(statement, namespace, function_name, statement_index, is_tag_function, selector, variable_scopes, build_context)
        commands.extend(loop_commands)
    
    elif statement['type'] == 'function_call':
        func_name = statement['name']
        # Simple function call
        commands.append(f"function {namespace}:{func_name}")
    
    elif statement['type'] == 'raw_text':
        # Raw Minecraft commands
        raw_commands = statement['commands']
        for cmd in raw_commands:
            processed_cmd = _process_variable_substitutions(cmd, selector)
            commands.append(processed_cmd)
    
    return commands


def _generate_function_file(ast: Dict[str, Any], output_dir: Path, namespace: str, verbose: bool = False, build_context: BuildContext = None) -> None:
    """Generate function files from the AST for a specific namespace."""
    if build_context is None:
        build_context = BuildContext()
    
    if 'functions' not in ast:
        return
    
    # Filter functions by namespace
    namespace_functions = []
    for func in ast['functions']:
        # Check if function belongs to this namespace
        # For now, we'll generate all functions in all namespaces
        # In the future, we could add namespace annotations to functions
        namespace_functions.append(func)
    
    if verbose:
        print(f"DEBUG: Processing {len(namespace_functions)} functions for namespace {namespace}")
    
    for func in namespace_functions:
        func_name = func['name']
        func_body = func.get('body', [])
        
        # Generate function content
        function_commands = []
        for i, statement in enumerate(func_body):
            try:
                print(f"DEBUG: Processing statement {i} of type {statement.get('type', 'unknown')}: {statement}")
                commands = _process_statement(statement, namespace, func_name, i, False, "@s", {}, build_context)
                function_commands.extend(commands)
                print(f"Generated {len(commands)} commands for statement {i} in function {func_name}: {commands}")
            except Exception as e:
                print(f"Warning: Error processing statement {i} in function {func_name}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Write function file
        if function_commands:
            # Only add armor stand setup to main functions that need it
            # Don't add to helper functions or functions in the "other" namespace
            should_add_armor_stand = (namespace != "other" and 
                                    func_name in ["main", "init", "load"] or 
                                    any(cmd for cmd in function_commands if "scoreboard" in cmd or "tellraw" in cmd))
            
            final_commands = []
            if should_add_armor_stand:
                final_commands.append("execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:[\"mdl_server\"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}")
            final_commands.extend(function_commands)
            
            if verbose:
                print(f"DEBUG: Final commands for {func_name}: {final_commands}")
            
            func_dir = output_dir / "data" / namespace / "function"
            ensure_dir(str(func_dir))
            
            with open(func_dir / f"{func_name}.mcfunction", 'w', encoding='utf-8') as f:
                content = '\n'.join(final_commands)
                if verbose:
                    print(f"DEBUG: Writing to file {func_name}.mcfunction: {repr(content)}")
                f.write(content)
            
            if verbose:
                print(f"Generated function: {namespace}:{func_name}")
        else:
            if verbose:
                print(f"No commands generated for function: {namespace}:{func_name}")
                print(f"Function body: {func_body}")


def _generate_hook_files(ast: Dict[str, Any], output_dir: Path, namespace: str, build_context: BuildContext = None) -> None:
    """Generate load and tick tag files."""
    if build_context is None:
        build_context = BuildContext()
    
    # Generate load tag
    load_tag_dir = output_dir / "data" / "minecraft" / "tags" / "function"
    ensure_dir(str(load_tag_dir))
    
    # Start with the load function
    load_values = [f"{namespace}:load"]
    
    # Add functions specified in on_load hooks
    if 'hooks' in ast:
        for hook in ast['hooks']:
            if hook['hook_type'] == 'load':
                load_values.append(hook['function_name'])
    
    # Add pack-specific load function if pack name is available
    if 'pack' in ast and 'name' in ast['pack']:
        pack_name = ast['pack']['name']
        load_values.append(f"{pack_name}:load")
    
    load_tag_content = {
        "values": load_values
    }
    write_json(str(load_tag_dir / "load.json"), load_tag_content)
    
    # Generate tick tag if there are tick functions
    tick_functions = []
    if 'functions' in ast:
        for func in ast['functions']:
            if func.get('name', '').startswith('tick'):
                tick_functions.append(f"{namespace}:{func['name']}")
    
    if tick_functions:
        tick_tag_content = {
            "values": tick_functions
        }
        write_json(str(load_tag_dir / "tick.json"), tick_tag_content)


def _generate_global_load_function(ast: Dict[str, Any], output_dir: Path, namespace: str, build_context: BuildContext = None) -> None:
    """Generate the global load function."""
    if build_context is None:
        build_context = BuildContext()
    
    # Generate scoreboard objectives
    scoreboard_commands = _generate_scoreboard_objectives(ast, output_dir)
    
    # Generate load function
    _generate_load_function(scoreboard_commands, output_dir, namespace, ast)


def _generate_tag_files(ast: Dict[str, Any], output_dir: Path, namespace: str) -> None:
    """Generate tag files for the datapack."""
    # This is handled by _generate_hook_files
    pass


def _validate_pack_format(pack_format: int) -> None:
    """Validate the pack format number."""
    if not isinstance(pack_format, int) or pack_format < 1:
        raise ValueError(f"Invalid pack format: {pack_format}. Must be a positive integer.")


def _collect_conditional_functions(if_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s", variable_scopes: Dict[str, str] = None, build_context: BuildContext = None) -> List[str]:
    """Collect conditional functions from if statements."""
    if variable_scopes is None:
        variable_scopes = {}
    
    if build_context is None:
        build_context = BuildContext()
    
    conditional_functions = []
    
    # Generate function name for this conditional
    if_func_name = f"{function_name}_if_{statement_index}"
    conditional_functions.append(if_func_name)
    
    # Process then body
    for i, stmt in enumerate(if_statement['then_body']):
        if stmt['type'] == 'if_statement':
            nested_functions = _collect_conditional_functions(stmt, namespace, if_func_name, i, is_tag_function, selector, variable_scopes, build_context)
            conditional_functions.extend(nested_functions)
    
    # Process else body if it exists
    if 'else_body' in if_statement and if_statement['else_body']:
        else_func_name = f"{function_name}_else_{statement_index}"
        conditional_functions.append(else_func_name)
        
        for i, stmt in enumerate(if_statement['else_body']):
            if stmt['type'] == 'if_statement':
                nested_functions = _collect_conditional_functions(stmt, namespace, else_func_name, i, is_tag_function, selector, variable_scopes, build_context)
                conditional_functions.extend(nested_functions)
    
    return conditional_functions


def _process_while_loop_recursion(while_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s", variable_scopes: Dict[str, str] = None, build_context: BuildContext = None) -> List[str]:
    """Process while loops using recursive function calls."""
    if variable_scopes is None:
        variable_scopes = {}
    
    if build_context is None:
        build_context = BuildContext()
    
    condition = while_statement['condition']
    body = while_statement['body']
    
    # Generate unique function names
    loop_func_name = f"{function_name}_while_{statement_index}"
    loop_body_func_name = f"{function_name}_while_body_{statement_index}"
    
    # Process loop body
    body_commands = []
    for i, stmt in enumerate(body):
        body_commands.extend(_process_statement(stmt, namespace, loop_body_func_name, i, is_tag_function, selector, variable_scopes, build_context))
    
    # Write loop body function
    if body_commands:
        # Use the output directory from build context
        if hasattr(build_context, 'output_dir'):
            func_dir = build_context.output_dir / "data" / namespace / "function"
        else:
            func_dir = Path(f"data/{namespace}/function")
        ensure_dir(str(func_dir))
        with open(func_dir / f"{loop_body_func_name}.mcfunction", 'w', encoding='utf-8') as f:
            f.write('\n'.join(body_commands))
    
    # Create the main loop function
    minecraft_condition = _convert_condition_to_minecraft_syntax(condition, selector)
    loop_commands = [
        f"execute if {minecraft_condition} run function {namespace}:{loop_body_func_name}",
        f"execute if {minecraft_condition} run function {namespace}:{loop_func_name}"
    ]
    
    # Write loop function
    with open(func_dir / f"{loop_func_name}.mcfunction", 'w', encoding='utf-8') as f:
        f.write('\n'.join(loop_commands))
    
    # Return the command to start the loop with conditional execution
    return [f"execute if {minecraft_condition} run function {namespace}:{loop_func_name}"]


def _process_while_loop_schedule(while_statement, namespace: str, function_name: str, statement_index: int, is_tag_function: bool = False, selector: str = "@s", variable_scopes: Dict[str, str] = None, build_context: BuildContext = None) -> List[str]:
    """Process while loops using scheduled functions."""
    if variable_scopes is None:
        variable_scopes = {}
    
    if build_context is None:
        build_context = BuildContext()
    
    condition = while_statement['condition']
    body = while_statement['body']
    
    # Generate unique function names
    loop_func_name = f"{function_name}_while_{statement_index}"
    loop_body_func_name = f"{function_name}_while_body_{statement_index}"
    
    # Process loop body
    body_commands = []
    for i, stmt in enumerate(body):
        body_commands.extend(_process_statement(stmt, namespace, loop_body_func_name, i, is_tag_function, selector, variable_scopes, build_context))
    
    # Add the loop continuation command
    minecraft_condition = _convert_condition_to_minecraft_syntax(condition, selector)
    body_commands.append(f"execute {minecraft_condition} run schedule function {namespace}:{loop_body_func_name} 1t")
    
    # Write loop body function
    if body_commands:
        # Use the output directory from build context
        if hasattr(build_context, 'output_dir'):
            func_dir = build_context.output_dir / "data" / namespace / "function"
        else:
            func_dir = Path(f"data/{namespace}/function")
        ensure_dir(str(func_dir))
        with open(func_dir / f"{loop_body_func_name}.mcfunction", 'w', encoding='utf-8') as f:
            f.write('\n'.join(body_commands))
    
    # Return the command to start the loop
    return [f"schedule function {namespace}:{loop_body_func_name} 1t"]


def _create_zip_file(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from a directory."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)


def _generate_pack_mcmeta(ast: Dict[str, Any], output_dir: Path) -> None:
    """Generate the pack.mcmeta file."""
    pack_format = ast.get('pack', {}).get('format', 82)
    pack_description = ast.get('pack', {}).get('description', 'MDL Generated Datapack')
    
    pack_meta = {
        "pack": {
            "pack_format": pack_format,
            "description": pack_description
        }
    }
    
    write_json(str(output_dir / "pack.mcmeta"), pack_meta)


def _ast_to_pack(ast: Dict[str, Any], mdl_files: List[Path]) -> Pack:
    """Convert AST to Pack object."""
    pack_info = ast.get('pack', {})
    if pack_info is None:
        pack_info = {}
    pack_name = pack_info.get('name', 'mdl_pack')
    pack_format = pack_info.get('pack_format', 82)  # Use pack_format instead of format
    pack_description = pack_info.get('description', 'MDL Generated Datapack')
    
    pack = Pack(pack_name, pack_description, pack_format)
    
    # Add namespaces and functions
    if 'functions' in ast:
        # Get namespace name from AST or use pack name
        namespace_info = ast.get('namespace', {})
        if namespace_info is None:
            namespace_info = {}
        namespace_name = namespace_info.get('name', pack_name)
        namespace = pack.namespace(namespace_name)
        
        for func in ast['functions']:
            function_name = func['name']
            # Create function and add commands if they exist
            function = namespace.function(function_name)
            
            # Add commands from function body if they exist
            if 'body' in func:
                for i, statement in enumerate(func['body']):
                    try:
                        # Use the same processing logic as the build system
                        commands = _process_statement(statement, namespace_name, function_name, i, False, "@s", {}, BuildContext())
                        function.commands.extend(commands)
                    except Exception as e:
                        # If processing fails, try to add as simple command
                        if statement.get('type') == 'command':
                            function.commands.append(statement['command'])
                        elif statement.get('type') == 'function_call':
                            function.commands.append(f"function {statement['name']}")
                        elif statement.get('type') == 'variable_assignment':
                            # Handle variable assignments
                            var_name = statement['name']
                            value = statement['value']
                            if hasattr(value, 'value'):
                                # Simple literal value
                                function.commands.append(f"scoreboard players set {var_name} @s {value.value}")
                            else:
                                # Complex expression - add a placeholder
                                function.commands.append(f"# Variable assignment: {var_name} = {value}")
                        else:
                            # Add a placeholder for other statement types
                            function.commands.append(f"# Statement: {statement.get('type', 'unknown')}")
    
    # Add variables
    if 'variables' in ast:
        for var in ast['variables']:
            # Variables are handled during command processing
            pass
    
    # Add hooks
    if 'hooks' in ast:
        for hook in ast['hooks']:
            if hook['hook_type'] == 'load':
                pack.on_load(hook['function_name'])
            elif hook['hook_type'] == 'tick':
                pack.on_tick(hook['function_name'])
    
    # Add recipes
    if 'recipes' in ast:
        namespace_info = ast.get('namespace', {})
        if namespace_info is None:
            namespace_info = {}
        namespace_name = namespace_info.get('name', pack_name)
        namespace = pack.namespace(namespace_name)
        
        for recipe in ast['recipes']:
            recipe_name = recipe['name']
            recipe_data = recipe['data']
            # Create recipe object
            from .pack import Recipe
            recipe_obj = Recipe(recipe_name, recipe_data)
            namespace.recipes[recipe_name] = recipe_obj
    
    # Add advancements
    if 'advancements' in ast:
        namespace_info = ast.get('namespace', {})
        if namespace_info is None:
            namespace_info = {}
        namespace_name = namespace_info.get('name', pack_name)
        namespace = pack.namespace(namespace_name)
        
        for advancement in ast['advancements']:
            advancement_name = advancement['name']
            advancement_data = advancement['data']
            # Create advancement object
            from .pack import Advancement
            advancement_obj = Advancement(advancement_name, advancement_data)
            namespace.advancements[advancement_name] = advancement_obj
    
    # Add loot tables
    if 'loot_tables' in ast:
        namespace_info = ast.get('namespace', {})
        if namespace_info is None:
            namespace_info = {}
        namespace_name = namespace_info.get('name', pack_name)
        namespace = pack.namespace(namespace_name)
        
        for loot_table in ast['loot_tables']:
            loot_table_name = loot_table['name']
            loot_table_data = loot_table['data']
            # Create loot table object
            from .pack import LootTable
            loot_table_obj = LootTable(loot_table_name, loot_table_data)
            namespace.loot_tables[loot_table_name] = loot_table_obj
    
    return pack


def build_mdl(input_path: str, output_path: str, verbose: bool = False, pack_format_override: Optional[int] = None, wrapper: Optional[str] = None, ignore_warnings: bool = False) -> None:
    """Build MDL files into a Minecraft datapack."""
    error_collector = MDLErrorCollector()
    
    try:
        input_dir = Path(input_path)
        output_dir = Path(output_path)
        
        # Validate input directory exists
        if not input_dir.exists():
            error_collector.add_error(create_error(
                MDLFileError,
                f"Input path does not exist: {input_path}",
                file_path=input_path,
                suggestion="Check the path and ensure the file or directory exists."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Find MDL files
        mdl_files = _find_mdl_files(input_dir)
        
        if not mdl_files:
            error_collector.add_error(create_error(
                MDLFileError,
                f"No .mdl files found in {input_path}",
                file_path=input_path,
                suggestion="Ensure the directory contains .mdl files or specify a single .mdl file."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        if verbose:
            print(f"Found {len(mdl_files)} MDL file(s):")
            for file in mdl_files:
                print(f"  - {file}")
        
        # Merge and parse MDL files
        ast = _merge_mdl_files(mdl_files, verbose, error_collector)
        
        if ast is None:
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Override pack format if specified
        if pack_format_override is not None:
            _validate_pack_format(pack_format_override)
            if 'pack' not in ast:
                ast['pack'] = {}
            ast['pack']['format'] = pack_format_override
        
        # Create output directory
        ensure_dir(str(output_dir))
        
        # Generate pack.mcmeta
        _generate_pack_mcmeta(ast, output_dir)
        
        # Handle multiple namespaces from multiple files
        namespaces = []
        
        # Get namespaces from AST
        if 'namespaces' in ast:
            for ns in ast['namespaces']:
                if 'name' in ns:
                    namespaces.append(_slugify(ns['name']))
        
        # If no explicit namespaces, use the pack name as default
        if not namespaces:
            default_namespace = ast.get('pack', {}).get('name', 'mdl_pack')
            namespaces.append(_slugify(default_namespace))
        
        # Debug: Show what namespaces we're using
        if verbose:
            print(f"DEBUG: AST namespaces: {ast.get('namespaces', [])}")
            print(f"DEBUG: AST pack: {ast.get('pack', {})}")
            print(f"DEBUG: Using namespaces: {namespaces}")
        
        # Generate functions for each namespace
        build_context = BuildContext()
        for namespace in namespaces:
            if verbose:
                print(f"DEBUG: Processing namespace: {namespace}")
            _generate_function_file(ast, output_dir, namespace, verbose, build_context)
        
        # Generate hook files (load/tick tags) - use first namespace for global functions
        primary_namespace = namespaces[0] if namespaces else 'mdl_pack'
        _generate_hook_files(ast, output_dir, primary_namespace, build_context)
        
        # Generate global load function - use first namespace for global functions
        _generate_global_load_function(ast, output_dir, primary_namespace, build_context)
        
        # Create zip file (always create one, use wrapper name if specified)
        zip_name = wrapper if wrapper else output_dir.name
        # When using wrapper, create zip in output directory; otherwise in parent directory
        if wrapper:
            zip_path = output_dir / f"{zip_name}.zip"
        else:
            zip_path = output_dir.parent / f"{zip_name}.zip"
        _create_zip_file(output_dir, zip_path)
        if verbose:
            print(f"[ZIP] Created zip file: {zip_path}")
        
        print(f"[OK] Successfully built datapack: {output_path}")
        if verbose:
            print(f"[DIR] Output directory: {output_dir}")
            print(f"[NS] Namespace: {namespace}")
    
    except MDLLexerError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except MDLParserError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except MDLSyntaxError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except MDLBuildError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except MDLFileError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except MDLCompilationError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
    except Exception as e:
        error_collector.add_error(create_error(
            MDLBuildError,
            f"Unexpected error during build: {str(e)}",
            suggestion="Check the input files and try again. If the problem persists, report this as a bug."
        ))
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
