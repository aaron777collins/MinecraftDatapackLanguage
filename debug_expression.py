#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js, BinaryExpression, LiteralExpression
from minecraft_datapack_language.expression_processor import expression_processor

if __name__ == "__main__":
    # Test the expression processor directly
    expr = BinaryExpression(
        left=LiteralExpression('5', 'number'),
        operator='+',
        right=LiteralExpression('3', 'number')
    )
    
    print("=== EXPRESSION ===")
    print(f"Expression: {expr}")
    print(f"Left: {expr.left}")
    print(f"Operator: {expr.operator}")
    print(f"Right: {expr.right}")
    print()
    
    result = expression_processor.process_expression(expr, 'result')
    print("=== PROCESSED ===")
    print(f"Temp assignments: {result.temp_assignments}")
    print(f"Final command: {result.final_command}")
    print(f"Temp vars: {result.temp_vars}")
