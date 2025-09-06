# Function: hello_world:greet_player

tellraw @a {"text":"Welcome, player! You are visitor number $globalCounter$"}
tellraw @a {"text":"Hello, Steve! Visits: ","extra":[{"score":{"name":"@a","objective":"globalCounter"}}]}
tellraw @a {"text":"Hello, Player! Visits: ","extra":[{"score":{"name":"@a","objective":"globalCounter"}}]}