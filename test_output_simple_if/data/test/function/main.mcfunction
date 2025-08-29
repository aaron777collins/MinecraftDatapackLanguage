health = 15
execute if {"score":{"name":"@s","objective":"health"}} < 10 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"health"}} < 10 run function test:test_main_else_1
function test:test_main_if_end_0