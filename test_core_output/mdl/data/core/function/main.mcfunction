scoreboard objectives add counter dummy
scoreboard players set @s counter 0
data modify storage mdl:variables message set value ""
data modify storage mdl:variables message set value "Hello, MDL!"
data modify storage mdl:variables items set value []
data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "sword"
data modify storage mdl:variables items append value "shield"
data modify storage mdl:variables items append value "potion"
say "Starting core features test"
tellraw @a {"text":"Testing core MDL features","color":"green"}
scoreboard players set @s counter 42
data modify storage mdl:variables message set value "Updated message"
say "List length: " + length(items)
data modify storage mdl:variables first_item set value ""
# Access element at index 0 from items
data modify storage mdl:temp element set from storage mdl:variables items[0]
data modify storage mdl:variables first_item set from storage mdl:temp element
data modify storage mdl:variables second_item set value ""
# Access element at index 1 from items
data modify storage mdl:temp element set from storage mdl:variables items[1]
data modify storage mdl:variables second_item set from storage mdl:temp element
say "First item: " + first_item
say "Second item: " + second_item
scoreboard objectives add result dummy
scoreboard players operation @s left_0 = @s counter
scoreboard players add @s left_0 10
scoreboard players operation @s result = @s left_0
scoreboard players operation @s result *= @s 2
say "Result: " + result
# If statement: score @s counter > 40
execute if score @s counter > 40 run say "Counter is greater than 40"
execute if score @s counter > 40 run scoreboard players operation @s counter = @s counter
scoreboard players remove @s counter 10
# Else statement
execute score @s counter > 40 run say "Counter is 40 or less"
execute score @s counter > 40 run scoreboard players operation @s counter = @s counter
scoreboard players add @s counter 10
# While loop: score @s counter > 0
execute if score @s counter > 0 run say "Counter: " + counter
execute if score @s counter > 0 run scoreboard players operation @s counter = @s counter
scoreboard players remove @s counter 1
# For loop over @a
execute as @a run tellraw @s {"text":"Hello player!","color":"blue"}
# For-in loop over items
execute store result storage mdl:temp list_length int 1 run data get storage mdl:variables items
execute if data storage mdl:variables items run function core:for_in_item_items
scoreboard objectives add complex_result dummy
scoreboard players operation @s left_2 = @s counter
scoreboard players add @s left_2 5
scoreboard players operation @s left_1 = @s left_2
scoreboard players operation @s left_1 *= @s 2
scoreboard players operation @s complex_result = @s left_1
scoreboard players remove @s complex_result 10
say "Complex result: " + complex_result
data modify storage mdl:variables full_message set value ""
data modify storage mdl:variables left_3 set value ""
data modify storage mdl:variables concat_4 set value ""
data modify storage mdl:variables concat_4 append value "Items: "
# Access element at index 0 from items
data modify storage mdl:temp element set from storage mdl:variables items[0]
data modify storage mdl:variables concat_5 set from storage mdl:temp element
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables concat_5
data modify storage mdl:variables concat_4 append value storage mdl:temp concat
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables concat_4
data modify storage mdl:variables left_3 append value storage mdl:temp concat
data modify storage mdl:variables left_3 append value " and "
# Access element at index 1 from items
data modify storage mdl:temp element set from storage mdl:variables items[1]
data modify storage mdl:variables right_6 set from storage mdl:temp element
scoreboard players operation @s full_message = @s left_3
scoreboard players add @s full_message right_6
say full_message
insert items[1] "new_item"
say "After insert: " + length(items)
say "After remove: " + length(items)
pop items
say "After pop: " + length(items)
scoreboard objectives add index dummy
scoreboard players set @s index 5
# If statement: score @s index < length(items)
execute if score @s index < length(items) run data modify storage mdl:variables safe_item set value ""
execute if score @s index < length(items) run # Access element at variable index index from items
execute if score @s index < length(items) run execute store result storage mdl:temp index int 1 run scoreboard players get @s index
execute if score @s index < length(items) run data modify storage mdl:temp element set from storage mdl:variables items[storage mdl:temp index]
execute if score @s index < length(items) run data modify storage mdl:variables safe_item set from storage mdl:temp element
execute if score @s index < length(items) run say "Safe access: " + safe_item
# Else statement
execute score @s index < length(items) run say "Index out of bounds!"
clear items
say "List cleared!"
tellraw @a {"text":"All core features tested successfully!","color":"green"}
