execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run say Diamond sword combat detected
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 10 1
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:glowing 10 0
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run execute if entity @e[type=minecraft:zombie,distance=..5] run say Enemy nearby - combat mode activated
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run execute if entity @e[type=minecraft:zombie,distance=..5] run effect give @s minecraft:resistance 10 0
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:bow'}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run say Bow combat detected
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:bow'}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:speed 10 1
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:bow'}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:jump_boost 10 0
