execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add globalCounter dummy
scoreboard objectives add playerScore dummy
scoreboard objectives add counter dummy
scoreboard objectives add global_counter dummy
scoreboard objectives add global_timer dummy
scoreboard objectives add playerCounter dummy
scoreboard objectives add teamCounter dummy
scoreboard objectives add globalTimer dummy
scoreboard objectives add maxCount dummy
scoreboard objectives add playerHealth dummy
scoreboard objectives add gamePhase dummy
scoreboard objectives add local_counter dummy
scoreboard objectives add player_score dummy