execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add globalCounter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] globalCounter 0
scoreboard objectives add playerCounter dummy
scoreboard objectives add teamCounter dummy
scoreboard players set @a[team=red] teamCounter 0