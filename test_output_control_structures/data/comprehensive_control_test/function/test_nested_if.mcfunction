say say
say "Testing nested if statements"
execute score $playerScore$ @s matches 51.. run function comprehensive_control_test:test_nested_if_if_2
execute unless score $playerScore$ @s matches 51.. run function comprehensive_control_test:test_nested_if_else_2
execute score $counter$ @s matches 1.. run function comprehensive_control_test:test_nested_if_if_3
execute unless score $counter$ @s matches 1.. run function comprehensive_control_test:test_nested_if_else_3
say say
say "Nested if statements complete"