execute if score @s player_level >= 5 run execute if score @s player_class == 'warrior' run say Warrior specialization available
execute if score @s player_level >= 5 run execute if score @s player_class == 'warrior' run effect give @s minecraft:resistance 10 0
execute if score @s player_level >= 5 run execute if score @s player_class == 'warrior' run effect give @s minecraft:strength 10 0
execute if score @s player_level >= 5 run execute if score @s player_class == 'mage' unless score @s player_class == 'warrior' run say Mage specialization available
execute if score @s player_level >= 5 run execute if score @s player_class == 'mage' unless score @s player_class == 'warrior' run effect give @s minecraft:levitation 5 0
execute if score @s player_level >= 5 run execute if score @s player_class == 'mage' unless score @s player_class == 'warrior' run effect give @s minecraft:night_vision 10 0
execute if score @s player_level >= 5 run execute if score @s player_class == 'archer' unless score @s player_class == 'warrior' unless score @s player_class == 'mage' run say Archer specialization available
execute if score @s player_level >= 5 run execute if score @s player_class == 'archer' unless score @s player_class == 'warrior' unless score @s player_class == 'mage' run effect give @s minecraft:speed 10 0
execute if score @s player_level >= 5 run execute if score @s player_class == 'archer' unless score @s player_class == 'warrior' unless score @s player_class == 'mage' run effect give @s minecraft:jump_boost 10 0
