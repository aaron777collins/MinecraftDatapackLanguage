say [game:player_action] Player action detected
execute if entity @s[type=minecraft:player] run function utils:calculator
execute if entity @s[type=minecraft:player] run effect give @s minecraft:speed 5 0
