execute if score @e[type=armor_stand,tag=mdl_server,limit=1] player_class matches 2 run function scoped_calls:conditional_demo_if_3_if_0
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] player_class matches 2 run function scoped_calls:conditional_demo_if_3_else_0
function scoped_calls:conditional_demo_if_3_if_end_0