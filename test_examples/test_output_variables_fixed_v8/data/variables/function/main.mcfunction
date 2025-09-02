execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] globalCounter 1
scoreboard players add @s playerCounter 1
scoreboard players add @a[team=red] teamCounter 1
tellraw @a [{"text":"Global counter: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"globalCounter"}},{"text":";"}]
tellraw @a [{"text":"Player counter: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"playerCounter"}},{"text":";"}]
tellraw @a [{"text":"Team counter: "},{"score":{"name":"@a[team=red]","objective":"teamCounter"}},{"text":";"}]