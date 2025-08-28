scoreboard objectives add local_counter dummy
scoreboard players set @s local_counter 10
data modify storage mdl:variables player_name set value ""
data modify storage mdl:variables player_name set value "Steve"
data modify storage mdl:variables local_items set value []
data modify storage mdl:variables local_items append value "apple"
data modify storage mdl:variables local_items append value "bread"
data modify storage mdl:variables local_items append value "steak"
scoreboard players add @s local_counter 5
scoreboard players add @s global_counter 1
data modify storage mdl:variables player_name set value "Alex"
scoreboard players add @s global_message Updated: 
data modify storage mdl:variables full_name set value ""
data modify storage mdl:variables full_name set value " Minecraft"
data modify storage mdl:variables local_items append value "golden_apple"
# Insert 'enchanted_sword' at index 1 in local_items
data modify storage mdl:variables local_items insert 1 value "enchanted_sword"
scoreboard objectives add first_item dummy
scoreboard players set @s first_item 0
scoreboard objectives add item_count dummy
scoreboard players set @s item_count 0
scoreboard objectives add result dummy
scoreboard players set @s result 0
scoreboard objectives add modulo_result dummy
scoreboard players set @s modulo_result 0
data modify storage mdl:variables status set value ""
data modify storage mdl:variables status set value " has "
say Variable demo complete
tellraw @s {"text":"Result: " + result}
tellraw @s {"text":"Modulo: " + modulo_result}
tellraw @s {"text":"Status: " + status}
