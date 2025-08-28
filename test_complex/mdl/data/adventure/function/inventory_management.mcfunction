scoreboard objectives add inventory_size dummy
scoreboard players set @s inventory_size 0
data modify storage mdl:variables status_message set value ""
data modify storage mdl:variables status_message set value "Inventory: "
execute if score @s inventory_size > 10 run scoreboard players add @s status_message  (Full!)
execute if score @s inventory_size > 10 run tellraw @s {"text":status_message,"color":"red"}
execute if score @s inventory_size > 5 unless score @s inventory_size > 10 run scoreboard players add @s status_message  (Getting full)
execute if score @s inventory_size > 5 unless score @s inventory_size > 10 run tellraw @s {"text":status_message,"color":"yellow"}
execute unless score @s inventory_size > 10 unless score @s inventory_size > 5 run tellraw @s {"text":status_message,"color":"green"}
execute if score @s inventory_size > 8 run say Auto-organizing inventory
execute if score @s inventory_size > 8 run scoreboard objectives add i dummy
execute if score @s inventory_size > 8 run scoreboard players set @s i 0
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run data modify storage mdl:variables current_item set value ""
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run data modify storage mdl:variables current_item set value "ListAccessExpression(list_name='player_inventory', index=VariableExpression(name='i'))"
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run scoreboard objectives add j dummy
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run scoreboard players set @s j 0
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run execute if score @s j < player_inventory.length run execute if score @s player_inventory[j] == current_item run scoreboard players remove @s j 1
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run execute if score @s j < player_inventory.length run scoreboard players add @s j 1
execute if score @s inventory_size > 8 run execute if score @s i < player_inventory.length run scoreboard players add @s i 1
