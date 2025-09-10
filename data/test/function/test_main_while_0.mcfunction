tellraw @a [{"text":"Counter: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_global,limit=1]","objective":"counter"}}]
scoreboard players add @s counter 1
execute if score @e[type=armor_stand,tag=mdl_global,limit=1] counter matches ..2 run function test:test_main_while_0