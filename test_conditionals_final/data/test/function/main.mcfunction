player_level = 15
player_health = 8
experience = 75
execute if {"score":{"name":"@s","objective":"player_level"}} > 10 run function test:test_main_if_0
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"player_health"}} < 10 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"player_health"}} < 10 run function test:test_main_else_1
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"player_level"}} = 15 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"player_level"}} = 15 run function test:test_main_else_1
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"player_level"}} = 20 run function test:test_main_if_0
execute unless {"score":{"name":"@s","objective":"player_level"}} = 20 if {"score":{"name":"@s","objective":"player_level"}} = 15 run function test:test_main_elif_1_0
execute unless {"score":{"name":"@s","objective":"player_level"}} = 20 if {"score":{"name":"@s","objective":"player_level"}} = 10 run function test:test_main_elif_2_1
execute unless {"score":{"name":"@s","objective":"player_level"}} = 20 run function test:test_main_else_3
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"player_level"}} > {"score":{"name":"@s","objective":"min_level"}} run function test:test_main_if_0
function test:test_main_if_end_0
execute if {"score":{"name":"@s","objective":"experience"}} = {"score":{"name":"@s","objective":"required_exp"}} run function test:test_main_if_0
function test:test_main_if_end_0