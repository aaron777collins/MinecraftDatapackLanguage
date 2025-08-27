say Testing for loop with item collection
tag @e[type=minecraft:item] add items
execute if entity @e[tag=items] run function test:item_for_for_control_2
