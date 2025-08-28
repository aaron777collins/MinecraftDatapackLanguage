scoreboard objectives add health dummy
scoreboard players set @s health 15
scoreboard objectives add hunger dummy
scoreboard players set @s hunger 8
data modify storage mdl:variables biome set value ""
data modify storage mdl:variables biome set value "plains"
execute if score @s health < 10 run execute if score @s hunger < 5 run say Player is in critical condition!
execute if score @s health < 10 run execute if score @s hunger < 5 run effect give @s minecraft:regeneration 10 1
execute if score @s health < 10 run execute if score @s hunger < 5 run effect give @s minecraft:saturation 5 0
execute if score @s health < 10 run execute unless score @s hunger < 5 run say Player is low on health
execute if score @s health < 10 run execute unless score @s hunger < 5 run effect give @s minecraft:regeneration 5 0
execute unless score @s health < 10 run say Player is healthy
execute unless score @s health < 10 run effect give @s minecraft:speed 5 0
