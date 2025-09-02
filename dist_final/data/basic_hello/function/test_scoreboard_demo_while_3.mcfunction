scoreboard players add @s player_score 10
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_score > = @e[type=armor_stand,tag=mdl_server,limit=1] target_score run function basic_hello:test_scoreboard_demo_while_3_if_1
tellraw @ s {"text":"Current score: "+ player_score}
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_score < @e[type=armor_stand,tag=mdl_server,limit=1] target_score run function basic_hello:test_scoreboard_demo_while_3