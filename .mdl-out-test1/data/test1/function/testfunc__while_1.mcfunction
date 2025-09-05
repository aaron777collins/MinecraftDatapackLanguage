# Function: test1:testfunc__while_1
tellraw @a {"text":"Hello from testfunc!"}
scoreboard players operation @s temp_1 = @s testfunccount1
scoreboard players remove @s temp_1 1
scoreboard players operation @s testfunccount1 = @s temp_1
execute if score @s testfunccount1 matches 1.. run function test1:testfunc__while_1
