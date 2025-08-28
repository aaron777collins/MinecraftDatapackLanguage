data modify storage mdl:variables numbers set value []
data modify storage mdl:variables numbers set value []
data modify storage mdl:variables numbers append value "1"
data modify storage mdl:variables numbers append value "2"
data modify storage mdl:variables numbers append value "3"
data modify storage mdl:variables numbers append value "4"
data modify storage mdl:variables numbers append value "5"
say "Original list length: " + length(numbers)
say "After append: " + length(numbers)
insert numbers[0] 0
say "After insert: " + length(numbers)
say "After remove: " + length(numbers)
pop numbers
say "After pop: " + length(numbers)
scoreboard objectives add first dummy
# Access element at index 0 from numbers
data modify storage mdl:temp element set from storage mdl:variables numbers[0]
data modify storage mdl:variables first set from storage mdl:temp element
scoreboard objectives add last dummy
scoreboard players operation @s index_7 = @s FunctionCall(function_name='length', arguments=[VariableExpression(name='numbers')])
scoreboard players remove @s index_7 1
# Access element at complex index from numbers
execute store result storage mdl:temp index int 1 run scoreboard players get @s index_7
data modify storage mdl:temp element set from storage mdl:variables numbers[storage mdl:temp index]
data modify storage mdl:variables last set from storage mdl:temp element
say "First: " + first + ", Last: " + last
