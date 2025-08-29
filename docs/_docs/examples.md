---
layout: page
title: Examples
permalink: /docs/examples/
---

# **SIMPLIFIED** JavaScript-style MDL Examples (v10+)

This page contains complete, working examples of the **simplified** JavaScript-style MDL format that demonstrate **control structures and number variables**.

> **📚 Looking for legacy examples?** See [Legacy Examples](legacy-examples.md) for the old MDL format (v9 and below).

## Basic Examples

### Hello World

A simple datapack that displays a welcome message when loaded.

```mdl
// hello_world.mdl
pack "Hello World" description "A simple example datapack" pack_format 82;

namespace "example";

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
}

on_load "example:hello";
```

**Build and use:**
```bash
mdl build --mdl hello_world.mdl -o dist
# Copy dist/hello_world/ to your world's datapacks folder
# Run /reload in-game
```

### **Simplified** Variable System

Demonstrates the **simplified** variable system with **number variables only**.

```mdl
// variables.mdl
pack "Variable System" description "Demonstrates number variables" pack_format 82;

namespace "variables";

// Number variables only
var num player_count = 0;
var num health = 20;
var num level = 1;

function "init" {
    say Initializing variable system...;
    player_count = 0;
    health = 20;
    level = 1;
}

function "count_players" {
    player_count = 0;
    for player in @a {
        player_count = player_count + 1;
    }
    say Player count: $player_count$;
}

function "check_health" {
    if "$health$ < 10" {
        say Health is low!;
        health = health + 5;
        effect give @s minecraft:regeneration 10 1;
    } else {
        say Health is good: $health$;
    }
}

function "level_up" {
    level = level + 1;
    say Level up! New level: $level$;
    effect give @s minecraft:experience 10 0;
}

on_load "variables:init";
on_tick "variables:count_players";
on_tick "variables:check_health";
```

### Particle Effects

A datapack that creates particle effects around players with **number variables**.

```mdl
// particles.mdl
pack "Particle Effects" description "Creates particle effects around players" pack_format 82;

namespace "particles";

// Configuration variables
var num particle_count = 5;
var num effect_duration = 10;

function "tick" {
    // Create particles around all players
    for player in @a {
        say Creating particles for $player$;
        execute as @s run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 $particle_count$;
        effect give @s minecraft:glowing $effect_duration$ 0;
    }
}

function "increase_particles" {
    particle_count = particle_count + 2;
    say Increased particle count to: $particle_count$;
}

function "decrease_particles" {
    if "$particle_count$ > 1" {
        particle_count = particle_count - 1;
        say Decreased particle count to: $particle_count$;
    }
}

on_tick "particles:tick";
```

## **Simplified** Control Flow Examples

### Conditional Logic

Demonstrates **if/else if/else** statements with **number variables**.

```mdl
// conditionals.mdl
pack "Conditional Logic" description "Shows if/else if/else functionality" pack_format 82;

namespace "conditionals";

// Number variables
var num player_level = 15;
var num player_health = 8;
var num player_experience = 75;

function "check_player_status" {
    if "$player_level$ >= 10" {
        if "$player_health$ < 10" {
            say Advanced player with low health!;
            effect give @s minecraft:regeneration 10 1;
            player_health = player_health + 5;
        } else {
            say Advanced player with good health;
            effect give @s minecraft:strength 10 1;
        }
    } else if "$player_level$ >= 5" {
        say Intermediate player;
        effect give @s minecraft:speed 10 0;
    } else {
        say Beginner player;
        effect give @s minecraft:jump_boost 10 0;
    }
}

function "experience_system" {
    if "$player_experience$ >= 100" {
        player_level = player_level + 1;
        player_experience = 0;
        say Level up! New level: $player_level$;
        effect give @s minecraft:experience 10 0;
    } else if "$player_experience$ >= 50" {
        say Getting close to level up! Experience: $player_experience$;
    } else {
        say Keep going! Experience: $player_experience$;
    }
}

on_tick "conditionals:check_player_status";
on_tick "conditionals:experience_system";
```

### While Loops

Demonstrates **while loops** with **number variables**.

