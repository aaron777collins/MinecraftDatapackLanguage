say [adventure:initialize_player] Initializing player
scoreboard players set @s player_level 1
scoreboard players set @s player_experience 0
data modify storage mdl:variables player_class set value "warrior"
# Clear all elements from player_inventory
data modify storage mdl:variables player_inventory set value []
data modify storage mdl:variables player_inventory append value "wooden_sword"
data modify storage mdl:variables player_inventory append value "leather_armor"
# Clear all elements from completed_quests
data modify storage mdl:variables completed_quests set value []
tellraw @s {"text":"Welcome to the Adventure Pack!","color":"gold"}
tellraw @s {"text":"You are a level " + player_level + " " + player_class,"color":"green"}
