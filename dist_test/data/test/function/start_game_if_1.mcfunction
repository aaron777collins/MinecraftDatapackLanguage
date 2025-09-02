tellraw @a [{"text":"Warning: Low health!"}]
scoreboard players add @s playerHealth 5
tellraw @a [{"text":"Health restored to: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"playerHealth"}}]