tellraw @a [{"text":"Countdown: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"countdown"}}]
scoreboard players remove @s countdown 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] countdown matches 1.. run function example:test_countdown_while_1