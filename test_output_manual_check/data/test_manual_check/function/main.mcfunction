player_count = 0
game_timer = 0
player_score = 100
execute if {"score":{"name":"@s","objective":"player_score"}} > 50 run function test_manual_check:test_manual_check_main_if_0
execute unless {"score":{"name":"@s","objective":"player_score"}} > 50 run function test_manual_check:test_manual_check_main_else_1
function test_manual_check:test_manual_check_main_if_end_0
execute if {"score":{"name":"@s","objective":"game_timer"}} < 10 run function test_manual_check:test_manual_check_main_while_0
function test_manual_check:test_manual_check_main_while_end_0
execute as @a run function test_manual_check:main_for_0
execute if {"score":{"name":"@s","objective":"player_count"}} > 0 run function test_manual_check:test_manual_check_main_if_0
function test_manual_check:test_manual_check_main_if_end_0