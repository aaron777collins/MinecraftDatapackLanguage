execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add player_count dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_count 0
scoreboard objectives add game_timer dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] game_timer 0
scoreboard objectives add player_score dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_score 0
scoreboard objectives add result dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] result 0