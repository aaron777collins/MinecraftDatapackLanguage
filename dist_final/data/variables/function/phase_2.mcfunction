execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Phase 2: Advanced features!"}]
effect give @a minecraft:glowing 5 1 true
particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
tellraw @a [{"text":"Special effects applied!"}]
tellraw @a {"text":"Final Score: ","color":"gold"}
tellraw @a {"score": {"name":"@s","objective":"playerScore"},"color":"yellow"}