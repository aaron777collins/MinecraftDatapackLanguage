execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add global_counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 0
scoreboard objectives add global_timer dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 0
scoreboard objectives add player_score dummy
scoreboard players set @s player_score 0
scoreboard objectives add player_level dummy
scoreboard players set @s player_level 0
scoreboard objectives add red_team_score dummy
scoreboard players set @a[team=red] red_team_score 0
scoreboard objectives add blue_team_score dummy
scoreboard players set @a[team=blue] blue_team_score 0
scoreboard objectives add all_players_counter dummy
scoreboard players set @a all_players_counter 0