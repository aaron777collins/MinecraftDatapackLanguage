scoreboard players set @s health 100
data modify storage mdl:variables name set value "Player"
data modify storage mdl:variables items set value []
data modify storage mdl:variables items append value "sword"
data modify storage mdl:variables items append value "shield"
scoreboard players add @s health 10
scoreboard players add @s name  Hero
data modify storage mdl:variables items append value "potion"
execute if score @s health matches 100.. run say Player is healthy
execute unless score @s health matches 100.. run say Player needs healing
scoreboard players set @s counter 0
execute if score @s counter matches ..2 run say Loop iteration
execute if score @s counter matches ..2 run scoreboard players add @s counter 1
say Test complete
tellraw @s {"text":"Final health: " + health}
