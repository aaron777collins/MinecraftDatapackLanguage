say say
say "Testing basic if statements"
execute score $counter$ @s matches 6.. run function comprehensive_control_test:test_basic_if_if_2
execute score $playerHealth$ @s matches ..9 run function comprehensive_control_test:test_basic_if_if_3
execute score $playerScore$ @s > = 100 @s run function comprehensive_control_test:test_basic_if_if_4
say say
say "Basic if statements complete"