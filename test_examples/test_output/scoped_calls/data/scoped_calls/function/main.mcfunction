execute unless entity @e[type=armor_stand,tag=mdl_server,limit=1] run summon armor_stand ~ 320 ~ {Tags:["mdl_server"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b}
tellraw @a [{"text":"Starting scoped function demo . . ."}]
function scoped_calls:scoped_calls:increment_player<@s>
function scoped_calls:scoped_calls:increment_global<global>
function scoped_calls:scoped_calls:show_scores<@a>