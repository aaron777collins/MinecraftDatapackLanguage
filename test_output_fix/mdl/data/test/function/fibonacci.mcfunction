scoreboard objectives add n dummy
scoreboard objectives add a dummy
scoreboard objectives add b dummy
scoreboard objectives add i dummy
scoreboard objectives add temp dummy
execute if score @s i matches ..10 run scoreboard players operation @s temp = @s a
execute if score @s i matches ..10 run data modify storage mdl:variables temp set from storage mdl:variables temp
execute if score @s i matches ..10 run data modify storage mdl:variables temp append from storage mdl:variables b
execute if score @s i matches ..10 run scoreboard players operation @s a = @s b
execute if score @s i matches ..10 run scoreboard players operation @s b = @s temp
execute if score @s i matches ..10 run data modify storage mdl:variables i set from storage mdl:variables i
execute if score @s i matches ..10 run data modify storage mdl:variables i append value "LiteralExpression(value='1', type='number')"
tellraw @s [{"text":"Fibonacci result: "},{"score":{"name":"@s","objective":"b"}}]
tellraw @s [{"text":"Fibonacci(" ","score":{"name":"@s","objective":"n"},"text":" ") = " ","score":{"name":"@s","objective":"b"}}]
