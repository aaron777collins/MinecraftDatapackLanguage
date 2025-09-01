say say
say "Testing complex if conditions"
execute score $playerScore$ @s > 100 && $playerHealth$ > 10 @s run function comprehensive_control_test:test_complex_if_if_2
execute score $teamScore$ @s > 50 || $globalTimer$ > 200 @s run function comprehensive_control_test:test_complex_if_if_3
execute score $counter$ @s = 0 && $flag$ == 1 @s run function comprehensive_control_test:test_complex_if_if_4
execute score $playerScore$ @s > = 100 && $playerHealth$ >= 15 && $globalTimer$ < 300 @s run function comprehensive_control_test:test_complex_if_if_5
say say
say "Complex if conditions complete"