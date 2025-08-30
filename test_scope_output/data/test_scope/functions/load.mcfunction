execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add global_counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 0
scoreboard objectives add global_timer dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 0
scoreboard objectives add player_score dummy
scoreboard players set @s player_score 0
scoreboard objectives add player_level dummy
scoreboard players set @s player_level 0
scoreboard objectives add team_score dummy
scoreboard players set @a[team=red] team_score 0
scoreboard objectives add team_bonus dummy
scoreboard players set @a[team=blue] team_bonus 0
scoreboard objectives add world_timer dummy
scoreboard players set @e[type=armor_stand,tag=world_timer,limit=1] world_timer 0