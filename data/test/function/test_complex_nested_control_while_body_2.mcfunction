# Complex assignment: counter = BinaryExpression(left=VariableExpression(name='counter'), operator='PLUS', right=LiteralExpression(value='1', type='number'))
execute score $counter$ % 2 @s matches 0 run function test:test_complex_nested_control_while_body_2_if_1
execute unless score $counter$ % 2 @s matches 0 run function test:test_complex_nested_control_while_body_2_else_1
execute score $playerScore$ @s matches 101.. run function test:test_complex_nested_control_while_body_2_if_2