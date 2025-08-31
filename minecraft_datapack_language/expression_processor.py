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
    
    def process_binary_expression(self, expr, target_var: str, selector: str = "@s") -> ProcessedExpression:
        """Process binary expressions like a + b, a * b, etc."""
        print(f"DEBUG: process_binary_expression called: target_var='{target_var}', selector='{selector}', operator='{expr.operator}'")
        commands = []
        temp_vars = []
        
        # Process left operand
        if self.is_complex_expression(expr.left):
            left_temp = self.generate_temp_var("left")
            temp_vars.append(left_temp)
            left_result = self.process_expression(expr.left, left_temp, selector)
            commands.extend(left_result.temp_assignments)
            left_var = left_temp
        else:
            left_var = self.extract_simple_value(expr.left)
        
        # Process right operand
        if self.is_complex_expression(expr.right):
            right_temp = self.generate_temp_var("right")
            temp_vars.append(right_temp)
            right_result = self.process_expression(expr.right, right_temp, selector)
            commands.extend(right_result.temp_assignments)
            right_var = right_temp
        else:
            right_var = self.extract_simple_value(expr.right)
        
        # Generate operation command
        op_command = self.generate_binary_operation(expr.operator, left_var, right_var, target_var, selector)
        commands.append(op_command)
        
        return ProcessedExpression(commands, "", temp_vars)
    
    def extract_simple_value(self, expr) -> str:
        """Extract a simple value from an expression"""
        if hasattr(expr, 'name'):
            # Check if the variable name contains scope information
            if '<' in expr.name and expr.name.endswith('>'):
                return expr.name  # Return the full scoped variable name
            return expr.name
        elif hasattr(expr, 'value'):
            return str(expr.value)
        elif hasattr(expr, 'variable_name'):
            # Handle VariableSubstitutionExpression
            if hasattr(expr, 'scope_selector') and expr.scope_selector:
                # For scoped variables, we need to handle them specially in binary operations
                return f"{expr.variable_name}<{expr.scope_selector}>"
            else:
                return expr.variable_name
        else:
            return str(expr)
    
    def _is_same_variable(self, var1: str, var2: str) -> bool:
        """Check if two variables are the same, handling scoped variables"""
        # Extract base variable names (without scope)
        base1 = var1.split('<')[0] if '<' in var1 else var1
        base2 = var2.split('<')[0] if '<' in var2 else var2
        result = base1 == base2
        print(f"DEBUG: _is_same_variable({var1}, {var2}) -> base1={base1}, base2={base2}, result={result}")
        return result
    
    def parse_scoped_variable(self, var_str: str) -> tuple[str, str]:
        """Parse a scoped variable string into (scope_selector, variable_name) for use in scoreboard commands"""
        if '<' in var_str and var_str.endswith('>'):
            parts = var_str.split('<', 1)
            if len(parts) == 2:
                variable_name = parts[0]
                scope_selector = parts[1][:-1]  # Remove closing >
                # Resolve special selectors
                if scope_selector == "global":
                    scope_selector = "@e[type=armor_stand,tag=mdl_server,limit=1]"
                return scope_selector, variable_name  # Return (selector, variable_name) for correct command order
        return "@s", var_str  # Default to @s if no scope specified
    
    def generate_binary_operation(self, operator: str, left: str, right: str, target: str, selector: str = "@s") -> str:
        """Generate a binary operation command"""
        print(f"DEBUG: generate_binary_operation called: operator='{operator}', left='{left}', right='{right}', target='{target}'")
        # Extract base variable name from target if it's scoped
        base_target = target
        if '<' in target and target.endswith('>'):
            base_target = target.split('<', 1)[0]
        
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
        
        # Check if left and right are scoped variables
        left_selector, left_var = self.parse_scoped_variable(left)
        right_selector, right_var = self.parse_scoped_variable(right)
        
        # The parse_scoped_variable now returns (selector, variable_name) for correct command order
        
        # For literal numbers, we can use direct add/remove/set
        # For variable operands, we need to use scoreboard operations
        
        if operator == '+':
            if is_right_literal:
                # For literal numbers, use direct add
                # Check if this is a self-modification case (left variable equals target variable)
                print(f"DEBUG: + operator with literal: left='{left}', target='{target}'")
                # More aggressive check for same variable
                left_base = left.split('<')[0] if '<' in left else left
                target_base = target.split('<')[0] if '<' in target else target
                if left_base == target_base or self._is_same_variable(left, target):
                    # Avoid self-assignment - just add the literal
                    print(f"DEBUG: Same variable detected for + operator, using direct add")
                    return f"scoreboard players add {selector} {base_target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then add right
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players add {selector} {base_target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players add {selector} {base_target} {right}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
                else:
                    # Both are variables
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
        
        elif operator == '-':
            if is_right_literal:
                # For literal numbers, use direct remove
                # Check if this is a self-modification case (left variable equals target variable)
                print(f"DEBUG: - operator with literal: left='{left}', target='{target}'")
                # More aggressive check for same variable
                left_base = left.split('<')[0] if '<' in left else left
                target_base = target.split('<')[0] if '<' in target else target
                if left_base == target_base or self._is_same_variable(left, target):
                    # Avoid self-assignment - just remove the literal
                    print(f"DEBUG: Same variable detected for - operator, using direct remove")
                    return f"scoreboard players remove {selector} {base_target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then remove right
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players remove {selector} {base_target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players remove {selector} {base_target} {right}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation {selector} {base_target} -= {right_selector} {right_var}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players operation {selector} {base_target} -= {right_selector} {right_var}"
                else:
                    # Both are variables
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} -= {right_selector} {right_var}"
        
        elif operator == '*':
            if is_right_literal:
                # For multiplication with literal, we need to create a temporary objective
                temp_obj = f"temp_{right}"
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} *= @s {temp_obj}"
                elif is_left_literal:
                    # Both are literals, set left then multiply by right
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {base_target} {left}\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} *= @s {temp_obj}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} *= @s {temp_obj}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation {selector} {base_target} *= {right_selector} {right_var}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players operation {selector} {base_target} *= {right_selector} {right_var}"
                else:
                    # Both are variables
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} *= {right_selector} {right_var}"
        
        elif operator == '/':
            if is_right_literal:
                # For division with literal, we need to create a temporary objective
                temp_obj = f"temp_{right}"
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} /= @s {temp_obj}"
                elif is_left_literal:
                    # Both are literals, set left then divide by right
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {base_target} {left}\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} /= @s {temp_obj}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard objectives add {temp_obj} dummy\nscoreboard players set {selector} {temp_obj} {right}\nscoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} /= @s {temp_obj}"
            else:
                # For variable operands, use scoreboard operation
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation {selector} {base_target} /= {right_selector} {right_var}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players operation {selector} {base_target} /= {right_selector} {right_var}"
                else:
                    # Both are variables
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} /= {right_selector} {right_var}"
        
        else:
            # Default to addition for unknown operators
            if is_right_literal:
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players add {selector} {base_target} {right}"
                elif is_left_literal:
                    # Both are literals, set left then add right
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players add {selector} {base_target} {right}"
                else:
                    # Left is variable, right is literal
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players add {selector} {base_target} {right}"
            else:
                if left == target:
                    # Avoid self-assignment
                    return f"scoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
                elif is_left_literal:
                    # Left is literal, right is variable
                    return f"scoreboard players set {selector} {base_target} {left}\nscoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
                else:
                    # Both are variables
                    return f"scoreboard players operation {selector} {base_target} = {left_selector} {left_var}\nscoreboard players operation {selector} {base_target} += {right_selector} {right_var}"
    
    def process_expression(self, expr, target_var: str, selector: str = "@s") -> ProcessedExpression:
        """Main entry point for processing any expression"""
        print(f"DEBUG: process_expression called: target_var='{target_var}', selector='{selector}', expr_type='{type(expr).__name__}'")
        # Extract base variable name from target if it's scoped
        base_target_var = target_var
        if '<' in target_var and target_var.endswith('>'):
            base_target_var = target_var.split('<', 1)[0]
        
        if not hasattr(expr, '__class__'):
            # Simple value
            commands = [f"scoreboard players set {selector} {base_target_var} {expr}"]
            return ProcessedExpression(commands, "", [])
        
        class_name = expr.__class__.__name__
        
        if class_name == 'BinaryExpression':
            return self.process_binary_expression(expr, base_target_var, selector)
        elif class_name == 'LiteralExpression':
            # Handle literal expressions (numbers only)
            try:
                value = int(expr.value)
                commands = [f"scoreboard players set {selector} {base_target_var} {value}"]
            except (ValueError, TypeError):
                # If not a number, set to 0
                commands = [f"scoreboard players set {selector} {base_target_var} 0"]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'VariableExpression':
            # Variable reference - copy from scoreboard
            # Check if the variable name contains scope information
            if hasattr(expr, 'scope_selector') and expr.scope_selector:
                # Use the scope selector from the AST node
                source_selector = expr.scope_selector
                source_var = expr.name
            elif '<' in expr.name and expr.name.endswith('>'):
                # Parse scoped variable
                var_selector, var_name = self.parse_scoped_variable(expr.name)
                source_selector = var_selector
                source_var = var_name
            else:
                # Use default selector
                source_selector = selector
                source_var = expr.name
            commands = [f"scoreboard players operation {selector} {base_target_var} = {source_selector} {source_var}"]
            return ProcessedExpression(commands, "", [])
        elif class_name == 'VariableSubstitutionExpression':
            # Variable substitution ($variable$ or $variable<selector>$) - read from scoreboard
            if hasattr(expr, 'scope_selector') and expr.scope_selector:
                # Use the specified scope selector
                source_selector = expr.scope_selector
            else:
                # Use the default selector
                source_selector = selector
            
            commands = [f"scoreboard players operation {selector} {base_target_var} = {source_selector} {expr.variable_name}"]
            return ProcessedExpression(commands, "", [])
        elif hasattr(expr, 'left') and hasattr(expr, 'right') and hasattr(expr, 'operator'):
            # This is a binary expression that wasn't caught by BinaryExpression class
            return self.process_binary_expression(expr, base_target_var, selector)
        else:
            # Unknown expression type - set to 0
            commands = [f"scoreboard players set {selector} {base_target_var} 0"]
            return ProcessedExpression(commands, "", [])


# Global instance for use in other modules
expression_processor = ExpressionProcessor()
