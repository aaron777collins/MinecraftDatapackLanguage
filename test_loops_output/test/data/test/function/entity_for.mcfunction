say Testing for loop with entity collection
tag @e[type=minecraft:player] add players
execute if entity @e[tag=players] run function test:entity_for_for_control_2
