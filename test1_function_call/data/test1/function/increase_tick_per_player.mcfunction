
    scoreboard players add @s player_tick_counter 1
    
execute if score @s player_tick_counter matches 101.. run function test1:increase_tick_per_player_if_1
function test1:increase_tick_per_player_if_end_1