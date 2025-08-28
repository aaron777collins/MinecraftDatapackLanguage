"""
Expression Processor for MDL to Minecraft Command Translation

This module handles the systematic breakdown of complex expressions into
simple operations that can be translated to Minecraft commands.
"""

import re
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ProcessedExpression:
    """Represents a processed expression with its temporary variables and final command"""
    temp_assignments: List[str]  # Commands to set up temporary variables
    final_command: str           # The final command using the processed expression
    temp_vars: List[str]         # List of temporary variables created


class ExpressionProcessor:
    """Handles the systematic breakdown of complex expressions"""
    
    def __init__(self):
        self.temp_counter = 0
        self.temp_vars_used = set()
    
    def generate_temp_var(self, prefix: str = "temp") -> str:
        """Generate a unique temporary variable name"""
        while True:
            temp_var = f"{prefix}_{self.temp_counter}"
            self.temp_counter += 1
            if temp_var not in self.temp_vars_used:
                self.temp_vars_used.add(temp_var)
                return temp_var
    
    def is_complex_expression(self, expr) -> bool:
        """Determine if an expression is complex and needs breakdown"""
        if not hasattr(expr, '__class__'):
            return False
        
        class_name = expr.__class__.__name__
        
        # Complex expressions that need breakdown
        complex_types = [
            'BinaryExpression',      # a + b, a * b, etc.
            'ListAccessExpression',  # list[index]
            'ListLengthExpression',  # list.length
            'StringConcatenation',   # "a" + "b"
        ]
        
        # Also check for literal expressions that might be list length
        if class_name == 'LiteralExpression' and hasattr(expr, 'value'):
            if isinstance(expr.value, str) and '.length' in expr.value:
                return True
        
        return class_name in complex_types
    
    def process_list_access(self, list_name: str, index_expr, target_var: str) -> ProcessedExpression:
        """Process list access expressions like list[index]"""
        commands = []
        temp_vars = []
        
        # Handle the index expression
        if hasattr(index_expr, 'name'):
            # Variable index - use directly
            index_var = index_expr.name
            commands.extend([
                f"# Access element at variable index {index_var} from {list_name}",
                f"execute store result storage mdl:temp index int 1 run scoreboard players get @s {index_var}",
                f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[storage mdl:temp index]",
                f"data modify storage mdl:variables {target_var} set from storage mdl:temp element"
            ])
        elif hasattr(index_expr, 'value'):
            # Literal index - use directly
            index = index_expr.value
            commands.extend([
                f"# Access element at index {index} from {list_name}",
                f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[{index}]",
                f"data modify storage mdl:variables {target_var} set from storage mdl:temp element"
            ])
        else:
            # Complex index expression - break it down
            temp_index_var = self.generate_temp_var("index")
            temp_vars.append(temp_index_var)
            index_commands = self.process_expression(index_expr, temp_index_var)
            commands.extend(index_commands.temp_assignments)
            commands.extend([
                f"# Access element at complex index from {list_name}",
                f"execute store result storage mdl:temp index int 1 run scoreboard players get @s {temp_index_var}",
                f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[storage mdl:temp index]",
                f"data modify storage mdl:variables {target_var} set from storage mdl:temp element"
            ])
            commands.extend(index_commands.final_command)
        
        return ProcessedExpression(commands, "", temp_vars)
    
    def process_list_length(self, list_name: str, target_var: str) -> ProcessedExpression:
        """Process list length expressions like list.length"""
        commands = [
            f"# Get length of {list_name}",
            f"execute store result score @s {target_var} run data get storage mdl:variables {list_name}"
        ]
        return ProcessedExpression(commands, "", [])
    
    def process_binary_expression(self, expr, target_var: str) -> ProcessedExpression:
        """Process binary expressions like a + b, a * b, etc."""
        commands = []
        temp_vars = []
        
        # Process left operand
        if self.is_complex_expression(expr.left):
            left_temp = self.generate_temp_var("left")
            temp_vars.append(left_temp)
            left_result = self.process_expression(expr.left, left_temp)
            commands.extend(left_result.temp_assignments)
            left_var = left_temp
        else:
            left_var = self.extract_simple_value(expr.left)
        
        # Process right operand
        if self.is_complex_expression(expr.right):
            right_temp = self.generate_temp_var("right")
            temp_vars.append(right_temp)
            right_result = self.process_expression(expr.right, right_temp)
            commands.extend(right_result.temp_assignments)
            right_var = right_temp
        else:
            right_var = self.extract_simple_value(expr.right)
        
        # Generate operation command
        op_command = self.generate_binary_operation(expr.operator, left_var, right_var, target_var)
        commands.append(op_command)
        
        return ProcessedExpression(commands, "", temp_vars)
    
    def extract_simple_value(self, expr) -> str:
        """Extract a simple value from an expression"""
        if hasattr(expr, 'name'):
            return expr.name
        elif hasattr(expr, 'value'):
            return str(expr.value)
        else:
            return str(expr)
    
    def generate_binary_operation(self, operator: str, left: str, right: str, target: str) -> str:
        """Generate a binary operation command"""
        if operator == '+':
            return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players add @s {target} {right}"
        elif operator == '-':
            return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players remove @s {target} {right}"
        elif operator == '*':
            return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} *= @s {right}"
        elif operator == '/':
            return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} /= @s {right}"
        else:
            # Default to addition for unknown operators
            return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players add @s {target} {right}"
    
    def process_string_concatenation(self, parts: List, target_var: str) -> ProcessedExpression:
        """Process string concatenation like "a" + b + "c" """
        commands = [f"data modify storage mdl:variables {target_var} set value \"\""]
        temp_vars = []
        
        for part in parts:
            if self.is_literal_string(part):
                # Literal string
                value = part.strip('"').strip("'")
                commands.append(f"data modify storage mdl:variables {target_var} append value \"{value}\"")
            elif hasattr(part, 'name'):
                # Variable reference
                commands.extend([
                    f"execute store result storage mdl:temp concat string 1 run data get storage mdl:variables {part.name}",
                    f"data modify storage mdl:variables {target_var} append value storage mdl:temp concat"
                ])
            elif self.is_complex_expression(part):
                # Complex expression - break it down
                temp_var = self.generate_temp_var("concat")
                temp_vars.append(temp_var)
                part_result = self.process_expression(part, temp_var)
                commands.extend(part_result.temp_assignments)
                commands.extend([
                    f"execute store result storage mdl:temp concat string 1 run data get storage mdl:variables {temp_var}",
                    f"data modify storage mdl:variables {target_var} append value storage mdl:temp concat"
                ])
            else:
                # Simple value
                value = str(part).strip('"').strip("'")
                commands.append(f"data modify storage mdl:variables {target_var} append value \"{value}\"")
        
        return ProcessedExpression(commands, "", temp_vars)
    
    def is_literal_string(self, expr) -> bool:
        """Check if expression is a literal string"""
        if isinstance(expr, str):
            return expr.startswith('"') and expr.endswith('"') or expr.startswith("'") and expr.endswith("'")
        elif hasattr(expr, 'type') and expr.type == 'string':
            return True
        return False
    
    def process_expression(self, expr, target_var: str) -> ProcessedExpression:
        """Main entry point for processing any expression"""
        if not hasattr(expr, '__class__'):
            # Simple value
            commands = [f"scoreboard players set @s {target_var} {expr}"]
            return ProcessedExpression(commands, "", [])
        
        class_name = expr.__class__.__name__
        print(f"DEBUG: Processing expression {class_name}: {expr}")
        
        if class_name == 'ListAccessExpression':
            print(f"DEBUG: Processing ListAccessExpression: {expr.list_name}[{expr.index}]")
            return self.process_list_access(expr.list_name, expr.index, target_var)
        elif class_name == 'ListLengthExpression':
            return self.process_list_length(expr.list_name, target_var)
        elif class_name == 'BinaryExpression':
            print(f"DEBUG: Processing BinaryExpression: {expr.left} {expr.operator} {expr.right}")
            return self.process_binary_expression(expr, target_var)
        elif class_name == 'LiteralExpression':
            if hasattr(expr, 'type'):
                if expr.type == 'string':
                    value = expr.value.strip('"').strip("'")
                    # Check if this is a list length expression
                    if '.length' in value:
                        list_name = value.split('.')[0]
                        commands = [
                            f"# Get length of {list_name}",
                            f"execute store result score @s {target_var} run data get storage mdl:variables {list_name}"
                        ]
                    else:
                        commands = [f"data modify storage mdl:variables {target_var} set value \"{value}\""]
                elif expr.type == 'number':
                    commands = [f"scoreboard players set @s {target_var} {expr.value}"]
                else:
                    commands = [f"# Unknown literal type: {expr.type}"]
            else:
                # Try to determine type
                try:
                    value = int(expr.value)
                    commands = [f"scoreboard players set @s {target_var} {value}"]
                except (ValueError, TypeError):
                    value = str(expr.value).strip('"').strip("'")
                    # Check if this is a list length expression
                    if '.length' in value:
                        list_name = value.split('.')[0]
                        commands = [
                            f"# Get length of {list_name}",
                            f"execute store result score @s {target_var} run data get storage mdl:variables {list_name}"
                        ]
                    else:
                        commands = [f"data modify storage mdl:variables {target_var} set value \"{value}\""]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'Identifier':
            # Variable reference
            commands = [f"scoreboard players operation @s {target_var} = @s {expr.name}"]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'ListExpression':
            # Handle list assignments
            commands = [f"data modify storage mdl:variables {target_var} set value []"]
            if hasattr(expr, 'elements'):
                for item in expr.elements:
                    if hasattr(item, 'value'):
                        # Handle string literals in lists
                        item_value = item.value.strip('"').strip("'")
                        commands.append(f"data modify storage mdl:variables {target_var} append value \"{item_value}\"")
                    else:
                        # Handle other types - convert to string for now
                        commands.append(f"data modify storage mdl:variables {target_var} append value \"unknown\"")
            return ProcessedExpression(commands, "", [])
        elif class_name == 'FunctionCall':
            # Handle built-in function calls
            if expr.function_name == 'length':
                if len(expr.arguments) == 1:
                    # length(list) - get the length of a list
                    list_arg = expr.arguments[0]
                    if hasattr(list_arg, 'name'):
                        # Variable reference
                        list_name = list_arg.name
                        commands = [
                            f"# Get length of {list_name}",
                            f"execute store result score @s {target_var} run data get storage mdl:variables {list_name}"
                        ]
                    else:
                        # Complex expression - evaluate first
                        temp_list_var = self.generate_temp_var("list")
                        list_result = self.process_expression(list_arg, temp_list_var)
                        commands.extend(list_result.temp_assignments)
                        commands.extend([
                            f"# Get length of complex list expression",
                            f"execute store result score @s {target_var} run data get storage mdl:variables {temp_list_var}"
                        ])
                    return ProcessedExpression(commands, "", [])
                else:
                    # Wrong number of arguments
                    commands = [f"# Error: length() expects exactly 1 argument"]
                    return ProcessedExpression(commands, "", [])
            else:
                # Unknown function - convert to string
                commands = [f"data modify storage mdl:variables {target_var} set value \"{str(expr)}\""]
                return ProcessedExpression(commands, "", [])
        else:
            # Unknown expression type - convert to string
            commands = [f"data modify storage mdl:variables {target_var} set value \"{str(expr)}\""]
            return ProcessedExpression(commands, "", [])
    
    def process_condition(self, condition: str) -> ProcessedExpression:
        """Process conditions that may contain complex expressions"""
        # This is a simplified version - in practice, we'd need to parse the condition
        # and identify complex expressions within it
        commands = [f"# Process condition: {condition}"]
        return ProcessedExpression(commands, condition, [])


# Global instance for use in other modules
expression_processor = ExpressionProcessor()
