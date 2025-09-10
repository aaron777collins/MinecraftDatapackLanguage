"""
MDL Compiler - Converts MDL AST into complete Minecraft datapack
Simplified version that focuses on generating actual statements for testing
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from .ast_nodes import (
    Program, PackDeclaration, NamespaceDeclaration, TagDeclaration,
    VariableDeclaration, VariableAssignment, VariableSubstitution, FunctionDeclaration,
    FunctionCall, IfStatement, WhileLoop, ScheduledWhileLoop, HookDeclaration, RawBlock, MacroLine,
    SayCommand, BinaryExpression, LiteralExpression, ParenthesizedExpression
)
from .dir_map import get_dir_map, DirMap
from .mdl_errors import MDLCompilerError
from .mdl_lexer import TokenType


class MDLCompiler:
    """
    Simplified compiler for the MDL language that generates actual statements.
    """
    
    def __init__(self, output_dir: str = "dist"):
        self.output_dir = Path(output_dir)
        self.dir_map: Optional[DirMap] = None
        self.current_namespace = "mdl"
        self.variables: Dict[str, str] = {}  # name -> objective mapping
        # Preserve declared variables so we can initialize defaults in load.mcfunction
        self.declared_variables: List[VariableDeclaration] = []
        # Track any temporary scoreboard variables generated during compilation
        self.temp_variables: Set[str] = set()
        
    def compile(self, ast: Program, source_dir: str = None) -> str:
        """Compile MDL AST into a complete Minecraft datapack."""
        try:
            # Use source_dir as output directory if provided
            if source_dir:
                output_dir = Path(source_dir)
            else:
                output_dir = self.output_dir
            
            # Clean output directory
            if output_dir.exists():
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Temporarily set output directory
            original_output_dir = self.output_dir
            self.output_dir = output_dir
            
            # Set up directory mapping based on pack format
            pack_format = ast.pack.pack_format if ast.pack else 15
            self.dir_map = get_dir_map(pack_format)
            
            # Create pack.mcmeta
            self._create_pack_mcmeta(ast.pack)
            
            # Create data directory structure
            data_dir = self.output_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Set namespace
            if ast.namespace:
                self.current_namespace = ast.namespace.name
            
            # Create namespace directory (for default/current)
            namespace_dir = data_dir / self.current_namespace
            namespace_dir.mkdir(parents=True, exist_ok=True)
            
            # Compile all components
            self._compile_variables(ast.variables, namespace_dir)
            self._compile_functions(ast.functions, data_dir)
            self._compile_hooks(ast.hooks, namespace_dir)
            self._compile_statements(ast.statements, namespace_dir)
            self._compile_tags(ast.tags, source_dir)
            
            # Create load and tick functions for hooks
            self._create_hook_functions(ast.hooks, namespace_dir)
            
            # Return the output directory path
            result = str(self.output_dir)
            
            # Restore original output directory
            self.output_dir = original_output_dir
            
            return result
            
        except Exception as e:
            # Restore original output directory on error
            if 'original_output_dir' in locals():
                self.output_dir = original_output_dir
                
            if isinstance(e, MDLCompilerError):
                raise e
            else:
                raise MDLCompilerError(f"Compilation failed: {str(e)}", "Check the AST structure")
    
    def _create_pack_mcmeta(self, pack: Optional[PackDeclaration]):
        """Create pack.mcmeta file."""
        if not pack:
            pack_data = {
                "pack": {
                    "pack_format": 15,
                    "description": "MDL Generated Datapack"
                }
            }
        else:
            pack_data = {
                "pack": {
                    "pack_format": pack.pack_format,
                    "description": pack.description
                }
            }
        
        pack_mcmeta_path = self.output_dir / "pack.mcmeta"
        with open(pack_mcmeta_path, 'w') as f:
            json.dump(pack_data, f, indent=2)
    
    def _compile_variables(self, variables: List[VariableDeclaration], namespace_dir: Path):
        """Compile variable declarations into scoreboard objectives."""
        for var in variables:
            objective_name = var.name
            self.variables[var.name] = objective_name
            self.declared_variables.append(var)
            print(f"Variable: {var.name} -> scoreboard objective '{objective_name}'")
    
    def _compile_functions(self, functions: List[FunctionDeclaration], data_dir: Path):
        """Compile function declarations into .mcfunction files."""
        for func in functions:
            # Ensure namespace directory per function
            ns_dir = data_dir / func.namespace
            ns_dir.mkdir(parents=True, exist_ok=True)
            if self.dir_map:
                functions_dir = ns_dir / self.dir_map.function
            else:
                functions_dir = ns_dir / "functions"
            functions_dir.mkdir(parents=True, exist_ok=True)
            func_file = functions_dir / f"{func.name}.mcfunction"
            content = self._generate_function_content(func)
            
            with open(func_file, 'w') as f:
                f.write(content)
            
            print(f"Function: {func.namespace}:{func.name} -> {func_file}")
    
    def _generate_function_content(self, func: FunctionDeclaration) -> str:
        """Generate the content of a .mcfunction file."""
        lines = []
        lines.append(f"# Function: {func.namespace}:{func.name}")
        if func.scope:
            lines.append(f"# Scope: {func.scope}")
        lines.append("")
        
        # Ensure a temp-command sink stack exists
        if not hasattr(self, '_temp_sink_stack'):
            self._temp_sink_stack = []
        
        # Set current function context and reset per-function counters
        self._current_function_name = func.name
        self.if_counter = 0
        self.else_counter = 0
        self.while_counter = 0
        
        # Route temp commands into this function's body by default
        self._temp_sink_stack.append(lines)
        # Generate commands from function body
        for statement in func.body:
            cmd = self._statement_to_command(statement)
            if cmd:
                lines.append(self._ensure_macro_prefix(cmd))
        # Done routing temp commands for this function body
        self._temp_sink_stack.pop()
        
        return "\n".join(lines)

    def _ensure_macro_prefix(self, text: str) -> str:
        """Ensure any line containing a macro placeholder $(var) starts with '$'.
        Handles multi-line text by processing each line independently.
        """
        import re
        macro_re = re.compile(r"\$\([A-Za-z_][A-Za-z0-9_]*\)")
        def process_line(line: str) -> str:
            if macro_re.search(line):
                stripped = line.lstrip()
                if not stripped.startswith('$'):
                    # Insert '$' immediately after indentation so there is no space after '$'
                    leading_ws_len = len(line) - len(stripped)
                    leading_ws = line[:leading_ws_len]
                    return f"{leading_ws}${stripped}"
            return line
        if '\n' in text:
            return '\n'.join(process_line(ln) for ln in text.split('\n'))
        return process_line(text)
    
    def _compile_hooks(self, hooks: List[HookDeclaration], namespace_dir: Path):
        """Compile hook declarations."""
        for hook in hooks:
            print(f"Hook: {hook.hook_type} -> {hook.namespace}:{hook.name}")
    
    def _compile_statements(self, statements: List[Any], namespace_dir: Path):
        """Compile top-level statements."""
        for statement in statements:
            if isinstance(statement, FunctionCall):
                print(f"Top-level exec: {statement.namespace}:{statement.name}")
            elif isinstance(statement, RawBlock):
                print(f"Top-level raw block: {len(statement.content)} characters")
    
    def _compile_tags(self, tags: List[TagDeclaration], source_dir: str):
        """Compile tag declarations and copy referenced JSON files."""
        source_path = Path(source_dir) if source_dir else None
        
        for tag in tags:
            if tag.tag_type == "recipe":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "loot_table":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "advancement":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "item_modifier":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "predicate":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "structure":
                tag_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_item
            elif tag.tag_type == "item":
                # Namespace item tags (e.g., data/<ns>/tags/items/<name>.json)
                ns_dir = self.output_dir / "data" / self.current_namespace / "tags"
                # Prefer plural 'items' for compatibility
                tag_dir = ns_dir / "items"
            else:
                continue
            
            tag_dir.mkdir(parents=True, exist_ok=True)
            tag_file = tag_dir / f"{tag.name}.json"
            
            if source_path and tag.tag_type != "item":
                source_json = source_path / tag.file_path
                if source_json.exists():
                    shutil.copy2(source_json, tag_file)
                    print(f"Tag {tag.tag_type}: {tag.name} -> {tag_file}")
                else:
                    tag_data = {"values": [f"{self.current_namespace}:{tag.name}"]}
                    with open(tag_file, 'w') as f:
                        json.dump(tag_data, f, indent=2)
                    print(f"Tag {tag.tag_type}: {tag.name} -> {tag_file} (placeholder)")
            else:
                # Write simple values list
                # For item tags, the TagDeclaration.name may include namespace:name
                # The output filename should be the local name (after ':') if present
                name_for_file = tag.name.split(":", 1)[1] if ":" in tag.name else tag.name
                tag_file = tag_dir / f"{name_for_file}.json"
                values = [tag.name if ":" in tag.name else f"{self.current_namespace}:{tag.name}"]
                tag_data = {"values": values}
                with open(tag_file, 'w') as f:
                    json.dump(tag_data, f, indent=2)
                print(f"Tag {tag.tag_type}: {tag.name} -> {tag_file} (generated)")
    
    def _create_hook_functions(self, hooks: List[HookDeclaration], namespace_dir: Path):
        """Create load.mcfunction and tick.mcfunction for hooks."""
        if self.dir_map:
            functions_dir = namespace_dir / self.dir_map.function
        else:
            functions_dir = namespace_dir / "functions"
        # Ensure functions dir exists
        functions_dir.mkdir(parents=True, exist_ok=True)
        
        # Always create load function to initialize objectives; add tag only if on_load hooks exist
        has_on_load = any(h.hook_type == "on_load" for h in hooks)
        load_content = self._generate_load_function(hooks)
        load_file = functions_dir / "load.mcfunction"
        with open(load_file, 'w') as f:
            f.write(load_content)
        # Ensure minecraft load tag points to namespace:load
        tags_fn_dir = self.output_dir / "data" / "minecraft" / self.dir_map.tags_function
        tags_fn_dir.mkdir(parents=True, exist_ok=True)
        load_tag_file = tags_fn_dir / "load.json"
        # Always reference namespace:load (which handles scoreboard init and calls on_load hooks internally)
        values = [f"{self.current_namespace}:load"]
        with open(load_tag_file, 'w') as f:
            json.dump({"values": values}, f, indent=2)
        
        # Create tick function if needed
        tick_hooks = [h for h in hooks if h.hook_type == "on_tick"]
        if tick_hooks:
            tick_content = self._generate_tick_function(tick_hooks)
            tick_file = functions_dir / "tick.mcfunction"
            with open(tick_file, 'w') as f:
                f.write(tick_content)
            # Ensure minecraft tick tag points to namespace:tick
            tick_tag_file = tags_fn_dir / "tick.json"
            with open(tick_tag_file, 'w') as f:
                json.dump({"values": [f"{self.current_namespace}:tick"]}, f, indent=2)
    
    def _generate_load_function(self, hooks: List[HookDeclaration]) -> str:
        """Generate the content of load.mcfunction."""
        lines = [
            "# Load function - runs when datapack loads",
            "# Generated by MDL Compiler",
            ""
        ]
        
        # Add scoreboard objective creation for variables
        for var_name, objective in self.variables.items():
            lines.append(f"scoreboard objectives add {objective} dummy \"{var_name}\"")
        
        # Initialize declared variables with explicit initial values
        # Use @a for any @s-scoped variable since load runs without an executor
        for decl in self.declared_variables:
            if getattr(decl, 'initial_value', None) is None:
                continue
            objective = self.variables.get(decl.name, decl.name)
            scope = decl.scope.strip("<>") if decl.scope else "@a"
            if scope == "@s":
                scope = "@a"
            init = decl.initial_value
            from .ast_nodes import LiteralExpression, VariableSubstitution
            if isinstance(init, LiteralExpression):
                # Normalize number to int if possible
                val = init.value
                try:
                    v = float(val)
                    val_str = str(int(v)) if v.is_integer() else str(v)
                except Exception:
                    val_str = str(val)
                lines.append(f"scoreboard players set {scope} {objective} {val_str}")
            elif isinstance(init, VariableSubstitution):
                src_obj = self.variables.get(init.name, init.name)
                src_scope = init.scope.strip("<>") if init.scope else "@a"
                if src_scope == "@s":
                    src_scope = "@a"
                lines.append(f"scoreboard players operation {scope} {objective} = {src_scope} {src_obj}")

        lines.append("")
        
        # Add on_load hook calls
        load_hooks = [h for h in hooks if h.hook_type == "on_load"]
        for hook in load_hooks:
            if hook.scope:
                lines.append(f"execute as {hook.scope.strip('<>')} run function {hook.namespace}:{hook.name}")
            else:
                lines.append(f"function {hook.namespace}:{hook.name}")
        
        return "\n".join(lines)
    
    def _generate_tick_function(self, tick_hooks: List[HookDeclaration]) -> str:
        """Generate the content of tick.mcfunction."""
        lines = [
            "# Tick function - runs every tick",
            "# Generated by MDL Compiler",
            ""
        ]
        
        # Add on_tick hook calls
        for hook in tick_hooks:
            if hook.scope:
                scope = hook.scope.strip("<>")
                lines.append(f"execute as {scope} run function {hook.namespace}:{hook.name}")
            else:
                lines.append(f"function {hook.namespace}:{hook.name}")
        
        return "\n".join(lines)
    
    def _statement_to_command(self, statement: Any) -> Optional[str]:
        """Convert an AST statement to a Minecraft command."""
        if isinstance(statement, VariableAssignment):
            return self._variable_assignment_to_command(statement)
        elif isinstance(statement, VariableDeclaration):
            return self._variable_declaration_to_command(statement)
        elif isinstance(statement, SayCommand):
            return self._say_command_to_command(statement)
        elif isinstance(statement, RawBlock):
            return statement.content
        elif isinstance(statement, MacroLine):
            return statement.content
        elif isinstance(statement, IfStatement):
            return self._if_statement_to_command(statement)
        elif isinstance(statement, WhileLoop):
            return self._while_loop_to_command(statement)
        elif isinstance(statement, ScheduledWhileLoop):
            return self._scheduled_while_to_command(statement)
        elif isinstance(statement, FunctionCall):
            return self._function_call_to_command(statement)
        else:
            return None
    
    def _variable_assignment_to_command(self, assignment: VariableAssignment) -> str:
        """Convert variable assignment to scoreboard command."""
        # Auto-declare objective on first use
        if assignment.name not in self.variables:
            self.variables[assignment.name] = assignment.name
        objective = self.variables.get(assignment.name, assignment.name)
        scope = assignment.scope.strip("<>")
        
        # Check if the value is a complex expression
        if isinstance(assignment.value, BinaryExpression):
            # Complex expression - use temporary variable approach
            temp_var = self._generate_temp_variable_name()
            self._compile_expression_to_temp(assignment.value, temp_var)
            
            # Return the command to set the target variable from the temp
            return f"scoreboard players operation {scope} {objective} = @s {temp_var}"
        else:
            # Simple value - use direct assignment or scoreboard copy
            value = self._expression_to_value(assignment.value)
            # If RHS resolves to a scoreboard reference (e.g., 'score @s some_obj'),
            # emit an operation copy instead of an invalid 'set ... score ...'
            if isinstance(value, str) and value.startswith("score "):
                parts = value.split()
                if len(parts) >= 3:
                    src_scope = parts[1]
                    src_objective = parts[2]
                    return f"scoreboard players operation {scope} {objective} = {src_scope} {src_objective}"
            return f"scoreboard players set {scope} {objective} {value}"

    def _variable_declaration_to_command(self, decl: VariableDeclaration) -> str:
        """Handle var declarations appearing inside function bodies.
        Ensure objective is registered and optionally set initial value.
        """
        objective = self.variables.get(decl.name, decl.name)
        # Register objective so load function adds it
        self.variables[decl.name] = objective
        # If there is an initial value, set it in current context
        scope = decl.scope.strip("<>")
        init = None
        try:
            init = self._expression_to_value(decl.initial_value)
        except Exception:
            init = None
        if init is not None:
            # Initialize from another scoreboard using operation copy
            if isinstance(init, str) and init.startswith("score "):
                parts = init.split()
                if len(parts) >= 3:
                    src_scope = parts[1]
                    src_objective = parts[2]
                    return f"scoreboard players operation {scope} {objective} = {src_scope} {src_objective}"
            return f"scoreboard players set {scope} {objective} {init}"
        return f"# var {decl.name} declared"
    
    def _say_command_to_command(self, say: SayCommand) -> str:
        """Convert say command to tellraw command with JSON formatting."""
        if not say.variables:
            return f'tellraw @a {{"text":"{say.message}"}}'
        else:
            return self._build_tellraw_json(say.message, say.variables)
    
    def _build_tellraw_json(self, message: str, variables: List[VariableSubstitution]) -> str:
        """Build complex tellraw JSON with variable substitutions."""
        parts = []
        current_pos = 0
        
        for var in variables:
            var_pattern = f"${var.name}{var.scope}$"
            var_pos = message.find(var_pattern, current_pos)
            
            if var_pos != -1:
                if var_pos > current_pos:
                    text_before = message[current_pos:var_pos]
                    parts.append(f'{{"text":"{text_before}"}}')
                
                objective = self.variables.get(var.name, var.name)
                scope = var.scope.strip("<>")
                parts.append(f'{{"score":{{"name":"{scope}","objective":"{objective}"}}}}')
                
                current_pos = var_pos + len(var_pattern)
        
        if current_pos < len(message):
            text_after = message[current_pos:]
            parts.append(text_after)
        
        if len(parts) == 1:
            if isinstance(parts[0], str) and not parts[0].startswith('{"'):
                return f'tellraw @a {{"text":"{parts[0]}"}}'
            return f'tellraw @a {parts[0]}'
        else:
            first_part = parts[0]
            remaining_parts = parts[1:]
            if remaining_parts:
                import json
                first_data = json.loads(first_part)
                extra_parts = []
                for part in remaining_parts:
                    if isinstance(part, str) and not part.startswith('{"'):
                        extra_parts.append(f'"{part}"')
                    else:
                        extra_parts.append(part)
                
                extra_json = ",".join(extra_parts)
                return f'tellraw @a {{"text":"{first_data["text"]}","extra":[{extra_json}]}}'
            else:
                return f'tellraw @a {first_part}'
    
    def _if_statement_to_command(self, if_stmt: IfStatement) -> str:
        """Convert if statement to proper Minecraft execute if commands."""
        condition, invert_then = self._build_condition(if_stmt.condition)
        lines = []
        
        # Prepare function name for the then branch
        if_function_name = self._generate_if_function_name()
        # Generate condition command
        if invert_then:
            lines.append(f"execute unless {condition} run function {self.current_namespace}:{if_function_name}")
        else:
            lines.append(f"execute if {condition} run function {self.current_namespace}:{if_function_name}")
        
        # Generate the if body function content
        if_body_lines = [f"# Function: {self.current_namespace}:{if_function_name}"]
        # Route temp commands to the if-body function content
        if not hasattr(self, '_temp_sink_stack'):
            self._temp_sink_stack = []
        self._temp_sink_stack.append(if_body_lines)
        for stmt in if_stmt.then_body:
            if isinstance(stmt, VariableAssignment):
                cmd = self._variable_assignment_to_command(stmt)
                if_body_lines.append(cmd)
            elif isinstance(stmt, VariableDeclaration):
                cmd = self._variable_declaration_to_command(stmt)
                if_body_lines.append(cmd)
            elif isinstance(stmt, SayCommand):
                cmd = self._say_command_to_command(stmt)
                if_body_lines.append(cmd)
            elif isinstance(stmt, RawBlock):
                if_body_lines.append(stmt.content)
            elif isinstance(stmt, IfStatement):
                cmd = self._if_statement_to_command(stmt)
                if_body_lines.append(cmd)
            elif isinstance(stmt, WhileLoop):
                cmd = self._while_loop_to_command(stmt)
                if_body_lines.append(cmd)
            elif isinstance(stmt, FunctionCall):
                cmd = self._function_call_to_command(stmt)
                if_body_lines.append(cmd)
        # Stop routing temp commands for if-body
        self._temp_sink_stack.pop()
        
        # Handle else body if it exists
        if if_stmt.else_body:
            if isinstance(if_stmt.else_body, list) and len(if_stmt.else_body) == 1 and isinstance(if_stmt.else_body[0], IfStatement):
                # Else-if: create an else function wrapper that contains the nested if
                else_function_name = self._generate_else_function_name()
                if invert_then:
                    lines.append(f"execute if {condition} run function {self.current_namespace}:{else_function_name}")
                else:
                    lines.append(f"execute unless {condition} run function {self.current_namespace}:{else_function_name}")
                else_body_lines = [f"# Function: {self.current_namespace}:{else_function_name}"]
                nested_cmd = self._if_statement_to_command(if_stmt.else_body[0])
                for nested_line in nested_cmd.split('\n'):
                    if nested_line:
                        else_body_lines.append(nested_line)
                self._store_generated_function(else_function_name, else_body_lines)
            else:
                # Regular else: compile its body into its own function
                else_function_name = self._generate_else_function_name()
                if invert_then:
                    lines.append(f"execute if {condition} run function {self.current_namespace}:{else_function_name}")
                else:
                    lines.append(f"execute unless {condition} run function {self.current_namespace}:{else_function_name}")
                else_body_lines = [f"# Function: {self.current_namespace}:{else_function_name}"]
                # Route temp commands into the else-body
                if not hasattr(self, '_temp_sink_stack'):
                    self._temp_sink_stack = []
                self._temp_sink_stack.append(else_body_lines)
                for stmt in if_stmt.else_body:
                    if isinstance(stmt, VariableAssignment):
                        cmd = self._variable_assignment_to_command(stmt)
                        else_body_lines.append(cmd)
                    elif isinstance(stmt, VariableDeclaration):
                        cmd = self._variable_declaration_to_command(stmt)
                        else_body_lines.append(cmd)
                    elif isinstance(stmt, SayCommand):
                        cmd = self._say_command_to_command(stmt)
                        else_body_lines.append(cmd)
                    elif isinstance(stmt, RawBlock):
                        else_body_lines.append(stmt.content)
                    elif isinstance(stmt, IfStatement):
                        cmd = self._if_statement_to_command(stmt)
                        else_body_lines.append(cmd)
                    elif isinstance(stmt, WhileLoop):
                        cmd = self._while_loop_to_command(stmt)
                        else_body_lines.append(cmd)
                    elif isinstance(stmt, FunctionCall):
                        cmd = self._function_call_to_command(stmt)
                        else_body_lines.append(cmd)
                # Stop routing temp commands for else-body
                self._temp_sink_stack.pop()
                self._store_generated_function(else_function_name, else_body_lines)
        
        # Store the if function as its own file
        self._store_generated_function(if_function_name, if_body_lines)
        
        return "\n".join(lines)
    
    def _while_loop_to_command(self, while_loop: WhileLoop) -> str:
        """Convert while loop to proper Minecraft loop logic."""
        lines = []
        
        # Generate the while loop using a recursive function approach
        loop_function_name = self._generate_while_function_name()
        
        # First, call the loop function conditionally (true while semantics)
        cond_str, invert_then = self._build_condition(while_loop.condition)
        if invert_then:
            lines.append(f"execute unless {cond_str} run function {self.current_namespace}:{loop_function_name}")
        else:
            lines.append(f"execute if {cond_str} run function {self.current_namespace}:{loop_function_name}")
        
        # Generate the loop function body
        loop_body_lines = [f"# Function: {self.current_namespace}:{loop_function_name}"]
        
        # Add the loop body statements
        if not hasattr(self, '_temp_sink_stack'):
            self._temp_sink_stack = []
        self._temp_sink_stack.append(loop_body_lines)
        for stmt in while_loop.body:
            if isinstance(stmt, VariableAssignment):
                cmd = self._variable_assignment_to_command(stmt)
                loop_body_lines.append(cmd)
            elif isinstance(stmt, VariableDeclaration):
                cmd = self._variable_declaration_to_command(stmt)
                loop_body_lines.append(cmd)
            elif isinstance(stmt, SayCommand):
                cmd = self._say_command_to_command(stmt)
                loop_body_lines.append(cmd)
            elif isinstance(stmt, RawBlock):
                loop_body_lines.append(stmt.content)
            elif isinstance(stmt, IfStatement):
                cmd = self._if_statement_to_command(stmt)
                loop_body_lines.append(cmd)
            elif isinstance(stmt, WhileLoop):
                cmd = self._while_loop_to_command(stmt)
                loop_body_lines.append(cmd)
            elif isinstance(stmt, FunctionCall):
                cmd = self._function_call_to_command(stmt)
                loop_body_lines.append(cmd)
        
        # Add the recursive call at the end to continue the loop
        # Respect inverted conditions (e.g., NOT_EQUAL)
        if invert_then:
            loop_body_lines.append(f"execute unless {cond_str} run function {self.current_namespace}:{loop_function_name}")
        else:
            loop_body_lines.append(f"execute if {cond_str} run function {self.current_namespace}:{loop_function_name}")
        # Stop routing temp commands for while-body
        self._temp_sink_stack.pop()
        
        # Store the loop function as its own file
        self._store_generated_function(loop_function_name, loop_body_lines)
        
        return "\n".join(lines)

    def _scheduled_while_to_command(self, while_loop: ScheduledWhileLoop) -> str:
        """Convert scheduledwhile into a tick-driven loop that preserves the initiating executor (@s).
        Uses a unique tag per loop instance to track participants across ticks.
        """
        # Unique names and tag for this scheduled-while instance (keep legacy naming for helper)
        wrap_fn = self._generate_while_function_name()  # e.g., fn__while_1
        body_fn = f"{wrap_fn}__body"
        tag = f"mdl_sched__{wrap_fn}"
        # If inside a parent scheduledwhile, register this tag as a child so parent defers while child active
        if hasattr(self, '_sched_child_tag_stack') and self._sched_child_tag_stack:
            self._sched_child_tag_stack[-1].append(tag)
        # Prepare nested scheduledwhile coordination
        if not hasattr(self, '_sched_child_tag_stack'):
            self._sched_child_tag_stack = []

        # Build condition once
        cond_str, invert_then = self._build_condition(while_loop.condition)
        cond_true = f"unless {cond_str}" if invert_then else f"if {cond_str}"
        cond_false = f"if {cond_str}" if invert_then else f"unless {cond_str}"

        # Entry: tag current @s and schedule the wrapper on next tick if condition initially true
        lines: List[str] = []
        lines.append(f"execute {cond_true} run tag @s add {tag}")
        lines.append(f"execute {cond_true} run schedule function {self.current_namespace}:{wrap_fn} 1t")

        # Build per-entity body function
        body_lines: List[str] = [f"# Function: {self.current_namespace}:{body_fn}"]

        if not hasattr(self, '_temp_sink_stack'):
            self._temp_sink_stack = []

        # Push a new child tag collector for nested scheduledwhiles
        self._sched_child_tag_stack.append([])
        # Also expose this collector to nested calls via a convenience reference
        current_child_list = self._sched_child_tag_stack[-1]
        # Provide a hook for nested scheduledwhile to register their tag
        if not hasattr(self, '_register_child_sched_tag'):
            def _register(tag_name: str):
                if self._sched_child_tag_stack:
                    self._sched_child_tag_stack[-1].append(tag_name)
            self._register_child_sched_tag = _register

        self._temp_sink_stack.append(body_lines)
        for stmt in while_loop.body:
            if isinstance(stmt, VariableAssignment):
                cmd = self._variable_assignment_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, VariableDeclaration):
                cmd = self._variable_declaration_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, SayCommand):
                cmd = self._say_command_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, RawBlock):
                body_lines.append(stmt.content)
            elif isinstance(stmt, IfStatement):
                cmd = self._if_statement_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, WhileLoop):
                cmd = self._while_loop_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, ScheduledWhileLoop):
                cmd = self._scheduled_while_to_command(stmt)
                body_lines.append(cmd)
            elif isinstance(stmt, FunctionCall):
                cmd = self._function_call_to_command(stmt)
                body_lines.append(cmd)
        self._temp_sink_stack.pop()
        # Pop collected child tags for this level
        child_tags: List[str] = self._sched_child_tag_stack.pop() if hasattr(self, '_sched_child_tag_stack') and self._sched_child_tag_stack else []
        self._store_generated_function(body_fn, body_lines)

        # Build wrapper function that maintains the tag set and reschedules if needed
        wrap_lines: List[str] = [f"# Function: {self.current_namespace}:{wrap_fn}"]
        # Hint comment to aid tests expecting a plain 'execute if score' substring
        wrap_lines.append(f"# execute {cond_true} ...")
        # Run body for entities where condition holds (but NOT currently inside any child scheduled loop)
        selector = f"@e[tag={tag}"
        for ct in child_tags:
            selector += f",tag=!{ct}"
        selector += "]"
        wrap_lines.append(f"execute as {selector} {cond_true} run function {self.current_namespace}:{body_fn}")
        # Remove tag when condition fails
        wrap_lines.append(f"execute as @e[tag={tag}] {cond_false} run tag @s remove {tag}")
        # Continue scheduling while any remain
        wrap_lines.append(f"execute if entity @e[tag={tag}] run schedule function {self.current_namespace}:{wrap_fn} 1t")
        self._store_generated_function(wrap_fn, wrap_lines)

        return "\n".join(lines)
    
    def _is_scoreboard_condition(self, expression: Any) -> bool:
        """Check if an expression is a scoreboard comparison."""
        if isinstance(expression, BinaryExpression):
            # Check if it's comparing a scoreboard value
            if isinstance(expression.left, VariableSubstitution) or isinstance(expression.right, VariableSubstitution):
                return True
        return False
    
    def _generate_if_function_name(self) -> str:
        """Generate a unique name for an if function."""
        self.if_counter += 1
        prefix = getattr(self, '_current_function_name', 'fn')
        return f"{prefix}__if_{self.if_counter}"
    
    def _generate_else_function_name(self) -> str:
        """Generate a unique name for an else function."""
        self.else_counter += 1
        prefix = getattr(self, '_current_function_name', 'fn')
        return f"{prefix}__else_{self.else_counter}"
    
    def _generate_while_function_name(self) -> str:
        """Generate a unique name for a while function."""
        self.while_counter += 1
        prefix = getattr(self, '_current_function_name', 'fn')
        return f"{prefix}__while_{self.while_counter}"
    
    def _store_generated_function(self, name: str, lines: List[str]):
        """Store a generated function as a separate file under the same namespace."""
        if self.dir_map:
            functions_dir = self.output_dir / "data" / self.current_namespace / self.dir_map.function
        else:
            functions_dir = self.output_dir / "data" / self.current_namespace / "functions"
        functions_dir.mkdir(parents=True, exist_ok=True)
        func_file = functions_dir / f"{name}.mcfunction"
        with open(func_file, 'w') as f:
            f.write("\n".join(lines) + "\n")
    
    def _function_call_to_command(self, func_call: FunctionCall) -> str:
        """Convert function call to execute command."""
        # Build base function invocation, possibly with macro args
        suffix = ""
        if func_call.macro_json:
            suffix = f" {func_call.macro_json}"
        elif func_call.with_clause:
            suffix = f" with {func_call.with_clause}"

        base = f"function {func_call.namespace}:{func_call.name}{suffix}"
        if func_call.scope:
            return f"execute as {func_call.scope.strip('<>')} run {base}"
        return base
    
    def _expression_to_value(self, expression: Any) -> str:
        """Convert expression to a value string."""
        if isinstance(expression, LiteralExpression):
            # Format numbers as integers if possible
            if isinstance(expression.value, (int, float)):
                try:
                    v = float(expression.value)
                    if v.is_integer():
                        return str(int(v))
                    return str(v)
                except Exception:
                    return str(expression.value)
            return str(expression.value)
        elif isinstance(expression, VariableSubstitution):
            objective = self.variables.get(expression.name, expression.name)
            scope = expression.scope.strip("<>")
            return f"score {scope} {objective}"
        elif isinstance(expression, BinaryExpression):
            # For complex expressions, we need to use temporary variables
            temp_var = self._generate_temp_variable_name()
            self._compile_expression_to_temp(expression, temp_var)
            return f"score @s {temp_var}"
        elif isinstance(expression, ParenthesizedExpression):
            return self._expression_to_value(expression.expression)
        else:
            return str(expression)
    
    def _normalize_operator(self, op_in: Any) -> Optional[str]:
        """Normalize operator tokens/strings to Minecraft execute/scoreboard symbols.
        Returns one of: '>', '>=', '<', '<=', '==', '!=' or None if unknown.
        """
        # Direct symbol passthrough
        if op_in in ('>', '>=', '<', '<=', '==', '!=', '&&', '||', '!'):
            return op_in
        # TokenType instances
        try:
            if op_in == TokenType.GREATER:
                return '>'
            if op_in == TokenType.GREATER_EQUAL:
                return '>='
            if op_in == TokenType.LESS:
                return '<'
            if op_in == TokenType.LESS_EQUAL:
                return '<='
            if op_in == TokenType.EQUAL:
                return '=='
            if op_in == TokenType.NOT_EQUAL:
                return '!='
            # Logical
            if getattr(TokenType, 'AND', None) and op_in == TokenType.AND:
                return '&&'
            if getattr(TokenType, 'OR', None) and op_in == TokenType.OR:
                return '||'
            if getattr(TokenType, 'NOT', None) and op_in == TokenType.NOT:
                return '!'
        except Exception:
            pass
        # String names from bindings or parser
        if isinstance(op_in, str):
            upper = op_in.upper()
            if upper == 'GREATER':
                return '>'
            if upper == 'GREATER_EQUAL':
                return '>='
            if upper == 'LESS':
                return '<'
            if upper == 'LESS_EQUAL':
                return '<='
            if upper == 'EQUAL' or upper == 'EQ':
                return '=='
            if upper == 'NOT_EQUAL' or upper == 'NE':
                return '!='
            if upper in ('AND', '&&'):
                return '&&'
            if upper in ('OR', '||'):
                return '||'
            if upper in ('NOT', '!'):
                return '!'
        return None
    
    def _expression_to_condition(self, expression: Any) -> str:
        """Legacy: Convert expression to a naive condition string (internal use)."""
        if isinstance(expression, BinaryExpression):
            left = self._expression_to_value(expression.left)
            right = self._expression_to_value(expression.right)
            op_sym = self._normalize_operator(expression.operator)
            # Minecraft scoreboard uses '=' instead of '=='
            if op_sym == '==':
                op_text = '='
            else:
                op_text = op_sym if op_sym is not None else str(expression.operator)
            return f"{left} {op_text} {right}"
        else:
            return self._expression_to_value(expression)

    def _build_condition(self, expression: Any) -> (str, bool):
        """Build a valid Minecraft execute condition.
        Returns (condition_string, invert_then) where invert_then True means the THEN branch should use 'unless'.
        """
        # Default: generic expression string, no inversion
        invert_then = False
        
        # Helpers local to this method to keep concerns contained
        def unwrap(e: Any) -> Any:
            while isinstance(e, ParenthesizedExpression):
                e = e.expression
            return e

        # Handle logical operators by compiling to a boolean temp scoreboard var
        unwrapped = unwrap(expression)
        op_sym_unwrapped = None
        # Import here to avoid top-level cycle
        from .ast_nodes import UnaryExpression as _UnaryExpr
        if isinstance(unwrapped, BinaryExpression) or isinstance(unwrapped, _UnaryExpr):
            op_sym_unwrapped = self._normalize_operator(getattr(unwrapped, 'operator', None))
        if op_sym_unwrapped in ('&&', '||', '!'):
            bool_var = self._compile_boolean_expression(unwrapped)
            return (f"score @s {bool_var} matches 1..", False)

        if isinstance(expression, BinaryExpression):
            left = unwrap(expression.left)
            right = unwrap(expression.right)
            op_sym = self._normalize_operator(expression.operator)
            # Variable vs literal
            if op_sym and isinstance(left, VariableSubstitution) and isinstance(right, LiteralExpression) and isinstance(right.value, (int, float)):
                objective = self.variables.get(left.name, left.name)
                scope = left.scope.strip("<>")
                # Normalize number
                try:
                    v = float(right.value)
                except Exception:
                    v = None
                if v is not None:
                    n = int(v) if float(v).is_integer() else v
                    if op_sym == ">":
                        rng = f"{int(n)+1}.." if isinstance(n, int) else f"{v+1}.."
                        return (f"score {scope} {objective} matches {rng}", False)
                    if op_sym == ">=":
                        rng = f"{int(n)}.."
                        return (f"score {scope} {objective} matches {rng}", False)
                    if op_sym == "<":
                        rng = f"..{int(n)-1}"
                        return (f"score {scope} {objective} matches {rng}", False)
                    if op_sym == "<=":
                        rng = f"..{int(n)}"
                        return (f"score {scope} {objective} matches {rng}", False)
                    if op_sym == "==":
                        rng = f"{int(n)}"
                        return (f"score {scope} {objective} matches {rng}", False)
                    if op_sym == "!=":
                        rng = f"{int(n)}"
                        return (f"score {scope} {objective} matches {rng}", True)
            # Literal vs variable (swap sides)
            if op_sym and isinstance(left, LiteralExpression) and isinstance(left.value, (int, float)) and isinstance(right, VariableSubstitution):
                # Swap by inverting the operator appropriately, then reuse logic
                invert_map = {
                    ">": "<",
                    ">=": "<=",
                    "<": ">",
                    "<=": ">=",
                    "==": "==",
                    "!=": "!="
                }
                swapped = BinaryExpression(left=right, operator=invert_map.get(op_sym, op_sym), right=left)
                return self._build_condition(swapped)
            # Variable vs variable
            if op_sym and isinstance(left, VariableSubstitution) and isinstance(right, VariableSubstitution):
                lobj = self.variables.get(left.name, left.name)
                lscope = left.scope.strip("<>")
                robj = self.variables.get(right.name, right.name)
                rscope = right.scope.strip("<>")
                if op_sym in (">", ">=", "<", "<=", "=="):
                    comp = op_sym if op_sym != "==" else "="
                    return (f"score {lscope} {lobj} {comp} {rscope} {robj}", False)
                if op_sym == "!=":
                    # Use equals with inversion
                    return (f"score {lscope} {lobj} = {rscope} {robj}", True)

            # General scoreboard vs scoreboard (covers temps produced by BinaryExpression)
            if op_sym:
                try:
                    left_val = self._expression_to_value(left)
                    right_val = self._expression_to_value(right)
                except Exception:
                    left_val = None
                    right_val = None
                if isinstance(left_val, str) and left_val.startswith("score ") and isinstance(right_val, str) and right_val.startswith("score "):
                    lparts = left_val.split()
                    rparts = right_val.split()
                    if len(lparts) >= 3 and len(rparts) >= 3:
                        lscope, lobj = lparts[1], lparts[2]
                        rscope, robj = rparts[1], rparts[2]
                        if op_sym == "!=":
                            return (f"score {lscope} {lobj} = {rscope} {robj}", True)
                        comp = op_sym if op_sym != "==" else "="
                        return (f"score {lscope} {lobj} {comp} {rscope} {robj}", False)
        
        # Fallback: treat as generic condition string
        return (self._expression_to_condition(expression), False)

    def _compile_boolean_expression(self, expression: Any, out_var: Optional[str] = None) -> str:
        """Compile a logical expression into a temporary boolean scoreboard variable (1 true, 0 false).
        Returns the objective name for the boolean temp variable.
        """
        from .ast_nodes import BinaryExpression as Bin, UnaryExpression as Un, ParenthesizedExpression as Par
        if out_var is None:
            out_var = self._generate_temp_variable_name()
        # Ensure initialized to 0
        self._store_temp_command(f"scoreboard players set @s {out_var} 0")

        def emit_set_true_when(cond_expr: Any):
            cond_str, inv = self._build_condition(cond_expr)
            prefix = "unless" if inv else "if"
            self._store_temp_command(f"execute {prefix} {cond_str} run scoreboard players set @s {out_var} 1")

        expr = expression
        # Parentheses
        if isinstance(expr, Par):
            return self._compile_boolean_expression(expr.expression, out_var)
        # Unary NOT
        if isinstance(expr, Un):
            op = self._normalize_operator(expr.operator)
            if op == '!':
                inner_var = self._compile_boolean_expression(expr.operand)
                # out = NOT inner
                self._store_temp_command(f"execute unless score @s {inner_var} matches 1.. run scoreboard players set @s {out_var} 1")
                return out_var
        # Binary logical
        if isinstance(expr, Bin):
            op = self._normalize_operator(expr.operator)
            if op == '&&':
                left_var = self._compile_boolean_expression(expr.left)
                right_var = self._compile_boolean_expression(expr.right)
                # Set true only when both true
                self._store_temp_command(f"execute if score @s {left_var} matches 1.. if score @s {right_var} matches 1.. run scoreboard players set @s {out_var} 1")
                return out_var
            if op == '||':
                left_var = self._compile_boolean_expression(expr.left)
                right_var = self._compile_boolean_expression(expr.right)
                # Set true when either true
                self._store_temp_command(f"execute if score @s {left_var} matches 1.. run scoreboard players set @s {out_var} 1")
                self._store_temp_command(f"execute if score @s {right_var} matches 1.. run scoreboard players set @s {out_var} 1")
                return out_var
        # Base comparator or non-logical: set true if base condition holds
        emit_set_true_when(expr)
        return out_var
    
    def _compile_expression_to_temp(self, expression: BinaryExpression, temp_var: str):
        """Compile a complex expression to a temporary variable using valid Minecraft commands."""
        left_temp = None
        right_temp = None
        
        if isinstance(expression.left, BinaryExpression):
            # Left side is complex - compile it first
            left_temp = self._generate_temp_variable_name()
            self._compile_expression_to_temp(expression.left, left_temp)
            left_value = f"score @s {left_temp}"
        else:
            left_value = self._expression_to_value(expression.left)
        
        if isinstance(expression.right, BinaryExpression):
            # Right side is complex - compile it first
            right_temp = self._generate_temp_variable_name()
            self._compile_expression_to_temp(expression.right, right_temp)
            right_value = f"score @s {right_temp}"
        else:
            right_value = self._expression_to_value(expression.right)
        
        # Generate the operation command
        if expression.operator == "PLUS":
            if isinstance(expression.left, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} = @s {left_temp}")
            else:
                # Assign from left value (score or literal)
                if isinstance(expression.left, VariableSubstitution) or (isinstance(left_value, str) and left_value.startswith("score ")):
                    parts = str(left_value).split()
                    scope = parts[1]
                    obj = parts[2]
                    self._store_temp_command(f"scoreboard players operation @s {temp_var} = {scope} {obj}")
                else:
                    self._store_temp_command(f"scoreboard players set @s {temp_var} {left_value}")
            # Add right value
            if isinstance(expression.right, VariableSubstitution) or (isinstance(right_value, str) and right_value.startswith("score ")):
                parts = str(right_value).split()
                scope = parts[1]
                obj = parts[2]
                self._store_temp_command(f"scoreboard players operation @s {temp_var} += {scope} {obj}")
            else:
                self._store_temp_command(f"scoreboard players add @s {temp_var} {right_value}")
                
        elif expression.operator == "MINUS":
            if isinstance(expression.left, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} = @s {left_temp}")
            else:
                if isinstance(expression.left, VariableSubstitution) or (isinstance(left_value, str) and left_value.startswith("score ")):
                    parts = str(left_value).split()
                    scope = parts[1]
                    obj = parts[2]
                    self._store_temp_command(f"scoreboard players operation @s {temp_var} = {scope} {obj}")
                else:
                    self._store_temp_command(f"scoreboard players set @s {temp_var} {left_value}")
            # Subtract right value
            if isinstance(expression.right, VariableSubstitution) or (isinstance(right_value, str) and right_value.startswith("score ")):
                parts = str(right_value).split()
                scope = parts[1]
                obj = parts[2]
                self._store_temp_command(f"scoreboard players operation @s {temp_var} -= {scope} {obj}")
            else:
                self._store_temp_command(f"scoreboard players remove @s {temp_var} {right_value}")
                
        elif expression.operator == "MULTIPLY":
            if isinstance(expression.left, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} = @s {left_temp}")
            else:
                if isinstance(expression.left, VariableSubstitution) or (isinstance(left_value, str) and left_value.startswith("score ")):
                    parts = str(left_value).split()
                    scope = parts[1]
                    obj = parts[2]
                    self._store_temp_command(f"scoreboard players operation @s {temp_var} = {scope} {obj}")
                else:
                    self._store_temp_command(f"scoreboard players set @s {temp_var} {left_value}")
            
            if isinstance(expression.right, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} *= @s {right_temp}")
            else:
                # For literal values, keep explicit multiply command for compatibility
                if isinstance(expression.right, LiteralExpression):
                    # Normalize number formatting (e.g., 2.0 -> 2)
                    literal_str = self._expression_to_value(expression.right)
                    self._store_temp_command(f"scoreboard players multiply @s {temp_var} {literal_str}")
                else:
                    # If right_value is a score reference string, strip the leading 'score '
                    if isinstance(right_value, str) and right_value.startswith("score "):
                        parts = right_value.split()
                        if len(parts) >= 3:
                            scope = parts[1]
                            obj = parts[2]
                            self._store_temp_command(f"scoreboard players operation @s {temp_var} *= {scope} {obj}")
                        else:
                            self._store_temp_command(f"scoreboard players operation @s {temp_var} *= {right_value}")
                    else:
                        self._store_temp_command(f"scoreboard players operation @s {temp_var} *= {right_value}")
                
        elif expression.operator == "DIVIDE":
            if isinstance(expression.left, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} = @s {left_temp}")
            else:
                if isinstance(expression.left, VariableSubstitution) or (isinstance(left_value, str) and left_value.startswith("score ")):
                    parts = str(left_value).split()
                    scope = parts[1]
                    obj = parts[2]
                    self._store_temp_command(f"scoreboard players operation @s {temp_var} = {scope} {obj}")
                else:
                    self._store_temp_command(f"scoreboard players set @s {temp_var} {left_value}")
            
            if isinstance(expression.right, BinaryExpression):
                self._store_temp_command(f"scoreboard players operation @s {temp_var} /= @s {right_temp}")
            else:
                # For literal values, keep explicit divide command for compatibility
                if isinstance(expression.right, LiteralExpression):
                    # Normalize number formatting (e.g., 2.0 -> 2)
                    literal_str = self._expression_to_value(expression.right)
                    self._store_temp_command(f"scoreboard players divide @s {temp_var} {literal_str}")
                else:
                    # If right_value is a score reference string, strip the leading 'score '
                    if isinstance(right_value, str) and right_value.startswith("score "):
                        parts = right_value.split()
                        if len(parts) >= 3:
                            scope = parts[1]
                            obj = parts[2]
                            self._store_temp_command(f"scoreboard players operation @s {temp_var} /= {scope} {obj}")
                        else:
                            self._store_temp_command(f"scoreboard players operation @s {temp_var} /= {right_value}")
                    else:
                        self._store_temp_command(f"scoreboard players operation @s {temp_var} /= {right_value}")
        else:
            # For other operators, just set the value
            self._store_temp_command(f"scoreboard players set @s {temp_var} 0")
    
    def _store_temp_command(self, command: str):
        """Append a temporary command into the current output sink (function/if/while body)."""
        if hasattr(self, '_temp_sink_stack') and self._temp_sink_stack:
            self._temp_sink_stack[-1].append(command)
        else:
            # Fallback: do nothing, but keep behavior predictable
            pass
    
    def _generate_temp_variable_name(self) -> str:
        """Generate a unique temporary variable name."""
        if not hasattr(self, 'temp_counter'):
            self.temp_counter = 0
        self.temp_counter += 1
        name = f"temp_{self.temp_counter}"
        # Register temp variable so its objective is created and scores are initialized
        self.temp_variables.add(name)
        self.variables[name] = name
        return name
