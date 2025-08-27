say Testing for loop with complex selector
execute if entity @a[gamemode=survival] run function test:complex_for_for_control_1
if "entity @s[nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}]":
say Player has diamond sword!
effect give @s minecraft:strength 10 1
execute run function test:complex_for_else
