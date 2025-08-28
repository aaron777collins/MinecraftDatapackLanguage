say "Helper function called!"
scoreboard objectives add helper_var dummy
scoreboard players set @s helper_var 100
say "Helper value: " + helper_var
