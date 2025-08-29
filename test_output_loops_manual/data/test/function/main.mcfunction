counter = 0
execute if {"score":{"name":"@s","objective":"counter"}} < 5 run function test:test_main_while_0
function test:test_main_while_end_0
counter = 0
execute if {"score":{"name":"@s","objective":"counter"}} < {"score":{"name":"@s","objective":"max_count"}} run function test:test_main_while_0
function test:test_main_while_end_0
execute as @a run function test:main_for_0
execute as @e[type=zombie] run function test:main_for_0
counter = 0
execute if {"score":{"name":"@s","objective":"counter"}} < 3 run function test:test_main_while_0
function test:test_main_while_end_0