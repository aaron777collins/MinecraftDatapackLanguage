scoreboard objectives add counter dummy
scoreboard players set @s counter 0
data modify storage mdl:variables message set value ""
data modify storage mdl:variables message set value "Hello, MDL!"
data modify storage mdl:variables items set value []
data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "sword"
data modify storage mdl:variables items append value "shield"
data modify storage mdl:variables items append value "potion"
say "Starting MDL feature test"
tellraw @a {"text":"Testing all MDL features","color":"green"}
scoreboard players set @s counter 42
data modify storage mdl:variables message set value "Updated message"
insert items[1] "axe"
pop items
data modify storage mdl:variables full_message set value ""
data modify storage mdl:variables left_0 set value ""
data modify storage mdl:variables concat_1 set value ""
data modify storage mdl:variables concat_1 append value "Items: "
# Access element at index 0 from items
data modify storage mdl:temp element set from storage mdl:variables items[0]
data modify storage mdl:variables concat_2 set from storage mdl:temp element
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables concat_2
data modify storage mdl:variables concat_1 append value storage mdl:temp concat
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables concat_1
data modify storage mdl:variables left_0 append value storage mdl:temp concat
data modify storage mdl:variables left_0 append value " and "
# Access element at index 1 from items
data modify storage mdl:temp element set from storage mdl:variables items[1]
data modify storage mdl:variables right_3 set from storage mdl:temp element
scoreboard players operation @s full_message = @s left_0
scoreboard players add @s full_message right_3
say full_message
scoreboard objectives add result dummy
scoreboard players operation @s left_4 = @s counter
scoreboard players add @s left_4 10
scoreboard players operation @s result = @s left_4
scoreboard players operation @s result *= @s 2
say "Result: " + result
# ERROR: Failed to process IfStatement - 'IfStatement' object has no attribute 'if_body'
# While loop: score @s counter matches 1..
execute if score @s counter matches 1.. run say "Counter: " + counter
execute if score @s counter matches 1.. run scoreboard players operation @s counter = @s counter
scoreboard players remove @s counter 1
# For loop over @a
execute as @a run tellraw @s {"text":"Hello player!","color":"blue"}
# For-in loop over items
execute store result storage mdl:temp list_length int 1 run data get storage mdl:variables items
execute if data storage mdl:variables items run function test:for_in_item_items
scoreboard objectives add item_count dummy
# Get length of items
execute store result score @s item_count run data get storage mdl:variables items
say "Total items: " + item_count
scoreboard objectives add index dummy
scoreboard players set @s index 0
data modify storage mdl:variables first_item set value ""
# Access element at variable index index from items
execute store result storage mdl:temp index int 1 run scoreboard players get @s index
data modify storage mdl:temp element set from storage mdl:variables items[storage mdl:temp index]
data modify storage mdl:variables first_item set from storage mdl:temp element
say "First item: " + first_item
scoreboard objectives add complex_result dummy
scoreboard players operation @s left_6 = @s counter
scoreboard players add @s left_6 5
scoreboard players operation @s left_5 = @s left_6
scoreboard players operation @s left_5 *= @s 2
scoreboard players operation @s complex_result = @s left_5
scoreboard players remove @s complex_result 10
say "Complex result: " + complex_result
function test:helper_function
function utils:calculator
# ERROR: Failed to process IfStatement - 'IfStatement' object has no attribute 'if_body'
clear items
say "List cleared!"
tellraw @a {"text":"All features tested successfully!","color":"green"}
