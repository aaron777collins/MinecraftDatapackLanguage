say Testing simple while loop
scoreboard players set @s loop_counter 5
execute if score @s loop_counter matches 1.. run function test:simple_while_while_control_2
