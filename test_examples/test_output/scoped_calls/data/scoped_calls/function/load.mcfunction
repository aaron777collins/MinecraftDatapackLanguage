execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add playerScore dummy
scoreboard players set @s playerScore 0
scoreboard objectives add globalTimer dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] globalTimer 0