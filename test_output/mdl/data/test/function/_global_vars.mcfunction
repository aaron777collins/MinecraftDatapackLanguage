scoreboard objectives add global_counter dummy
scoreboard players set @s global_counter 0
data modify storage mdl:variables global_message set value ""
data modify storage mdl:variables global_message set value "System Ready"
data modify storage mdl:variables global_items set value []
data modify storage mdl:variables global_items append value "sword"
data modify storage mdl:variables global_items append value "shield"
data modify storage mdl:variables global_items append value "potion"
