scoreboard objectives add player_level dummy
scoreboard players set @s player_level 15
data modify storage mdl:variables player_class set value ""
data modify storage mdl:variables player_class set value "warrior"
scoreboard objectives add experience dummy
scoreboard players set @s experience 75
# If statement: score @s player_level >= 10
execute if score @s player_level >= 10 run # If statement: score @s player_class == 'warrior'
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run # If statement: score @s experience >= 50
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run execute if score @s experience >= 50 run say Advanced warrior detected!
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run execute if score @s experience >= 50 run effect give @s minecraft:strength 10 2
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run execute if score @s experience >= 50 run effect give @s minecraft:glowing 10 0
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run # Else statement
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run execute unless score @s experience >= 50 run say Novice warrior
execute if score @s player_level >= 10 run execute if data storage mdl:variables player_class matches 'warrior' run execute unless score @s experience >= 50 run effect give @s minecraft:haste 10 0
execute if score @s player_level >= 10 run # Else statement
execute if score @s player_level >= 10 run execute unless data storage mdl:variables player_class matches 'warrior' run say Unknown advanced class
execute if score @s player_level >= 10 run execute unless data storage mdl:variables player_class matches 'warrior' run effect give @s minecraft:glowing 10 0
# Else statement
execute unless score @s player_level >= 10 run say Beginner player
execute unless score @s player_level >= 10 run effect give @s minecraft:jump_boost 10 0
