"""
MDL Compiler - Converts MDL AST into complete Minecraft datapack
Simplified version that focuses on generating actual statements for testing
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from .ast_nodes import (
    Program, PackDeclaration, NamespaceDeclaration, TagDeclaration,
    VariableDeclaration, VariableAssignment, VariableSubstitution, FunctionDeclaration,
    FunctionCall, IfStatement, WhileLoop, HookDeclaration, RawBlock,
    SayCommand, BinaryExpression, LiteralExpression, ParenthesizedExpression
)
from .dir_map import get_dir_map, DirMap
from .mdl_errors import MDLCompilerError


class MDLCompiler:
    """
    Simplified compiler for the MDL language that generates actual statements.
    """
    
    def __init__(self, output_dir: str = "dist"):
        self.output_dir = Path(output_dir)
        self.dir_map: Optional[DirMap] = None
        self.current_namespace = "mdl"
        self.variables: Dict[str, str] = {}  # name -> objective mapping
        
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
            
            # Create namespace directory
            namespace_dir = data_dir / self.current_namespace
            namespace_dir.mkdir(parents=True, exist_ok=True)
            
            # Compile all components
            self._compile_variables(ast.variables, namespace_dir)
            self._compile_functions(ast.functions, namespace_dir)
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
            print(f"Variable: {var.name} -> scoreboard objective '{objective_name}'")
    
    def _compile_functions(self, functions: List[FunctionDeclaration], namespace_dir: Path):
        """Compile function declarations into .mcfunction files."""
        if self.dir_map:
            functions_dir = namespace_dir / self.dir_map.function
        else:
            functions_dir = namespace_dir / "functions"
        functions_dir.mkdir(parents=True, exist_ok=True)
        
        for func in functions:
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
        
        # Generate commands from function body
        for statement in func.body:
            cmd = self._statement_to_command(statement)
            if cmd:
                lines.append(cmd)
        
        return "\n".join(lines)
    
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
            else:
                continue
            
            tag_dir.mkdir(parents=True, exist_ok=True)
            tag_file = tag_dir / f"{tag.name}.json"
            
            if source_path:
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
                tag_data = {"values": [f"{self.current_namespace}:{tag.name}"]}
                with open(tag_file, 'w') as f:
                    json.dump(tag_data, f, indent=2)
                print(f"Tag {tag.tag_type}: {tag.name} -> {tag_file} (placeholder)")
    
    def _create_hook_functions(self, hooks: List[HookDeclaration], namespace_dir: Path):
        """Create load.mcfunction and tick.mcfunction for hooks."""
        if self.dir_map:
            functions_dir = namespace_dir / self.dir_map.function
        else:
            functions_dir = namespace_dir / "functions"
        
        # Create load function
        load_content = self._generate_load_function(hooks)
        load_file = functions_dir / "load.mcfunction"
        with open(load_file, 'w') as f:
            f.write(load_content)
        
        # Create tick function if needed
        tick_hooks = [h for h in hooks if h.hook_type == "on_tick"]
        if tick_hooks:
            tick_content = self._generate_tick_function(tick_hooks)
            tick_file = functions_dir / "tick.mcfunction"
            with open(tick_file, 'w') as f:
                f.write(tick_content)
    
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
        elif isinstance(statement, SayCommand):
            return self._say_command_to_command(statement)
        elif isinstance(statement, RawBlock):
            return statement.content
        elif isinstance(statement, IfStatement):
            return self._if_statement_to_command(statement)
        elif isinstance(statement, WhileLoop):
            return self._while_loop_to_command(statement)
        elif isinstance(statement, FunctionCall):
            return self._function_call_to_command(statement)
        else:
            return None
    
    def _variable_assignment_to_command(self, assignment: VariableAssignment) -> str:
        """Convert variable assignment to scoreboard command."""
        objective = self.variables.get(assignment.name, assignment.name)
        value = self._expression_to_value(assignment.value)
        scope = assignment.scope.strip("<>")
        return f"scoreboard players set {scope} {objective} {value}"
    
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
        """Convert if statement to comment and include actual statements."""
        condition = self._expression_to_condition(if_stmt.condition)
        lines = [f"# if {condition}"]
        
        # Include the actual statements from the if body for visibility
        for stmt in if_stmt.then_body:
            if isinstance(stmt, VariableAssignment):
                # Include variable assignments directly
                cmd = self._variable_assignment_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, SayCommand):
                # Include say commands directly
                cmd = self._say_command_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, RawBlock):
                # Include raw blocks directly
                lines.append(stmt.content)
            elif isinstance(stmt, IfStatement):
                # Recursively handle nested if statements
                cmd = self._if_statement_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, WhileLoop):
                # Handle while loops
                cmd = self._while_loop_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, FunctionCall):
                # Handle function calls
                cmd = self._function_call_to_command(stmt)
                lines.append(cmd)
        
        # Handle else body if it exists
        if if_stmt.else_body:
            lines.append("")
            lines.append("# else:")
            for stmt in if_stmt.else_body:
                if isinstance(stmt, VariableAssignment):
                    cmd = self._variable_assignment_to_command(stmt)
                    lines.append(cmd)
                elif isinstance(stmt, SayCommand):
                    cmd = self._say_command_to_command(stmt)
                    lines.append(cmd)
                elif isinstance(stmt, RawBlock):
                    lines.append(stmt.content)
                elif isinstance(stmt, IfStatement):
                    cmd = self._if_statement_to_command(stmt)
                    lines.append(cmd)
                elif isinstance(stmt, WhileLoop):
                    cmd = self._while_loop_to_command(stmt)
                    lines.append(cmd)
                elif isinstance(stmt, FunctionCall):
                    cmd = self._function_call_to_command(stmt)
                    lines.append(cmd)
        
        return "\n".join(lines)
    
    def _while_loop_to_command(self, while_loop: WhileLoop) -> str:
        """Convert while loop to comment and include actual statements."""
        condition = self._expression_to_condition(while_loop.condition)
        lines = [f"# while {condition}"]
        
        # Include the actual statements from the while body for visibility
        for stmt in while_loop.body:
            if isinstance(stmt, VariableAssignment):
                # Include variable assignments directly
                cmd = self._variable_assignment_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, SayCommand):
                # Include say commands directly
                cmd = self._say_command_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, RawBlock):
                # Include raw blocks directly
                lines.append(stmt.content)
            elif isinstance(stmt, IfStatement):
                # Recursively handle nested if statements
                cmd = self._if_statement_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, WhileLoop):
                # Handle nested while loops
                cmd = self._while_loop_to_command(stmt)
                lines.append(cmd)
            elif isinstance(stmt, FunctionCall):
                # Handle function calls
                cmd = self._function_call_to_command(stmt)
                lines.append(cmd)
        
        return "\n".join(lines)
    
    def _function_call_to_command(self, func_call: FunctionCall) -> str:
        """Convert function call to execute command."""
        if func_call.scope:
            return f"execute as {func_call.scope.strip('<>')} run function {func_call.namespace}:{func_call.name}"
        else:
            return f"function {func_call.namespace}:{func_call.name}"
    
    def _expression_to_value(self, expression: Any) -> str:
        """Convert expression to a value string."""
        if isinstance(expression, LiteralExpression):
            return str(expression.value)
        elif isinstance(expression, VariableSubstitution):
            objective = self.variables.get(expression.name, expression.name)
            scope = expression.scope.strip("<>")
            return f"score {scope} {objective}"
        elif isinstance(expression, BinaryExpression):
            left = self._expression_to_value(expression.left)
            right = self._expression_to_value(expression.right)
            return f"{left} {expression.operator} {right}"
        elif isinstance(expression, ParenthesizedExpression):
            return f"({self._expression_to_value(expression.expression)})"
        else:
            return str(expression)
    
    def _expression_to_condition(self, expression: Any) -> str:
        """Convert expression to a condition string."""
        if isinstance(expression, BinaryExpression):
            left = self._expression_to_value(expression.left)
            right = self._expression_to_value(expression.right)
            return f"{left} {expression.operator} {right}"
        else:
            return self._expression_to_value(expression)
