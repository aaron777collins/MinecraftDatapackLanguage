"""
Expression Processor for MDL to Minecraft Command Translation

This module handles simple expressions for the simplified MDL language.
Only supports number variables, simple arithmetic, and variable substitutions.
"""

import re
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ProcessedExpression:
    """Represents a processed expression with its temporary variables and final command"""
    temp_assignments: List[str]  # Commands to set up temporary variables
    final_command: str           # The final command using the processed expression
    temp_vars: List[str]         # List of temporary variables created


class ExpressionProcessor:
    """Handles simple expressions for the simplified MDL language"""
    
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
        
        # Only complex expressions we support
        complex_types = [
            'BinaryExpression',      # a + b, a * b, etc.
        ]
        
        return class_name in complex_types
    
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
        elif hasattr(expr, 'variable_name'):
            # Handle VariableSubstitutionExpression
            return expr.variable_name
        else:
            return str(expr)
    
    def generate_binary_operation(self, operator: str, left: str, right: str, target: str) -> str:
        """Generate a binary operation command"""
        # Check if left and right are numeric literals
        try:
            left_num = int(left)
            is_left_literal = True
        except (ValueError, TypeError):
            is_left_literal = False
            
        try:
            right_num = int(right)
            is_right_literal = True
        except (ValueError, TypeError):
            is_right_literal = False
        
        # For literal numbers, we can use direct add/remove/set
        # For variable operands, we need to use scoreboard operations
        
        if operator == '+':
            if is_right_literal:
                # For literal numbers, use direct add
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players add @s {target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then add right
                    return f"scoreboard players set @s {target} {left}\nscoreboard players add @s {target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players add @s {target} {right}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation @s {target} += @s {right}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set @s {target} {left}\nscoreboard players operation @s {target} += @s {right}"
                else:
                    # Both are variables
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} += @s {right}"
        
        elif operator == '-':
            if is_right_literal:
                # For literal numbers, use direct remove
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players remove @s {target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then remove right
                    return f"scoreboard players set @s {target} {left}\nscoreboard players remove @s {target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players remove @s {target} {right}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation @s {target} -= @s {right}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set @s {target} {left}\nscoreboard players operation @s {target} -= @s {right}"
                else:
                    # Both are variables
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} -= @s {right}"
        
        elif operator == '*':
            if is_right_literal:
                # For multiplication with literal, we need to create a temporary objective
                temp_obj = f"temp_{right}"
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} *= @s {temp_obj}"
                elif is_left_literal:
                    # Both are literals, set left then multiply by right
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {target} {left}\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} *= @s {temp_obj}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} *= @s {temp_obj}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation @s {target} *= @s {right}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set @s {target} {left}\nscoreboard players operation @s {target} *= @s {right}"
                else:
                    # Both are variables
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} *= @s {right}"
        
        elif operator == '/':
            if is_right_literal:
                # For division with literal, we need to create a temporary objective
                temp_obj = f"temp_{right}"
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} /= @s {temp_obj}"
                elif is_left_literal:
                    # Both are literals, set left then divide by right
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {target} {left}\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} /= @s {temp_obj}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set @s {temp_obj} {right}\nscoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} /= @s {temp_obj}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation @s {target} /= @s {right}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set @s {target} {left}\nscoreboard players operation @s {target} /= @s {right}"
                else:
                    # Both are variables
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} /= @s {right}"
        
        else:
            # Default to addition for unknown operators
            if is_right_literal:
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players add @s {target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then add right
                    return f"scoreboard players set @s {target} {left}\nscoreboard players add @s {target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players add @s {target} {right}"
            else:
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation @s {target} += @s {right}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set @s {target} {left}\nscoreboard players operation @s {target} += @s {right}"
                else:
                    # Both are variables
                    return f"scoreboard players operation @s {target} = @s {left}\nscoreboard players operation @s {target} += @s {right}"
    
    def process_expression(self, expr, target_var: str) -> ProcessedExpression:
        """Main entry point for processing any expression"""
        if not hasattr(expr, '__class__'):
            # Simple value
            commands = [f"scoreboard players set @s {target_var} {expr}"]
            return ProcessedExpression(commands, "", [])
        
        class_name = expr.__class__.__name__
        
        if class_name == 'BinaryExpression':
            return self.process_binary_expression(expr, target_var)
        elif class_name == 'LiteralExpression':
            # Handle literal expressions (numbers only)
            try:
                value = int(expr.value)
                commands = [f"scoreboard players set @s {target_var} {value}"]
            except (ValueError, TypeError):
                # If not a number, set to 0
                commands = [f"scoreboard players set @s {target_var} 0"]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'VariableExpression':
            # Variable reference - copy from scoreboard
            commands = [f"scoreboard players operation @s {target_var} = @s {expr.name}"]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'VariableSubstitutionExpression':
            # Variable substitution ($variable$) - read from scoreboard
            commands = [f"scoreboard players operation @s {target_var} = @s {expr.variable_name}"]
            return ProcessedExpression(commands, "", [])
        elif hasattr(expr, 'left') and hasattr(expr, 'right') and hasattr(expr, 'operator'):
            # This is a binary expression that wasn't caught by BinaryExpression class
            return self.process_binary_expression(expr, target_var)
        else:
            # Unknown expression type - set to 0
            commands = [f"scoreboard players set @s {target_var} 0"]
            return ProcessedExpression(commands, "", [])


# Global instance for use in other modules
expression_processor = ExpressionProcessor()
