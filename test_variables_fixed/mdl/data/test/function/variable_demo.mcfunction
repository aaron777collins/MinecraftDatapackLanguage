scoreboard objectives add local_counter dummy
scoreboard players set @s local_counter 10
data modify storage mdl:variables player_name set value ""
data modify storage mdl:variables player_name set value "Steve"
data modify storage mdl:variables local_items set value []
data modify storage mdl:variables local_items set value []
data modify storage mdl:variables local_items append value "apple"
data modify storage mdl:variables local_items append value "bread"
data modify storage mdl:variables local_items append value "steak"
scoreboard players operation @s local_counter = @s local_counter
scoreboard players add @s local_counter 5
scoreboard players operation @s global_counter = @s global_counter
scoreboard players add @s global_counter 1
data modify storage mdl:variables player_name set value "Alex"
data modify storage mdl:variables global_message set value ""
data modify storage mdl:variables global_message append value "Updated: "
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables player_name
data modify storage mdl:variables global_message append value storage mdl:temp concat
data modify storage mdl:variables full_name set value ""
data modify storage mdl:variables full_name set value ""
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables player_name
data modify storage mdl:variables full_name append value storage mdl:temp concat
data modify storage mdl:variables full_name append value " Minecraft"
data modify storage mdl:variables local_items append value "golden_apple"
# Insert 'enchanted_sword' at index 1 in local_items
data modify storage mdl:variables local_items insert 1 value "enchanted_sword"
scoreboard objectives add first_item dummy
# Access element at index 0 from local_items
data modify storage mdl:temp element set from storage mdl:variables local_items[0]
data modify storage mdl:variables first_item set from storage mdl:temp element
scoreboard objectives add item_count dummy
# Get length of local_items
execute store result score @s item_count run data get storage mdl:variables local_items
scoreboard objectives add result dummy
scoreboard players operation @s left_0 = @s local_counter
scoreboard players operation @s left_0 *= @s 2
scoreboard players operation @s result = @s left_0
scoreboard players add @s result global_counter
scoreboard objectives add modulo_result dummy
scoreboard players operation @s modulo_result = @s result
scoreboard players add @s modulo_result 7
data modify storage mdl:variables status set value ""
data modify storage mdl:variables status set value ""
data modify storage mdl:variables left_2 set value ""
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables player_name
data modify storage mdl:variables left_2 append value storage mdl:temp concat
data modify storage mdl:variables left_2 append value " has "
scoreboard players operation @s concat_1 = @s left_2
scoreboard players add @s concat_1 item_count
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables concat_1
data modify storage mdl:variables status append value storage mdl:temp concat
data modify storage mdl:variables status append value " items"
say Variable demo complete
tellraw @s {"text":"Result: ", "extra":[{"score":{"name":"result","objective":"result"}}]}
tellraw @s {"text":"Modulo: ", "extra":[{"score":{"name":"modulo_result","objective":"modulo_result"}}]}
tellraw @s {"text":"Status: ", "extra":[{"nbt":"status","storage":"mdl:variables"}]}
