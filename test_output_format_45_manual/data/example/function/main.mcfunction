counter = 0
health = 15
execute if {"score":{"name":"@s","objective":"health"}} < 10 run function example:example_main_if_0
execute unless {"score":{"name":"@s","objective":"health"}} < 10 run function example:example_main_else_1
function example:example_main_if_end_0
execute if {"score":{"name":"@s","objective":"counter"}} < 5 run function example:example_main_while_0
function example:example_main_while_end_0
execute as @a run function example:main_for_0