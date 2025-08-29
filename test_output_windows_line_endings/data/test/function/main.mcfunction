execute if {"score":{"name":"@s","objective":"health"}} > 10 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"health"}} > 10 if {"score":{"name":"@s","objective":"health"}} > 5 run function test:test_main_elif_1_0
execute unless {"score":{"name":"@s","objective":"health"}} > 10 run function test:test_main_else_2
function test:test_main_if_end_0