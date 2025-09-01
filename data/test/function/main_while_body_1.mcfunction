scoreboard players add @s counter 1
tellraw @a [{"text":"Counter: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"counter"}},{"text":"counter"}]