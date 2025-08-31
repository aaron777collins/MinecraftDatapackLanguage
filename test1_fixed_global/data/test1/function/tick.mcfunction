execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
scoreboard players operation @e[type=armor_stand,tag=mdl_server,limit=1] global_timer = global global_timer
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 1

    execute as @a run function test1:increase_tick_per_player
    
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] global_timer matches 201.. run function test1:tick_if_2
function test1:tick_if_end_2