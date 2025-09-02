execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Starting scoped function demo . . ."}]
execute as @s run function scoped_calls:increment_player

execute as @e[type=armor_stand,tag=mdl_server,limit=1] run function scoped_calls:increment_global

execute as @a run function scoped_calls:show_scores
