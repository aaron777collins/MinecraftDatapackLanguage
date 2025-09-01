say "Testing raw blocks with context"
say "MDL variable value: ${testVar}"
scoreboard players set @s mdl_test_var 42
    execute as @a run scoreboard players set @s mdl_test_var 42
say "Raw with context test complete"