scoreboard players set @s player_count 0
scoreboard players set @s game_timer 0
scoreboard players set @s player_score 100
execute if score @a player_score matches 51.. run function test2:test2_main_if_3
execute unless score @a player_score matches 51.. run function test2:test2_main_else_3
function test2:test2_main_if_end_3
execute if score @a game_timer matches ..9 run function test2:test2_main_while_4
execute if score @a player_count matches ..4 run function test2:test2_main_while_5
execute if score @a player_count matches 1.. run function test2:test2_main_if_6
function test2:test2_main_if_end_6