tellraw @a [{"text":"Player count: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"player_count"}}]
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] player_count 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_count matches ..4 run function test2:test2_main_while_5