counter = 42
health = 15
level = 5
experience = 100
say "Counter: {"score":{"name":"@s","objective":"counter"}}"
say "Health: {"score":{"name":"@s","objective":"health"}}"
say "Level: {"score":{"name":"@s","objective":"level"}}"
say "Experience: {"score":{"name":"@s","objective":"experience"}}"
tellraw @ s [ { "text" : "Counter: " } , { "score" : { "name" : "@s" , "objective" : "counter" } } ]
tellraw @ s [ { "text" : "Health: " } , { "score" : { "name" : "@s" , "objective" : "health" } } ]
counter = counter + 1
health = health - 5
level = level * 2
experience = experience / 2
say "Updated Counter: {"score":{"name":"@s","objective":"counter"}}"
say "Updated Health: {"score":{"name":"@s","objective":"health"}}"
say "Updated Level: {"score":{"name":"@s","objective":"level"}}"
say "Updated Experience: {"score":{"name":"@s","objective":"experience"}}"