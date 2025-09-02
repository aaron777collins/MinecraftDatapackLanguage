tellraw @a [{"text":"Countdown: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"countdown"}},{"text":";"}]
scoreboard players remove @s countdown 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] countdown matches 1.. run function while_loops:test_countdown_while_1