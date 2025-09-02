execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Game started! Phase: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"gamePhase"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] playerHealth matches ..9 run function registry:start_game_if_1
scoreboard players add @s playerScore 10
tellraw @a [{"text":"Score increased to: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"playerScore"}}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] globalTimer matches ..4 run function registry:test_start_game_while_4
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] gamePhase matches 1 run function registry:start_game_if_5