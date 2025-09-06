# Function: hello_world:main

scoreboard players operation @s temp_1 = @a globalCounter
scoreboard players add @s temp_1 1
scoreboard players operation @a globalCounter = @s temp_1
tellraw @a {"text":"Hello, Minecraft!"}
 tellraw @a {"text":"Welcome to my datapack!","color":"green"} 
tellraw @a {"text":"Global counter: $globalCounter$"}