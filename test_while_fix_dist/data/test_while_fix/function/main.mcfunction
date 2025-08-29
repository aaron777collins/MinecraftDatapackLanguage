scoreboard players set @s counter 0
scoreboard players set @s game_timer 0
execute if score @s game_timer matches ..4 run function test_while_fix:test_while_fix_main_while_2
execute if score @s counter matches ..2 run function test_while_fix:test_while_fix_main_while_3