execute if score @e[type=armor_stand,tag=mdl_server,limit=1] weapon_type matches 1 run function example:weapon_effects_if_1
execute unless score @e[type=armor_stand,tag=mdl_server,limit=1] weapon_type matches 1 run function example:weapon_effects_else_1
function example:weapon_effects_if_end_1