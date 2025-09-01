say "Testing effects and sounds"
effect give @a minecraft:speed 10 1
    effect give @a minecraft:glowing 5 1 true
    effect give @a minecraft:night_vision 20 1
    playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1
    playsound minecraft:block.note_block.pling player @a ~ ~ ~ 0.5 1
say "Effects and sounds complete"