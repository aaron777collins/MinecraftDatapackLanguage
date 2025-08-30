execute if score @e[type=armor_stand,tag=mdl_server,limit=1] timerenabled matches 1 run function test1:tick_if_0
function test1:tick_if_end_0
scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] tickcounter 0