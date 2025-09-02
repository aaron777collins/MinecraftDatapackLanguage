execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players add @s global_timer 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] global_timer % 400 matches 0 run function basic_hello:tick_if_1