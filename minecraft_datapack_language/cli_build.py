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
        
        tokens = lex_mdl_js(content, str(files[0]))
        ast = parse_mdl_js(tokens, str(files[0]))
        
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
            
            tokens = lex_mdl_js(content, str(file_path))
            additional_ast = parse_mdl_js(tokens, str(file_path))
            
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


def _process_statement(statement: Any, namespace: str, function_name: str, statement_index: int = 0, is_tag_function: bool = False, selector: str = "@s", variable_scopes: Dict[str, str] = None, build_context: BuildContext = None) -> List[str]:
    """Process a single statement and return Minecraft commands."""
    if variable_scopes is None:
        variable_scopes = {}
    
    if build_context is None:
        build_context = BuildContext()
    
    commands = []
    
    if statement['type'] == 'command':
        command = statement['command']
        processed_command = _process_variable_substitutions(command, selector)
        commands.append(processed_command)
    
    elif statement['type'] == 'variable_assignment':
        var_name = statement['name']
        value = statement['value']
        
        # Handle different value types
        if isinstance(value, int):
            commands.append(f"scoreboard players set {var_name} {selector} {value}")
        elif isinstance(value, str) and value.startswith('$') and value.endswith('$'):
            # Variable reference
            ref_var = value[1:-1]  # Remove $ symbols
            commands.append(f"scoreboard players operation {var_name} {selector} = {ref_var} {selector}")
        else:
            # Assume it's a number
            try:
                num_value = int(value)
                commands.append(f"scoreboard players set {var_name} {selector} {num_value}")
            except ValueError:
                raise ValueError(f"Invalid value for variable {var_name}: {value}")
    
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
            commands.append(f"execute {minecraft_condition} run function {namespace}:{if_func_name}")
            commands.append(f"execute unless {minecraft_condition} run function {namespace}:{else_func_name}")
        else:
            commands.append(f"execute {minecraft_condition} run function {namespace}:{if_func_name}")
    
    elif statement['type'] == 'while_loop':
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
    """Generate function files from the AST."""
    if build_context is None:
        build_context = BuildContext()
    
    if 'functions' not in ast:
        return
    
    for func in ast['functions']:
        func_name = func['name']
        func_body = func.get('body', [])
        
        # Generate function content
        function_commands = []
        for i, statement in enumerate(func_body):
            try:
                commands = _process_statement(statement, namespace, func_name, i, False, "@s", {}, build_context)
                function_commands.extend(commands)
            except Exception as e:
                if verbose:
                    print(f"Warning: Error processing statement {i} in function {func_name}: {e}")
                continue
        
        # Write function file
        if function_commands:
            func_dir = output_dir / "data" / namespace / "function"
            ensure_dir(str(func_dir))
            
            with open(func_dir / f"{func_name}.mcfunction", 'w', encoding='utf-8') as f:
                f.write('\n'.join(function_commands))
            
            if verbose:
                print(f"Generated function: {namespace}:{func_name}")


def _generate_hook_files(ast: Dict[str, Any], output_dir: Path, namespace: str, build_context: BuildContext = None) -> None:
    """Generate load and tick tag files."""
    if build_context is None:
        build_context = BuildContext()
    
    # Generate load tag
    load_tag_dir = output_dir / "data" / "minecraft" / "tags" / "function"
    ensure_dir(str(load_tag_dir))
    
    load_tag_content = {
        "values": [f"{namespace}:load"]
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
        func_dir = Path(f"data/{namespace}/function")
        ensure_dir(str(func_dir))
        with open(func_dir / f"{loop_body_func_name}.mcfunction", 'w', encoding='utf-8') as f:
            f.write('\n'.join(body_commands))
    
    # Create the main loop function
    minecraft_condition = _convert_condition_to_minecraft_syntax(condition, selector)
    loop_commands = [
        f"execute {minecraft_condition} run function {namespace}:{loop_body_func_name}",
        f"execute {minecraft_condition} run function {namespace}:{loop_func_name}"
    ]
    
    # Write loop function
    with open(func_dir / f"{loop_func_name}.mcfunction", 'w', encoding='utf-8') as f:
        f.write('\n'.join(loop_commands))
    
    # Return the command to start the loop
    return [f"function {namespace}:{loop_func_name}"]


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
    pack_name = pack_info.get('name', 'mdl_pack')
    pack_format = pack_info.get('format', 82)
    pack_description = pack_info.get('description', 'MDL Generated Datapack')
    
    pack = Pack(pack_name, pack_format, pack_description)
    
    # Add namespaces
    if 'functions' in ast:
        namespace = Namespace(pack_name)
        
        for func in ast['functions']:
            function = Function(func['name'])
            namespace.add_function(function)
        
        pack.add_namespace(namespace)
    
    return pack


def build_mdl(input_path: str, output_path: str, verbose: bool = False, pack_format_override: Optional[int] = None, wrapper: Optional[str] = None) -> None:
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
            error_collector.print_errors(verbose=True)
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
            error_collector.print_errors(verbose=True)
            error_collector.raise_if_errors()
            return
        
        if verbose:
            print(f"Found {len(mdl_files)} MDL file(s):")
            for file in mdl_files:
                print(f"  - {file}")
        
        # Merge and parse MDL files
        ast = _merge_mdl_files(mdl_files, verbose, error_collector)
        
        if ast is None:
            error_collector.print_errors(verbose=True)
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
        
        # Get namespace from pack name or use default
        namespace = ast.get('pack', {}).get('name', 'mdl_pack')
        namespace = _slugify(namespace)
        
        # Generate functions
        build_context = BuildContext()
        _generate_function_file(ast, output_dir, namespace, verbose, build_context)
        
        # Generate hook files (load/tick tags)
        _generate_hook_files(ast, output_dir, namespace, build_context)
        
        # Generate global load function
        _generate_global_load_function(ast, output_dir, namespace, build_context)
        
        # Create zip file if wrapper is specified
        if wrapper:
            zip_path = output_dir.parent / f"{wrapper}.zip"
            _create_zip_file(output_dir, zip_path)
            if verbose:
                print(f"📦 Created zip file: {zip_path}")
        
        print(f"✅ Successfully built datapack: {output_path}")
        if verbose:
            print(f"📁 Output directory: {output_dir}")
            print(f"🏷️  Namespace: {namespace}")
    
    except MDLLexerError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except MDLParserError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except MDLSyntaxError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except MDLBuildError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except MDLFileError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except MDLCompilationError as e:
        error_collector.add_error(e)
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
    except Exception as e:
        error_collector.add_error(create_error(
            MDLBuildError,
            f"Unexpected error during build: {str(e)}",
            suggestion="Check the input files and try again. If the problem persists, report this as a bug."
        ))
        error_collector.print_errors(verbose=True)
        error_collector.raise_if_errors()
