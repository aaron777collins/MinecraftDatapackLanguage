scoreboard players set @s result 0
scoreboard players set @s result 5
scoreboard players add @s result 3
tellraw @s [{"text":"Calculation result: "},{"score":{"name":"@s","objective":"result"}}]
tellraw @s [{"text":"Score: "}, {"score": {"name":"@s","objective":"player_score"}}]