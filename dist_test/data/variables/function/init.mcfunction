execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
globalCounter < global > = 10
playerScore < @ s > = 100
tellraw @a [{"text":"Global: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"globalCounter"}},{"text":", Player: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"playerScore"}}]