scoreboard players set @s global_hello_count<global> 0
scoreboard players set @s player_hello_count<@s> 0
tellraw @a [{"text":"Statistics reset !"}]
tellraw @a {"text":"Your statistics have been reset!","color":"yellow"}