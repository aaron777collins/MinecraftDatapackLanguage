execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players set @s player_score 50
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_score < @e[type=armor_stand,tag=mdl_server,limit=1] target_score run function registry:test_scoreboard_demo_while_3
tellraw @ s {"text":"Final score: "+ player_score}