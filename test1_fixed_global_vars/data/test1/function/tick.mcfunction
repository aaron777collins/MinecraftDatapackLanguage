execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] tickcounter 1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] tickcounter matches 101.. run function test1:tick_if_1
function test1:tick_if_end_1