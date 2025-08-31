execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Global counter: $global_counter<global>$"}]
tellraw @a [{"text":"Global timer: $global_timer<global>$"}]
tellraw @a [{"text":"My score: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"player_score"}}]
tellraw @a [{"text":"My level: "},{"score":{"name":"@e[type=armor_stand,tag=mdl_server,limit=1]","objective":"player_level"}}]
tellraw @a [{"text":"My score (explicit): $player_score<@s>$"}]
tellraw @a [{"text":"My level (explicit): $player_level<@s>$"}]
tellraw @a [{"text":"Red team score: $red_team_score<@a[team=red]>$"}]
tellraw @a [{"text":"Blue team score: $blue_team_score<@a[team=blue]>$"}]
tellraw @a [{"text":"All players counter: $all_players_counter<@a>$"}]
global_counter < global > = global_counter < global > + 1
global_timer < global > = global_timer < global > + 1
player_score < @s > = player_score < @s > + 5
player_level < @s > = player_level < @s > + 1
red_team_score < @a [team = red] > = red_team_score < @a [team = red] > + 2
blue_team_score < @a [team = blue] > = blue_team_score < @a [team = blue] > + 3
all_players_counter < @a > = all_players_counter < @a > + 1
execute if $global_counter<global>$ > 5 run function test_scoped:test_scoped_access_and_assignment_if_16
function test_scoped:test_scoped_access_and_assignment_if_end_16
execute if $player_score<@s>$ >= 10 run function test_scoped:test_scoped_access_and_assignment_if_17
function test_scoped:test_scoped_access_and_assignment_if_end_17
execute if $red_team_score<@a[team=red]>$ > $blue_team_score<@a[team=blue]>$ run function test_scoped:test_scoped_access_and_assignment_if_18
function test_scoped:test_scoped_access_and_assignment_if_end_18