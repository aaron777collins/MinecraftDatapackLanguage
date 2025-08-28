function adventure:check_combat
function adventure:quest_system
function adventure:inventory_management
function adventure:class_specialization
scoreboard objectives add save_counter dummy
scoreboard players set @s save_counter 0
scoreboard players add @s save_counter 1
execute if score @s save_counter >= 100 run function adventure:save_progress
execute if score @s save_counter >= 100 run scoreboard players set @s save_counter 0
