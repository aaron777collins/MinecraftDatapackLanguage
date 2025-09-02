execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Testing raw blocks final verification"}]
scoreboard objectives add test_score dummy "Test Score"
scoreboard players set @a test_score 0
scoreboard players add @a test_score 10
tellraw @a [{"text":"Raw block completed successfully"}]