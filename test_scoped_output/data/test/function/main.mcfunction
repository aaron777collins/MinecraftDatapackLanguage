execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] playerScore matches 11.. run function test:main_if_0
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] globalCounter matches 101.. run function test:main_if_1
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] teamScore matches 51.. run function test:main_if_2
execute if score @e[type=armor_stand,tag=mdl_server,limit=1] playerScore matches 6.. run function test:main_if_3