scoreboard objectives add global_counter dummy
scoreboard players set @s global_counter 0
data modify storage mdl:variables global_message set value ""
data modify storage mdl:variables global_message set value "Hello from global!"
data modify storage mdl:variables global_items set value []
data modify storage mdl:variables global_items set value []
data modify storage mdl:variables global_items append value "apple"
data modify storage mdl:variables global_items append value "banana"
data modify storage mdl:variables global_items append value "cherry"
