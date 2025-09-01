say say
say "Starting basic raw block test"
scoreboard players set @s player_timer_enabled 1
    execute as @a run function raw_test:increase_tick_per_player
    say "Raw commands bypass MDL syntax checking"say "Basic raw block test complete"