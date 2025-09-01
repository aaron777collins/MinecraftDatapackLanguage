tellraw @ a {"score": {"name":"@s","objective":"playerScore"},"color":"yellow"}
tellraw @ a [{"text": "Your score: ", "color": "white"}, {"score": {"name": "@s", "objective": "playerScore"}, "color": "gold"}]
tellraw @ a [{"score": {"name": "@s", "objective": "playerScore"}, "color": "green"}, {"text": " points", "color": "gray"}]
say say
say "Tellraw score complete"