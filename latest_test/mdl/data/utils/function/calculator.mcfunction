say [utils:calculator] Calculator function
scoreboard players set @s a 10
scoreboard players set @s b 5
# String concatenation: a + b
data modify storage mdl:variables result set from storage mdl:variables a
execute store result storage mdl:temp concat string 1 run data get storage mdl:variables b
data modify storage mdl:variables result append value storage mdl:temp concat
say Calculation result: result
