scoreboard players add @s game_timer 1
tellraw @a [{"text":"Timer: "},{"score":{"name":"@s","objective":"game_timer"}}]
execute if score @s game_timer matches ..9 run function test2:test2_main_while_4