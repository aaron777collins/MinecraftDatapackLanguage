say say
say "Testing control structures with complex expressions"
execute score ($playerScore$ + $counter$) @s matches 101.. run function comprehensive_control_test:test_control_complex_expressions_if_2
execute score $playerScore$ @s > 50 && ($playerHealth$ + $counter$) > 25 @s run function comprehensive_control_test:test_control_complex_expressions_if_4
say say
say "Control complex expressions complete"