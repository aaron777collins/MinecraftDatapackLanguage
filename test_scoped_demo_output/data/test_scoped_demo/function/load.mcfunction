execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add global_counter dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 0
scoreboard objectives add player_kills dummy
scoreboard players set @a player_kills 0
scoreboard objectives add red_team_score dummy
scoreboard players set @a[team=red] red_team_score 0
scoreboard objectives add global_counter<global> dummy
scoreboard objectives add player_kills<@s> dummy
scoreboard objectives add red_team_score<@a[team=red]> dummy