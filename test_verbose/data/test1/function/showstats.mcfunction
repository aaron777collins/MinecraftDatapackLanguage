tellraw @a {"text":"=== Player Statistics ===","color":"gold","bold": true}
tellraw @a [{"text": "Global Hello Count: ", "color": "gold"}, {"score": {"name": "@e[type=armor_stand,tag=mdl_server,limit=1]", "objective": "global_hello_count"}, "color": "gold"}]
execute as @a run function test1:showplayerstats