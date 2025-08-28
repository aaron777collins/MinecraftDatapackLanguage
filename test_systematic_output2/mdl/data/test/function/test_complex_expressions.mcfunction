data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "apple"
data modify storage mdl:variables items append value "banana"
data modify storage mdl:variables items append value "cherry"
scoreboard objectives add index dummy
scoreboard players set @s index 1
data modify storage mdl:variables item set value ""
data modify storage mdl:variables item set value "ListAccessExpression(list_name='items', index=VariableExpression(name='index'))"
scoreboard objectives add count dummy
scoreboard players set @s count 0
data modify storage mdl:variables message set value ""
data modify storage mdl:variables message set value "Found "
tellraw @s {"text":message,"color":"green"}
scoreboard objectives add result dummy
scoreboard players set @s result 0
say Result: $result
data modify storage mdl:variables nested set value []
data modify storage mdl:variables nested append value "unknown"
data modify storage mdl:variables nested append value "unknown"
data modify storage mdl:variables nested_item set value ""
data modify storage mdl:variables nested_item set value "0"
say Nested item: $nested_item
