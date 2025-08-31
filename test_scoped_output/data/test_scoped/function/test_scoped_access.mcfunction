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
execute if $global_counter<global>$ > 5 run function test_scoped:test_scoped_access_if_9
function test_scoped:test_scoped_access_if_end_9
execute if $player_score<@s>$ >= 10 run function test_scoped:test_scoped_access_if_10
function test_scoped:test_scoped_access_if_end_10
execute if $red_team_score<@a[team=red]>$ > $blue_team_score<@a[team=blue]>$ run function test_scoped:test_scoped_access_if_11
function test_scoped:test_scoped_access_if_end_11