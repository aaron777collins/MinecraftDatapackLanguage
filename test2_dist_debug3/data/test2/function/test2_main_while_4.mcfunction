scoreboard players add @s game_timer 1
tellraw @a [{"text":"Timer: "},{"score":{"name":"@a","objective":"game_timer"}}]
execute if score @a game_timer matches ..9 run function test2:test2_main_while_4