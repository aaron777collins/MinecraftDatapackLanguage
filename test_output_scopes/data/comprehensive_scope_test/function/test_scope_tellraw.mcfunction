say say
say "Testing scope tellraw"
tellraw @ a {"text":"Player Score: ","color":"green"}
tellraw @ a {"text": "${playerScore}", "color": "yellow"}
tellraw @ a {"text":"Global Timer: ","color":"blue"}
tellraw @ a {"text": "${globalTimer}", "color": "cyan"}
tellraw @ a {"text":"Red Team Score: ","color":"red"}
tellraw @ a {"text": "${redTeamScore}", "color": "gold"}
tellraw @ a {"text":"All Players Score: ","color":"purple"}
tellraw @ a {"text": "${allPlayersScore}", "color": "light_purple"}
say say
say "Scope tellraw test complete"