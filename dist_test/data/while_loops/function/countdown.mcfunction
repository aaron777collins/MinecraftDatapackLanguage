execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] countdown matches 1.. run function while_loops:test_countdown_while_1
tellraw @a [{"text":"Blast off!"}]