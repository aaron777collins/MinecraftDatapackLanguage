say say
say "Testing control structures with tellraw"
execute score $playerScore$ @s matches 101.. run function comprehensive_control_test:test_control_with_tellraw_if_2
execute unless score $playerScore$ @s matches 101.. run function comprehensive_control_test:test_control_with_tellraw_else_2
execute score $playerHealth$ @s matches ..9 run function comprehensive_control_test:test_control_with_tellraw_if_4
say say
say "Control with tellraw complete"