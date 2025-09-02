execute if score @e[type=armor_stand,tag=mdl_server,limit=1] i % 2 matches 0 run function registry:test_loop_demo_while_2_if_0
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] i % 2 matches 0 run function registry:test_loop_demo_while_2_else_0
function registry:test_loop_demo_while_2_if_end_0
scoreboard players add @s i 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] i % 5 matches 0 run function registry:test_loop_demo_while_2_if_2
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] i < @e[type=armor_stand,tag=mdl_server,limit=1] max_iterations run function registry:test_loop_demo_while_2