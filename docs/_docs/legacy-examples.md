# Legacy MDL Examples (v9 and below)

> **⚠️ Legacy Format Notice**: These examples use the **old MDL language format** (v9 and below). For new projects, see the [Examples](examples.md) page for the modern JavaScript-style MDL format (v10+).

This page contains working examples of the legacy MDL format for reference and learning purposes.

## Basic Examples

### Hello World

```mdl
pack "Hello World" description "Simple hello world example" pack_format 48

namespace "hello"

function "greet":
    say Hello, World!
    tellraw @a {"text":"Welcome to MDL!","color":"green"}

on_tick "hello:greet"
```

### Simple Counter

```mdl
pack "Counter" description "Simple counter example" pack_format 48

namespace "counter"

function "init":
    scoreboard objectives add counter dummy
    scoreboard players set @a counter 0

function "tick":
    scoreboard players add @a counter 1
    execute as @a if score @s counter matches 10 run function counter:reset

function "reset":
    scoreboard players set @s counter 0
    say Counter reset!

on_load "counter:init"
on_tick "counter:tick"
```

### Player Effects

```mdl
pack "Player Effects" description "Give effects to players" pack_format 48

namespace "effects"

function "tick":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            effect give @s minecraft:speed 10 1
            effect give @s minecraft:night_vision 10 0
        else:
            effect give @s minecraft:slowness 10 0

on_tick "effects:tick"
```

## Control Flow Examples

### Conditional Effects

```mdl
pack "Conditional Effects" description "Different effects based on conditions" pack_format 48

namespace "conditional"

function "tick":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            if "entity @s[gamemode=survival]":
                effect give @s minecraft:haste 10 0
            else if "entity @s[gamemode=creative]":
                effect give @s minecraft:fly 10 0
            else:
                effect give @s minecraft:jump_boost 10 0

on_tick "conditional:tick"
```

### Weapon Effects

```mdl
pack "Weapon Effects" description "Effects based on held items" pack_format 48

namespace "weapons"

function "tick":
    for player in @a:
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
            effect give @s minecraft:strength 10 1
            particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.5 0.5 0.1 10
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:golden_sword'}}]":
            effect give @s minecraft:speed 10 1
            particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.05 5
        else if "entity @s[nbt={SelectedItem:{id:'minecraft:netherite_sword'}}]":
            effect give @s minecraft:resistance 10 1
            particle minecraft:flame ~ ~1 ~ 0.4 0.4 0.4 0.1 8

on_tick "weapons:tick"
```

### Loop Examples

```mdl
pack "Loop Examples" description "Demonstrating loops" pack_format 48

namespace "loops"

function "countdown":
    scoreboard players set @s timer 10
    while "score @s timer matches 1..":
        say Countdown: @s timer
        scoreboard players remove @s timer 1
        execute unless score @s timer matches 0 run function loops:wait

function "wait":
    schedule function loops:countdown 20t

function "spawn_particles":
    for entity in @e[type=minecraft:zombie]:
        particle minecraft:smoke ~ ~ ~ 0.5 0.5 0.5 0.1 5

on_tick "loops:spawn_particles"
```

## Multi-file Examples

### Core Module

```mdl
# core.mdl
pack "Multi-file Example" description "Multi-file project" pack_format 48

namespace "core"

function "init":
    say Core module initialized
    scoreboard objectives add health dummy
    scoreboard objectives add mana dummy

function "tick":
    for player in @a:
        scoreboard players set @s health 20
        scoreboard players set @s mana 100

on_load "core:init"
on_tick "core:tick"
```

### Combat Module

```mdl
# combat.mdl
namespace "combat"

function "attack":
    for player in @a:
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
            execute as @s at @s if entity @e[type=minecraft:zombie,distance=..3] run function combat:damage

function "damage":
    effect give @e[type=minecraft:zombie,distance=..3] minecraft:instant_damage 1 1
    particle minecraft:crit ~ ~ ~ 0.5 0.5 0.5 0.1 10

on_tick "combat:attack"
```

### UI Module

```mdl
# ui.mdl
namespace "ui"

function "show_hud":
    for player in @a:
        tellraw @s {"text":"Health: ","color":"red","extra":[{"score":{"name":"@s","objective":"health"},"color":"white"}]}
        tellraw @s {"text":"Mana: ","color":"blue","extra":[{"score":{"name":"@s","objective":"mana"},"color":"white"}]}

on_tick "ui:show_hud"
```

## Advanced Examples

### Teleport System

```mdl
pack "Teleport System" description "Advanced teleportation system" pack_format 48

namespace "teleport"

function "init":
    scoreboard objectives add teleport_cooldown dummy
    scoreboard objectives add teleport_destination dummy

function "set_destination":
    for player in @a:
        if "entity @s[scores={teleport_destination=1}]":
            execute store result score @s temp run data get entity @s Pos[0]
            execute store result score @s temp2 run data get entity @s Pos[2]
            scoreboard players set @s teleport_cooldown 100

function "teleport":
    for player in @a:
        if "entity @s[scores={teleport_cooldown=1..}]":
            execute at @s run tp @s ~ ~ ~
            scoreboard players remove @s teleport_cooldown 1

on_load "teleport:init"
on_tick "teleport:set_destination"
on_tick "teleport:teleport"
```

### Inventory Management

