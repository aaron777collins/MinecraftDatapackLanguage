say say
say "Testing if-else statements"
execute score $health$ @s matches ..9 run function comprehensive_control_test:test_if_else_if_2
execute unless score $health$ @s matches ..9 run function comprehensive_control_test:test_if_else_else_2
execute score $playerScore$ @s matches 51.. run function comprehensive_control_test:test_if_else_if_3
execute unless score $playerScore$ @s matches 51.. run function comprehensive_control_test:test_if_else_else_3
execute score $globalTimer$ @s matches 101.. run function comprehensive_control_test:test_if_else_if_4
execute unless score $globalTimer$ @s matches 101.. run function comprehensive_control_test:test_if_else_else_4
say say
say "If-else statements complete"