scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] game_timer 1
tellraw @a [{"text":"Timer: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"game_timer"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] game_timer matches ..9 run function other:other_main_while_0