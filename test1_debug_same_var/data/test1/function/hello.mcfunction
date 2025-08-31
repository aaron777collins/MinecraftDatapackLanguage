execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Hello, Minecraft !"}]
tellraw @a {"text":"Welcome to my datapack!","color":"green"}
scoreboard players operation @e[type=armor_stand,tag=mdl_server,limit=1] global_hello_count = @e[type=armor_stand,tag=mdl_server,limit=1] global_hello_count
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] global_hello_count 1
scoreboard players operation @a player_hello_count = @s player_hello_count
scoreboard players add @a player_hello_count 1
tellraw @a [{"text": "Global Hello Count: ", "color": "gold"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "global_hello_count"}, "color": "gold"}]
tellraw @a [{"text": "Your Hello Count: ", "color": "blue"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "player_hello_count"}, "color": "blue"}]
tellraw @a [{"text": "Your Timer Enabled: ", "color": "green"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "player_timer_enabled"}, "color": "green"}]

    say "To enable your timer, run /function test1:enabletimer"
    say "To disable your timer, run /function test1:disabletimer"
    say "To see all players' stats, run /function test1:showstats"
    