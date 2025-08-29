scoreboard players add @s game_timer 1
tellraw @a [{"text":"Timer: "},{"score":{"name":"@s","objective":"game_timer"}}]
execute if score @s game_timer matches ..4 run function test_while_fix:test_while_fix_main_while_2