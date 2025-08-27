say Testing nested loops
scoreboard players set @s outer 3
execute if score @s outer matches 1.. run function test:nested_loops_while_control_2
execute if score @s inner matches 1.. run function test:nested_loops_while_control_3
