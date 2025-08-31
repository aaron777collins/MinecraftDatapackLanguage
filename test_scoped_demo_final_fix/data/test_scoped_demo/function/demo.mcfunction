execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players operation @e[type=armor_stand,tag=mdl_server,limit=1] global_counter = global global_counter
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] global_counter 1
scoreboard players operation @a player_kills = @s player_kills
scoreboard players add @a player_kills 1
scoreboard players operation @a[team=red] red_team_score = @a[team=red] red_team_score
scoreboard players add @a[team=red] red_team_score 2
tellraw @a [{"text": "Global Counter: ", "color": "gold"}, {"score": {"name": "global", "objective": "global_counter"}, "color": "gold"}]
tellraw @s [{"text": "Your Kills: ", "color": "blue"}, {"score": {"name": "@s", "objective": "player_kills"}, "color": "blue"}]
tellraw @a [team = red] [{"text": "Red Team Score: ", "color": "red"}, {"score": {"name": "@a[team=red]", "objective": "red_team_score"}, "color": "red"}]
tellraw @a [{"score": {"name": "@s", "objective": "player_kills"}, "color": "yellow"}, {"text": " just got a kill!", "color": "yellow"}]
tellraw @s [{"text": "Server has been running for ", "color": "aqua"}, {"score": {"name": "global", "objective": "global_counter"}, "color": "aqua"}, {"text": " ticks", "color": "aqua"}]