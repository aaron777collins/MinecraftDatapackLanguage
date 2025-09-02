execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players add @s local_counter 5
scoreboard players add @s global_counter 1
# Complex operation: player_score = VariableExpression(name='player_score') MULTIPLY LiteralExpression(value='2', type='number')
tellraw @ s {"text":"Variable demo complete"}
tellraw @ s {"text":"Result: "+ result}
tellraw @ s {"text":"Modulo: "+ modulo_result}