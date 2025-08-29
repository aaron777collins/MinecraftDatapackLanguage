scoreboard players set @s result 0
scoreboard players set @s result 5
scoreboard players add @s result 3
tellraw @a [{"text":"Calculation result: "},{"score":{"name":"@s","objective":"result"}}]
tellraw @a [{"text":"Score: "}, {"score": {"name":"@s","objective":"player_score"}}]