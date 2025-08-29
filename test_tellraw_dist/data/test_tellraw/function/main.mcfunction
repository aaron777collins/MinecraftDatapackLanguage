scoreboard players set @s player_score 100
tellraw @s [{"text":"Score: "}, {"score": {"name":"@s","objective":"player_score"}}]
say"Calculation result: $player_score$"