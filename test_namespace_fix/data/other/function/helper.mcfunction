say "Calculation result: $result$"
tellraw @a [{"text":"Score: "}, {"score": {"name":"@a","objective":"player_score"}}]
