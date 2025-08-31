tellraw @a [{"text": "Countdown: "}, {"score": {"name": "@s", "objective": "countdown"}}]
scoreboard players remove @e[type=armor_stand,tag=mdl_server,limit=1] countdown 1
execute if score @s countdown matches 1.. run function while_loops:while_loops_countdown_while_1