scoreboard players add @s counter 1
tellraw @a [{"text":"Schedule counter: "},{"score":{"name":"@s","objective":"counter"}}]
execute if score @s counter matches ..2 run schedule function test_while_fix:test_while_fix_main_while_3 1t