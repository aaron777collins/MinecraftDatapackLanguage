tellraw @a [{"text":"Hello, Minecraft !"}]
tellraw @a {"text":"Welcome to my datapack!","color":"green"}
scoreboard players add @e[type=armor_stand,tag=mdl_server,limit=1] counter 1
tellraw @a {"text":"Counter: $counter$"};
    tellraw @a {"text":"Timerenabled: $timerenabled$"};
say "To enable the timer, run /function test1:enabletimer";
    say "To disable the timer, run /function test1:disabletimer";
