say say
say "Testing raw blocks with scope context"
scoreboard players set @s mdl_player_score 100
    scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] mdl_global_timer 0
    scoreboard players set @a[team=red] mdl_red_team_score 50 say "Raw with scope context test complete"