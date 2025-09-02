execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Starting while loop demo...;"}]
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] counter 0
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] counter < @e[type=armor_stand,tag=mdl_server,limit=1] maxCount run function while_loops:test_main_while_2
tellraw @a [{"text":"Loop finished!;"}]