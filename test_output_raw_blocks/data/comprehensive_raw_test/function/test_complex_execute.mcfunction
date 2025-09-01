say say
say "Testing complex execute commands"
execute as @a[team=red] at @s run particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 100
    execute as @a[team=blue] at @s run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
    execute as @a[tag=admin] at @s run effect give @s minecraft:glowing 10 1 true say "Complex execute commands complete"