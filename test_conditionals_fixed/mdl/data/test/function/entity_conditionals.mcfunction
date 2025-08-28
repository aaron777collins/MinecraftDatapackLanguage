execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run say Diamond sword detected!
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 10 1
execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:glowing 10 0
execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run say No player found
