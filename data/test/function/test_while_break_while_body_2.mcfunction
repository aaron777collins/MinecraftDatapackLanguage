# Complex assignment: counter = BinaryExpression(left=VariableExpression(name='counter'), operator='PLUS', right=LiteralExpression(value='1', type='number'))
execute score $counter$ @s matches 10 run function test:test_while_break_while_body_2_if_1
execute score $counter$ @s matches 15 run function test:test_while_break_while_body_2_if_2
say "Counter: ${counter}"