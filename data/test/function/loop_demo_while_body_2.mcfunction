execute score $i$ % 2 @s matches 0 run function test:loop_demo_while_body_2_if_0
execute unless score $i$ % 2 @s matches 0 run function test:loop_demo_while_body_2_else_0
# Complex assignment: i = BinaryExpression(left=VariableExpression(name='i'), operator='PLUS', right=LiteralExpression(value='1', type='number'))
execute score $i$ % 5 @s matches 0 run function test:loop_demo_while_body_2_if_2