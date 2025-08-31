tellraw @a {"text":"=== All Player Kills ===","color":"yellow","bold": true}
tellraw @a [{"text": "Your kills: ", "color": "green"}, {"score": {"name": "@s", "objective": "player_kills"}, "color": "green"}]
tellraw @a [{"text": "Server uptime: ", "color": "gray"}, {"score": {"name": "global", "objective": "global_counter"}, "color": "gray"}, {"text": " ticks", "color": "gray"}]