scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] counter 1
tellraw @a [{"text":"Loop iteration: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"counter"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] counter < @e[type=armor_stand,tag=mdl_server,limit=1] maxCount run function basic_hello:test_main_while_2