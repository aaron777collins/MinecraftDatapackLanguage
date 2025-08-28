scoreboard objectives add player_level dummy
scoreboard players set @s player_level 1
scoreboard objectives add player_experience dummy
scoreboard players set @s player_experience 0
data modify storage mdl:variables player_class set value ""
data modify storage mdl:variables player_class set value "warrior"
data modify storage mdl:variables player_inventory set value []
data modify storage mdl:variables player_inventory append value "wooden_sword"
data modify storage mdl:variables player_inventory append value "leather_armor"
data modify storage mdl:variables completed_quests set value []
