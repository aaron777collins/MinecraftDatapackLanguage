scoreboard players set @s local_counter 10
data modify storage mdl:variables player_name set value "Steve"
data modify storage mdl:variables local_items set value []
data modify storage mdl:variables local_items append value "apple"
data modify storage mdl:variables local_items append value "bread"
data modify storage mdl:variables local_items append value "steak"
scoreboard players add @s local_counter 5
scoreboard players add @s global_counter 1
data modify storage mdl:variables player_name set value "Alex"
scoreboard players add @s global_message Updated: 
scoreboard players add @s full_name  Minecraft
data modify storage mdl:variables local_items append value "golden_apple"
# Insert 'enchanted_sword' at index 1 in local_items
data modify storage mdl:variables local_items insert 1 value "enchanted_sword"
# Access element at index 0 from local_items
data modify storage mdl:temp element set from storage mdl:variables local_items[0]
data modify storage mdl:variables first_item set from storage mdl:temp element
data modify storage mdl:variables item_count set value "local_items.length"
scoreboard players set @s result 0
scoreboard players set @s modulo_result 0
scoreboard players set @s status 0
say Variable demo complete
tellraw @s {"text":"Result: " + result}
tellraw @s {"text":"Modulo: " + modulo_result}
tellraw @s {"text":"Status: " + status}
