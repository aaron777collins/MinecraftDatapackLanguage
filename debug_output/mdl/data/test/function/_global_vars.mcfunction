data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "apple"
data modify storage mdl:variables items append value "banana"
data modify storage mdl:variables items append value "cherry"
scoreboard objectives add index dummy
scoreboard players set @s index 0
data modify storage mdl:variables item set value ""
data modify storage mdl:variables item set value "ListAccessExpression(list_name='items', index=VariableExpression(name='index'))"
