execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_level > = 5 run function registry:conditional_demo_if_3
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] player_level > = 5 run function registry:conditional_demo_else_3
function registry:conditional_demo_if_end_3