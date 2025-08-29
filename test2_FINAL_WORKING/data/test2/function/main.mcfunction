execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_count 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] game_timer 0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] player_score 100
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_score matches 51.. run function test2:test2_main_if_3
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] player_score matches 51.. run function test2:test2_main_else_3
function test2:test2_main_if_end_3
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] game_timer matches ..9 run function test2:test2_main_while_4
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_count matches ..4 run function test2:test2_main_while_5
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_count matches 1.. run function test2:test2_main_if_6
function test2:test2_main_if_end_6