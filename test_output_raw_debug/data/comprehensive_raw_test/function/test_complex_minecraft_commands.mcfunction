say "Testing complex Minecraft commands"
summon armor_stand ~ ~ ~ {Tags:["test_stand"],CustomName:'{"text":"Test Stand"}',Invisible:1b}
    tp @e[type=armor_stand,tag=test_stand] ~ ~5 ~
    kill @e[type=armor_stand,tag=test_stand]
say "Complex Minecraft commands complete"