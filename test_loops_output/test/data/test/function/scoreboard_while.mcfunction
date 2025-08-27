say Testing while loop with scoreboard condition
scoreboard objectives add test_obj dummy
scoreboard players set @s test_obj 10
execute if score @s test_obj matches 5.. run function test:scoreboard_while_while_control_3
