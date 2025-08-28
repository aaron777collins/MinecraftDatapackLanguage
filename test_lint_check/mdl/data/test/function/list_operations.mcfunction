data modify storage mdl:variables weapons set value []
data modify storage mdl:variables weapons append value "diamond_sword"
data modify storage mdl:variables weapons append value "golden_sword"
data modify storage mdl:variables weapons append value "bow"
data modify storage mdl:variables armor set value []
data modify storage mdl:variables armor append value "diamond_helmet"
data modify storage mdl:variables armor append value "diamond_chestplate"
data modify storage mdl:variables weapons append value "crossbow"
data modify storage mdl:variables armor append value "diamond_leggings"
# Insert 'netherite_sword' at index 1 in weapons
data modify storage mdl:variables weapons insert 1 value "netherite_sword"
# Insert 'netherite_helmet' at index 0 in armor
data modify storage mdl:variables armor insert 0 value "netherite_helmet"
# Access element at index 0 from weapons
data modify storage mdl:temp element set from storage mdl:variables weapons[0]
data modify storage mdl:variables primary_weapon set from storage mdl:temp element
scoreboard objectives add weapon_count dummy
# Get length of weapons
execute store result score @s weapon_count run data get storage mdl:variables weapons
scoreboard objectives add armor_count dummy
# Get length of armor
execute store result score @s armor_count run data get storage mdl:variables armor
# Remove 'golden_sword' from weapons
execute store result storage mdl:temp index int 1 run data get storage mdl:variables weapons
execute if data storage mdl:variables weapons[{value:"golden_sword"}] run data remove storage mdl:variables weapons[{value:"golden_sword"}]
# Remove 'diamond_helmet' from armor
execute store result storage mdl:temp index int 1 run data get storage mdl:variables armor
execute if data storage mdl:variables armor[{value:"diamond_helmet"}] run data remove storage mdl:variables armor[{value:"diamond_helmet"}]
# Pop last element from weapons
execute store result storage mdl:temp last_index int 1 run data get storage mdl:variables weapons
execute if data storage mdl:variables weapons run data remove storage mdl:variables weapons[storage mdl:temp last_index]
# Pop last element from armor
execute store result storage mdl:temp last_index int 1 run data get storage mdl:variables armor
execute if data storage mdl:variables armor run data remove storage mdl:variables armor[storage mdl:temp last_index]
say List operations complete
tellraw @s {"text":"Weapon count: ", "extra":[{"score":{"name":"weapon_count","objective":"weapon_count"}}]}
tellraw @s {"text":"Armor count: ", "extra":[{"score":{"name":"armor_count","objective":"armor_count"}}]}
tellraw @s {"text":"Primary weapon: ", "extra":[{"nbt":"primary_weapon","storage":"mdl:variables"}]}
