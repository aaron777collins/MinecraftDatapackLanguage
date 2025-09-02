execute if score @e[type=armor_stand,tag=mdl_server,limit=1] experience > = 50 run function registry:conditional_demo_if_3_if_0_if_0
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] experience > = 50 run function registry:conditional_demo_if_3_if_0_else_0
function registry:conditional_demo_if_3_if_0_if_end_0