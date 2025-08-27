say Testing mixed control structures
execute if entity @s[type=minecraft:player] run function test:mixed_control_if_1
execute if score @s counter matches 1.. run function test:mixed_control_while_control_2
execute if entity @e[type=minecraft:zombie,distance=..5] run function test:mixed_control_for_control_3
execute unless entity @s[type=minecraft:player] run function test:mixed_control_else
