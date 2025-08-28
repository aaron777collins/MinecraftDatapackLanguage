scoreboard objectives add tick_count dummy
scoreboard players set @s tick_count 0
scoreboard players operation @s tick_count = @s tick_count
scoreboard players add @s tick_count 1
# ERROR: Failed to process IfStatement - 'IfStatement' object has no attribute 'if_body'
