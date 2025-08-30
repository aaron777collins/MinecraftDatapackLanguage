scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] game_timer_2 1
tellraw @a [{"text":"Timer 2: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"game_timer_2"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] game_timer_2 matches ..9 run function other:other_main_while_1