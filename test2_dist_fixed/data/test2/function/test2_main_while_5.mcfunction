tellraw @a [{"text":"Player count: "},{"score":{"name":"@s","objective":"player_count"}}]
scoreboard players add @s player_count 1
execute if score @s player_count matches ..4 run function test2:test2_main_while_5