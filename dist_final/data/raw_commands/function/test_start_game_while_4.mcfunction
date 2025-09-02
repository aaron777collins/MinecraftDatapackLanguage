scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] globalTimer 1
tellraw @a [{"text":"Timer: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"globalTimer"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] globalTimer matches ..4 run function raw_commands:test_start_game_while_4