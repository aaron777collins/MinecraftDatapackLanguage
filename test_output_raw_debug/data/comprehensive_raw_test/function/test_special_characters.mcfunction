say "Testing special characters"
tellraw @a {"text":"Special chars: $@#%^&*()","color":"gold"}
    tellraw @a {"text":"Complex JSON: {\"nested\":{\"value\":42}}","color":"blue"}
    execute as @a run data modify entity @s CustomName set value "Complex Name with Spaces"
say "Special characters test complete"