```mdl
// loops.mdl
pack "Loop Examples" description "Shows while and for loop functionality" pack_format 82;

namespace "loops";

// Number variables
var num counter = 5;
var num regen_count = 0;

function "countdown" {
    while "$counter$ > 0" {
        say Countdown: $counter$;
        counter = counter - 1;
        say Decremented counter;
    }
    say Countdown complete!;
    counter = 5; // Reset for next time
}

function "health_regeneration" {
    regen_count = 0;
    while "$regen_count$ < 3" {
        say Regenerating health...;
        effect give @s minecraft:regeneration 5 0;
        regen_count = regen_count + 1;
    }
    say Health regeneration complete!;
}

function "item_cleanup" {
    var num cleanup_count = 0;
    while "$cleanup_count$ < 5" {
        say Cleaning up items...;
        execute as @e[type=minecraft:item,limit=1] run kill @s;
        cleanup_count = cleanup_count + 1;
    }
    say Item cleanup complete!;
}

on_tick "loops:countdown";
on_tick "loops:health_regeneration";
on_tick "loops:item_cleanup";
```

### For Loops

Demonstrates **for loops** for entity iteration.

```mdl
// for_loops.mdl
pack "For Loop Examples" description "Shows for loop functionality" pack_format 82;

namespace "for_loops";

// Number variables
var num player_count = 0;
var num item_count = 0;

function "player_effects" {
    player_count = 0;
    for player in @a {
        say Processing player: @s;
        effect give @s minecraft:speed 10 1;
        tellraw @s {"text":"You got speed!","color":"green"};
        player_count = player_count + 1;
    }
    say Processed $player_count$ players;
}

function "item_processing" {
    item_count = 0;
    for item in @e[type=minecraft:item] {
        say Processing item: @s;
        effect give @s minecraft:glowing 5 1;
        item_count = item_count + 1;
    }
    say Processed $item_count$ items;
}

function "mob_effects" {
    for mob in @e[type=minecraft:zombie] {
        say Processing zombie: @s;
        effect give @s minecraft:slowness 10 1;
    }
    
    for mob in @e[type=minecraft:skeleton] {
        say Processing skeleton: @s;
        effect give @s minecraft:weakness 10 1;
    }
}

on_tick "for_loops:player_effects";
on_tick "for_loops:item_processing";
on_tick "for_loops:mob_effects";
```

## Advanced Examples

### **Simplified** Game System

A complete game system using **number variables and control structures**.

```mdl
// game_system.mdl
pack "Game System" description "Complete game system example" pack_format 82;

namespace "game";

// Game state variables
var num player_score = 0;
var num player_lives = 3;
var num game_level = 1;
var num enemy_count = 0;

function "init_game" {
    say Initializing game system...;
    player_score = 0;
    player_lives = 3;
    game_level = 1;
    enemy_count = 0;
    tellraw @a {"text":"Game system loaded!","color":"green"};
}

function "update_game" {
    // Count enemies
    enemy_count = 0;
    for enemy in @e[type=minecraft:zombie] {
        enemy_count = enemy_count + 1;
    }
    
    // Check game state
    if "$player_lives$ <= 0" {
        say Game Over! Final score: $player_score$;
        tellraw @a {"text":"Game Over!","color":"red"};
        function game:init_game;
    } else if "$enemy_count$ == 0" {
        say Level complete!;
        game_level = game_level + 1;
        player_score = player_score + 100;
        tellraw @a {"text":"Level $game_level$ complete!","color":"gold"};
    }
    
    // Display status
    say Score: $player_score$ Lives: $player_lives$ Level: $game_level$ Enemies: $enemy_count$;
}

function "player_hit" {
    player_lives = player_lives - 1;
    say Player hit! Lives remaining: $player_lives$;
    effect give @s minecraft:resistance 5 0;
}

function "score_points" {
    player_score = player_score + 10;
    say Points scored! Total: $player_score$;
}

on_load "game:init_game";
on_tick "game:update_game";
```

### **Simplified** Multi-Namespace System

Demonstrates organizing code across multiple namespaces.

```mdl
// multi_namespace.mdl
pack "Multi-Namespace System" description "Shows namespace organization" pack_format 82;

namespace "core";

// Core variables
var num system_version = 1;
var num player_count = 0;

function "init" {
    say [core:init] Initializing system...;
    system_version = 1;
    player_count = 0;
    tellraw @a {"text":"Multi-namespace system loaded!","color":"green"};
}

function "tick" {
    say [core:tick] Core systems running...;
    player_count = 0;
    for player in @a {
        player_count = player_count + 1;
    }
    say Player count: $player_count$;
}

namespace "combat";

// Combat variables
var num weapon_damage = 10;
var num armor_bonus = 5;

function "weapon_effects" {
    say [combat:weapon_effects] Applying weapon effects...;
    execute as @a[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 1 0 true;
    weapon_damage = weapon_damage + 2;
    say Weapon damage: $weapon_damage$;
}

function "armor_bonus" {
    say [combat:armor_bonus] Checking armor bonuses...;
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] run effect give @s minecraft:resistance 1 0 true;
    armor_bonus = armor_bonus + 1;
    say Armor bonus: $armor_bonus$;
}

namespace "ui";

// UI variables
var num hud_version = 1;

function "show_hud" {
    say [ui:show_hud] Updating HUD...;
    title @a actionbar {"text":"Multi-namespace system active","color":"gold"};
    hud_version = hud_version + 1;
    say HUD version: $hud_version$;
}

function "update_ui" {
    function ui:show_hud;
    function combat:weapon_effects;
    function combat:armor_bonus;
}

// Hooks
on_load "core:init";
on_tick "core:tick";
on_tick "ui:update_ui";

// Tags
tag function "minecraft:load" {
    add "core:init";
}

tag function "minecraft:tick" {
    add "core:tick";
    add "ui:update_ui";
}
```

