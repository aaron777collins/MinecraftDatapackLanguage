execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Starting raw command demo..."}]
# This is a raw command block
# These commands are inserted directly without processing
effect give @a minecraft:night_vision 10 1 true
effect give @a minecraft:jump_boost 10 2 true
tellraw @a [{"text":"Raw commands executed!"}]