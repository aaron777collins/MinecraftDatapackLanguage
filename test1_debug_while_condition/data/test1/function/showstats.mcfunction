tellraw @a {"text":"=== Player Statistics ===","color":"gold","bold": true}
tellraw @a [{"text": "Global Hello Count: ", "color": "gold"}, {"score": {"name": "@s", "objective": "global_hello_count"}, "color": "gold"}]
tellraw @a [{"text": "Your Hello Count: ", "color": "blue"}, {"score": {"name": "@s", "objective": "player_hello_count"}, "color": "blue"}]
tellraw @a [{"text": "Your Timer Status: ", "color": "green"}, {"score": {"name": "@s", "objective": "player_timer_enabled"}, "color": "green"}]