execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 1
scoreboard players add @s player_score 10
scoreboard players add @a[team=red] team_score 5
scoreboard players add @e[type=armor_stand,tag=world_timer,limit=1] world_timer 1