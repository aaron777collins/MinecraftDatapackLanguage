# Function: test1:main

tellraw @a {"text":"Hello from test1!"}
scoreboard players set @s counter 10
tellraw @a {"text":"Counter: ","extra":[{"score":{"name":"@s","objective":"counter"}}]}
execute if score @s counter matches 6.. run function test1:main__if_1
execute unless score @s counter matches 6.. run function test1:main__else_1
execute as @a run function test1:testfunc