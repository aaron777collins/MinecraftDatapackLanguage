execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
globalCounter < global > = globalCounter < global > + 1
playerScore < @ s > = playerScore < @ s > + 10
tellraw @a [{"text":"Updated - Global: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"globalCounter"}},{"text":", Player: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"playerScore"}}]