```mdl
pack "Inventory Manager" description "Advanced inventory management" pack_format 48

namespace "inventory"

function "check_inventory":
    for player in @a:
        if "entity @s[nbt={Inventory:[{Slot:0b,id:'minecraft:diamond'}]}]":
            say Player has diamond in first slot
            clear @s minecraft:diamond 1
            give @s minecraft:emerald 1
        else if "entity @s[nbt={Inventory:[{Slot:1b,id:'minecraft:golden_apple'}]}]":
            say Player has golden apple in second slot
            effect give @s minecraft:absorption 600 0

on_tick "inventory:check_inventory"
```

### Weather System

```mdl
pack "Weather System" description "Dynamic weather system" pack_format 48

namespace "weather"

function "init":
    scoreboard objectives add weather_timer dummy
    scoreboard objectives add weather_type dummy
    scoreboard players set @a weather_timer 1200
    scoreboard players set @a weather_type 0

function "tick":
    scoreboard players remove @a weather_timer 1
    for player in @a:
        if "entity @s[scores={weather_timer=0}]":
            function weather:change_weather

function "change_weather":
    scoreboard players add @s weather_type 1
    if "entity @s[scores={weather_type=1}]":
        weather clear
        say Weather cleared
    else if "entity @s[scores={weather_type=2}]":
        weather rain
        say Rain started
    else if "entity @s[scores={weather_type=3}]":
        weather thunder
        say Thunder started
        scoreboard players set @s weather_type 0
    scoreboard players set @s weather_timer 1200

on_load "weather:init"
on_tick "weather:tick"
```

## Tag Examples

### Function Tags

```mdl
pack "Tag Examples" description "Demonstrating tag usage" pack_format 48

namespace "tags"

function "tick_function":
    say Tick function running

function "load_function":
    say Load function running

tag function "minecraft:tick":
    add "tags:tick_function"

tag function "minecraft:load":
    add "tags:load_function"
```

### Item Tags

```mdl
pack "Item Tags" description "Item tag examples" pack_format 48

namespace "items"

tag item "example:swords":
    add "minecraft:wooden_sword"
    add "minecraft:stone_sword"
    add "minecraft:iron_sword"
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag item "example:armor":
    add "minecraft:leather_helmet"
    add "minecraft:leather_chestplate"
    add "minecraft:leather_leggings"
    add "minecraft:leather_boots"
```

### Block Tags

```mdl
pack "Block Tags" description "Block tag examples" pack_format 48

namespace "blocks"

tag block "example:ores":
    add "minecraft:coal_ore"
    add "minecraft:iron_ore"
    add "minecraft:gold_ore"
    add "minecraft:diamond_ore"
    add "minecraft:emerald_ore"

tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"
    add "minecraft:white_stained_glass"
```

## Game Mechanics Examples

### Custom Crafting

```mdl
pack "Custom Crafting" description "Custom crafting system" pack_format 48

namespace "crafting"

function "check_crafting":
    for player in @a:
        if "entity @s[nbt={Inventory:[{Slot:0b,id:'minecraft:diamond'},{Slot:1b,id:'minecraft:diamond'},{Slot:2b,id:'minecraft:diamond'},{Slot:3b,id:'minecraft:diamond'},{Slot:4b,id:'minecraft:diamond'},{Slot:5b,id:'minecraft:diamond'},{Slot:6b,id:'minecraft:diamond'},{Slot:7b,id:'minecraft:diamond'},{Slot:8b,id:'minecraft:diamond'}]}]":
            clear @s minecraft:diamond 9
            give @s minecraft:netherite_ingot 1
            say Custom crafting successful!

on_tick "crafting:check_crafting"
```

### Mob AI

```mdl
pack "Mob AI" description "Custom mob behavior" pack_format 48

namespace "mob_ai"

function "zombie_ai":
    for entity in @e[type=minecraft:zombie]:
        if "entity @s[distance=..10]":
            execute as @s at @s run tp @s ~ ~ ~ facing @p
            if "entity @s[distance=..2]":
                effect give @p minecraft:poison 60 0

function "creeper_ai":
    for entity in @e[type=minecraft:creeper]:
        if "entity @s[distance=..5]":
            effect give @s minecraft:speed 20 1
            particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.1 3

on_tick "mob_ai:zombie_ai"
on_tick "mob_ai:creeper_ai"
```

## Performance Examples

### Optimized Loops

```mdl
pack "Performance" description "Performance optimization examples" pack_format 48

namespace "performance"

function "efficient_tick":
    # Only process nearby entities
    for entity in @e[type=minecraft:zombie,distance=..32]:
        if "entity @s[type=minecraft:zombie]":
            effect give @s minecraft:glowing 10 0

function "batch_processing":
    # Process players in batches
    execute as @a[limit=5] run function performance:process_player

function "process_player":
    effect give @s minecraft:speed 10 0

on_tick "performance:efficient_tick"
schedule function performance:batch_processing 10t
```

## Building and Testing

To build these legacy examples:

```bash
# Build a single file
mdl build --mdl example.mdl -o dist --pack-format 48

# Build multi-file project
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist --pack-format 48

# Check syntax
mdl check example.mdl --pack-format 48
```

## Migration Notes

These examples demonstrate the legacy MDL format. To migrate them to the new JavaScript-style format (v10+):

1. Change pack format from 48 to 82
2. Convert comments from `#` to `//`
3. Add curly braces `{}` around code blocks
4. Add semicolons `;` after statements
5. Update function declarations and control flow

See the [Migration Guide](migration-guide.md) for detailed instructions.

---

**Previous**: [Legacy MDL Language Reference](legacy-mdl-language.md) | **Next**: [Migration Guide](migration-guide.md)
