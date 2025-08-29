scoreboard players set @s player_score 50
scoreboard players set @s game_timer 10
scoreboard players set @s player_count 5
execute if score @s player_score matches 50.. run function test_operators:test_operators_main_if_3
function test_operators:test_operators_main_if_end_3
execute if score @s game_timer matches ..10 run function test_operators:test_operators_main_if_4
function test_operators:test_operators_main_if_end_4
execute if score @s player_count matches ..-1 1.. run function test_operators:test_operators_main_if_5
function test_operators:test_operators_main_if_end_5
execute if score @s player_score matches 50 run function test_operators:test_operators_main_if_6
function test_operators:test_operators_main_if_end_6