execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Hello, Minecraft !"}]
tellraw @a {"text":"Welcome to my datapack!","color":"green"}
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] counter 1
tellraw @a [{"text": "Counter: ", "color": "blue"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "counter"}, "color": "blue"}]
tellraw @a [{"text": "Timerenabled: ", "color": "blue"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "timerenabled"}, "color": "blue"}]

    say "To enable the timer, run /function test1:enabletimer"
    say "To disable the timer, run /function test1:disabletimer"
    