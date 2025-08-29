execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_count 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] game_timer 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_score 100
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] game_timer matches ..9 run function test:test_main_while_3