say say
say "Testing control structures with different scopes"
execute score $playerScore$ @s > 100 && $globalTimer$ < 200 @s run function comprehensive_control_test:test_control_with_scopes_if_5
say say
say "Control with scopes complete"