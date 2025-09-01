# Complex assignment: player_score = BinaryExpression(left=VariableExpression(name='player_score'), operator='PLUS', right=LiteralExpression(value='10', type='number'))
execute score $player_score$ @s > = $target_score$ @s run function test:scoreboard_demo_while_body_3_if_1
tellraw @ s {"text":"Current score: "+ player_score}