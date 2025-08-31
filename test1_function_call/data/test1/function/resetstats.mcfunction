scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_hello_count 0
scoreboard players set @a player_hello_count 0
tellraw @a [{"text":"Statistics reset !"}]
tellraw @a {"text":"Your statistics have been reset!","color":"yellow"}