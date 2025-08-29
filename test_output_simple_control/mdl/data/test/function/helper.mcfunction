scoreboard objectives add result dummy
scoreboard players operation @s result = @s 5
scoreboard players add @s result 3
tellraw @s [{"text":""Result: "},{"score":{"name":"@s","objective":"$result$""}}]
tellraw @s [{"text":"Health: "},{"score":{"name":"@s","objective":"health"}}]
