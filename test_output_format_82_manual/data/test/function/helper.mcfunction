scoreboard players set @s result 0
result = 5 + 3
say "Result: {"score":{"name":"@s","objective":"result"}}"
tellraw @ s [ { "text" : "Health: " } , { "score" : { "name" : "@s" , "objective" : "health" } } ]