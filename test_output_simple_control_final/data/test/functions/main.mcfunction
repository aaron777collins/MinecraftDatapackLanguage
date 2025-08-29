counter = 5
health = 15
execute if {"score":{"name":"@s","objective":"health"}} < 10 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"health"}} < 10 run function test:test_main_else_1
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"counter"}} > 3 run function test:test_main_if_0
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"counter"}} < 10 run function test:test_main_while_0
function test:test_main_while_end_0
execute as @a run function test:main_for_0