tellraw @a [{"text":"Player count: "},{"score":{"name":"@a","objective":"player_count"}}]
scoreboard players add @a player_count 1
execute if score @a player_count matches ..4 run function test2:test2_main_while_5