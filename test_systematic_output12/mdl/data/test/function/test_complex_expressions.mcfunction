data modify storage mdl:variables items set value []
data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "apple"
data modify storage mdl:variables items append value "banana"
data modify storage mdl:variables items append value "cherry"
scoreboard objectives add index dummy
scoreboard players set @s index 1
data modify storage mdl:variables item set value ""
# Access element at variable index index from items
execute store result storage mdl:temp index int 1 run scoreboard players get @s index
data modify storage mdl:temp element set from storage mdl:variables items[storage mdl:temp index]
data modify storage mdl:variables item set from storage mdl:temp element
scoreboard objectives add count dummy
# Get length of items
execute store result score @s count run data get storage mdl:variables items
data modify storage mdl:variables message set value ""
scoreboard players operation @s left_1 = @s Found 
scoreboard players add @s left_1 item
scoreboard players operation @s left_0 = @s left_1
scoreboard players add @s left_0  at index 
scoreboard players operation @s message = @s left_0
scoreboard players add @s message index
tellraw @s {"text":message,"color":"green"}
scoreboard objectives add result dummy
scoreboard players operation @s left_2 = @s count
scoreboard players add @s left_2 5
scoreboard players operation @s result = @s left_2
scoreboard players operation @s result *= @s 2
say Result: $result
data modify storage mdl:variables nested set value []
data modify storage mdl:variables nested set value []
data modify storage mdl:variables nested append value "unknown"
data modify storage mdl:variables nested append value "unknown"
data modify storage mdl:variables nested_item set value ""
# Access element at index 0 from nested
data modify storage mdl:temp element set from storage mdl:variables nested[0]
data modify storage mdl:variables nested_item set from storage mdl:temp element
say Nested item: $nested_item
