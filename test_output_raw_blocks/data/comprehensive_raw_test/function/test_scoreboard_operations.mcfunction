say say
say "Testing scoreboard operations"
scoreboard objectives add player_score dummy "Player Score"
    scoreboard objectives add global_timer dummy "Global Timer"
    scoreboard players set @a player_score 0
    scoreboard players add @a player_score 10
    scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] global_timer 0 say "Scoreboard operations complete"