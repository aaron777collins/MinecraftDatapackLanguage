data modify storage mdl:variables available_quests set value []
data modify storage mdl:variables available_quests append value "kill_zombies"
data modify storage mdl:variables available_quests append value "collect_iron"
data modify storage mdl:variables available_quests append value "explore_cave"
scoreboard objectives add quest_index dummy
scoreboard players set @s quest_index 0
execute if score @s quest_index < available_quests.length run data modify storage mdl:variables current_quest set value ""
execute if score @s quest_index < available_quests.length run data modify storage mdl:variables current_quest set value "ListAccessExpression(list_name='available_quests', index=VariableExpression(name='quest_index'))"
execute if score @s quest_index < available_quests.length run scoreboard objectives add is_completed dummy
execute if score @s quest_index < available_quests.length run scoreboard players set @s is_completed 0
execute if score @s quest_index < available_quests.length run scoreboard objectives add completed_index dummy
execute if score @s quest_index < available_quests.length run scoreboard players set @s completed_index 0
execute if score @s quest_index < available_quests.length run execute if score @s completed_index < completed_quests.length run execute if score @s completed_quests[completed_index] == current_quest run scoreboard players set @s is_completed 1
execute if score @s quest_index < available_quests.length run execute if score @s completed_index < completed_quests.length run scoreboard players add @s completed_index 1
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'kill_zombies' run execute if entity @e[type=minecraft:zombie,distance=..10] run say Zombie quest completed!
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'kill_zombies' run execute if entity @e[type=minecraft:zombie,distance=..10] run data modify storage mdl:variables completed_quests append value "kill_zombies"
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'kill_zombies' run execute if entity @e[type=minecraft:zombie,distance=..10] run function adventure:gain_experience
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'collect_iron' unless score @s current_quest == 'kill_zombies' run execute if entity @s[type=minecraft:player,nbt={Inventory:[{id:'minecraft:iron_ingot'}]}] run say Iron collection quest completed!
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'collect_iron' unless score @s current_quest == 'kill_zombies' run execute if entity @s[type=minecraft:player,nbt={Inventory:[{id:'minecraft:iron_ingot'}]}] run data modify storage mdl:variables completed_quests append value "collect_iron"
execute if score @s quest_index < available_quests.length run execute if score @s is_completed == 0 run execute if score @s current_quest == 'collect_iron' unless score @s current_quest == 'kill_zombies' run execute if entity @s[type=minecraft:player,nbt={Inventory:[{id:'minecraft:iron_ingot'}]}] run function adventure:gain_experience
execute if score @s quest_index < available_quests.length run scoreboard players add @s quest_index 1