## **Simplified** Patterns and Best Practices

### Counter Pattern

A common pattern for counting and tracking:

```mdl
// counter_pattern.mdl
pack "Counter Pattern" description "Shows counter patterns" pack_format 82;

namespace "counter";

var num global_counter = 0;
var num player_counter = 0;

function "increment_global" {
    global_counter = global_counter + 1;
    say Global counter: $global_counter$;
}

function "reset_counters" {
    global_counter = 0;
    player_counter = 0;
    say Counters reset;
}

function "count_players" {
    player_counter = 0;
    for player in @a {
        player_counter = player_counter + 1;
    }
    say Player counter: $player_counter$;
}

on_tick "counter:increment_global";
on_tick "counter:count_players";
```

### Health Management Pattern

Managing player health with **number variables**:

```mdl
// health_pattern.mdl
pack "Health Pattern" description "Shows health management" pack_format 82;

namespace "health";

var num player_health = 20;
var num max_health = 20;
var num regeneration_rate = 1;

function "check_health" {
    if "$player_health$ < 10" {
        say Health is low! Current: $player_health$;
        effect give @s minecraft:regeneration 10 1;
    } else if "$player_health$ < $max_health$" {
        say Health is recovering. Current: $player_health$;
        player_health = player_health + $regeneration_rate$;
    } else {
        say Health is full: $player_health$;
    }
}

function "take_damage" {
    player_health = player_health - 5;
    say Took damage! Health: $player_health$;
    effect give @s minecraft:resistance 5 0;
}

function "heal_full" {
    player_health = $max_health$;
    say Fully healed! Health: $player_health$;
    effect give @s minecraft:instant_health 1 0;
}

on_tick "health:check_health";
```

### Level System Pattern

A complete level system with experience:

```mdl
// level_pattern.mdl
pack "Level Pattern" description "Shows level system" pack_format 82;

namespace "level";

var num player_level = 1;
var num experience = 0;
var num experience_needed = 100;

function "gain_experience" {
    experience = experience + 10;
    say Experience gained! Current: $experience$;
    
    if "$experience$ >= $experience_needed$" {
        player_level = player_level + 1;
        experience = 0;
        experience_needed = experience_needed + 50;
        say Level up! New level: $player_level$;
        effect give @s minecraft:experience 10 0;
    }
}

function "show_status" {
    say Level: $player_level$ Experience: $experience$/$experience_needed$;
    tellraw @a {"text":"Level $player_level$ - XP: $experience$/$experience_needed$","color":"gold"};
}

on_tick "level:gain_experience";
on_tick "level:show_status";
```

## Tested Examples

All examples on this page are thoroughly tested and available for download:

- **[hello_world.mdl](test_examples/hello_world.mdl)** - Basic hello world
- **[variables.mdl](test_examples/variables.mdl)** - Number variables
- **[conditionals.mdl](test_examples/conditionals.mdl)** - If/else logic
- **[loops.mdl](test_examples/loops.mdl)** - While and for loops
- **[game_system.mdl](test_examples/game_system.mdl)** - Complete game system
- **[multi_namespace.mdl](test_examples/multi_namespace.mdl)** - Multi-namespace organization

**Build and test any example:**
```bash
mdl build --mdl test_examples/example_name.mdl -o dist
# Copy dist/example_name/ to your world's datapacks folder
# Run /reload in-game
```

## **Simplified** Language Benefits

The **simplified** MDL language focuses on:

1. **Reliability**: Control structures that actually work
2. **Simplicity**: Number variables only with `$variable$` substitution
3. **Clarity**: Clear, readable syntax with explicit block boundaries
4. **Performance**: Efficient compilation to Minecraft commands
5. **Maintainability**: Easy to understand and modify

This **simplified** approach makes it much easier to create reliable Minecraft datapacks without the complexity of the previous version.


