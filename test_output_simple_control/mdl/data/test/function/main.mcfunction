execute if $health$ matches ..9 run say "Health is low!"
execute unless $health$ matches ..9 run say "Health is okay"
execute if $counter$ matches 4.. run say "Counter is high!"
execute if $counter$ < 10 run data modify storage mdl:variables counter set value "$counter$"
execute if $counter$ < 10 run data modify storage mdl:variables counter append value "LiteralExpression(value='1', type='number')"
execute if $counter$ < 10 run tellraw @s [{"text":""Counter: "},{"score":{"name":"@s","objective":"$counter$""}}]
execute as @a run say "Hello $player$"
