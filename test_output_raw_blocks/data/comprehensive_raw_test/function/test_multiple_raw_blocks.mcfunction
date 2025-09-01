say say
say "Testing multiple raw blocks"
scoreboard players set @s test_counter 0 say "First raw block complete"
scoreboard players add @s test_counter 1 say "Second raw block complete"
scoreboard players add @s test_counter 1 say "Third raw block complete"
scoreboard players get @s test_counter say "Multiple raw blocks test complete"