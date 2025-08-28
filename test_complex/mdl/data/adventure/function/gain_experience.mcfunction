scoreboard objectives add exp_gained dummy
scoreboard players set @s exp_gained 10
# String concatenation: player_experience + exp_gained
data modify storage mdl:variables player_experience set from storage mdl:variables player_experience
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables exp_gained
data modify storage mdl:variables player_experience append value storage mdl:temp concat
scoreboard objectives add exp_needed dummy
scoreboard players set @s exp_needed 0
execute if score @s player_experience >= exp_needed run scoreboard players add @s player_level 1
execute if score @s player_experience >= exp_needed run scoreboard players set @s player_experience 0
execute if score @s player_experience >= exp_needed run tellraw @s {"text":"Level Up! You are now level " + player_level,"color":"yellow"}
execute if score @s player_experience >= exp_needed run effect give @s minecraft:glowing 10 0
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'warrior' run effect give @s minecraft:strength 30 0
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'warrior' run data modify storage mdl:variables player_inventory append value "iron_sword"
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'mage' unless score @s player_class == 'warrior' run effect give @s minecraft:night_vision 30 0
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'mage' unless score @s player_class == 'warrior' run data modify storage mdl:variables player_inventory append value "magic_staff"
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'archer' unless score @s player_class == 'warrior' unless score @s player_class == 'mage' run effect give @s minecraft:speed 30 0
execute if score @s player_experience >= exp_needed run execute if score @s player_class == 'archer' unless score @s player_class == 'warrior' unless score @s player_class == 'mage' run data modify storage mdl:variables player_inventory append value "enhanced_bow"
