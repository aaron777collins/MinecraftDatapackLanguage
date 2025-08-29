scoreboard players set @s count 10
execute if {"score":{"name":"@s","objective":"count"}} > 0 run function test:test_countdown_while_0
function test:test_countdown_while_end_0
say "Blast off!"