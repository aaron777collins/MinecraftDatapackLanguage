scoreboard players set @s result 0
result = 5 + 3
say "Calculation result: {"score":{"name":"@s","objective":"result"}}"
tellraw @ s [ { "text" : "Score: " } , { "score" : { "name" : "@s" , "objective" : "player_score" } } ]