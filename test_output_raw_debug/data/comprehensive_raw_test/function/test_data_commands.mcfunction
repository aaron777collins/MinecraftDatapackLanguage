say "Testing data commands"
data modify entity @e[type=armor_stand,limit=1] CustomName set value {"text":"Test Armor Stand","color":"gold"}
    data modify entity @s CustomName set value "Test Player"
    data get entity @s Health
say "Data commands complete"