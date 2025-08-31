execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard objectives add global_timer dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 0
scoreboard objectives add global_hello_count dummy
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_hello_count 0
scoreboard objectives add player_hello_count dummy
scoreboard players set @a player_hello_count 0
scoreboard objectives add player_timer_enabled dummy
scoreboard players set @a player_timer_enabled 0
scoreboard objectives add player_tick_counter dummy
scoreboard players set @a player_tick_counter 0
scoreboard objectives add global_hello_count<global> dummy
scoreboard objectives add player_hello_count<@s> dummy
scoreboard objectives add global_timer<global> dummy