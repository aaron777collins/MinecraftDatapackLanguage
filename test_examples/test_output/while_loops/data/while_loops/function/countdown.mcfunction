scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] countdown 10
execute if score @s countdown matches 1.. run function while_loops:while_loops_countdown_while_1
tellraw @a [{"text":"Blast off !"}]