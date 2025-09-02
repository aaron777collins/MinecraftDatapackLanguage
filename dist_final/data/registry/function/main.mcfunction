execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Welcome to the comprehensive example!"}]
scoreboard players set @s playerHealth 20
scoreboard players set @s playerScore 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] globalTimer 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] gamePhase 1
tellraw @a [{"text":"Game initialized!"}]
execute as @a run function comprehensive:start_game
