scoreboard players operation @e[type=armor_stand,tag=mdl_server,limit=1] global_timer = @e[type=armor_stand,tag=mdl_server,limit=1] global_timer
scoreboard players remove @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 1
tellraw @a [{"text": "Reducing global timer by 1 tick. New value: ", "color": "yellow"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "global_timer"}, "color": "yellow"}]
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] global_timer matches 201.. run function test1:test1_tick_while_1