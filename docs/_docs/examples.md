---
layout: page
title: Examples
permalink: /docs/examples/
---

# MDL Examples

This page contains complete, working examples that demonstrate MDL's modern JavaScript-style syntax with control structures, variables, expressions, and multi-file projects.

## Quick Examples

### Hello World

A simple datapack that displays a welcome message when loaded.

```mdl
// hello_world.mdl
pack "Hello World" "A simple example datapack" 82;

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

### Variable System

Demonstrates the modern variable system with expressions and arithmetic operations.

```mdl
// variables.mdl
pack "Variable System" "Demonstrates modern variables and expressions" 82;

namespace "variables";

// Number variables with expressions
var num player_count = 0;
var num health = 20;
var num level = 1;
var num experience = 0;

function "init" {
    say Initializing variable system...;
    player_count = 0;
    health = 20;
    level = 1;
    experience = 0;
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
    experience = $level$ * 100;  // Expression with multiplication
    say Level up! New level: $level$ Experience: $experience$;
    effect give @s minecraft:experience 10 0;
}

function "calculate_bonus" {
    var num bonus = $level$ * 10 + $player_count$;  // Complex expression
    say Bonus calculated: $bonus$;
}

on_load "variables:init";
on_tick "variables:count_players";
on_tick "variables:check_health";
```

## Control Structures

### If/Else Statements

```mdl
// conditionals.mdl
pack "Conditionals" "Demonstrates if/else logic" 82;

namespace "conditionals";

var num player_score = 0;
var num game_time = 0;

function "check_score" {
    if "$player_score$ > 100" {
        say Excellent score! You're a pro!;
        effect give @s minecraft:strength 30 0;
    } else if "$player_score$ > 50" {
        say Good score! Keep it up!;
        effect give @s minecraft:speed 30 0;
    } else if "$player_score$ > 10" {
        say Decent score. You can do better!;
    } else {
        say Low score. Try harder!;
        effect give @s minecraft:jump_boost 30 0;
    }
}

function "update_game" {
    game_time = game_time + 1;
    if "$game_time$ % 100 == 0" {
        say Game time: $game_time$ seconds;
    }
}

on_tick "conditionals:check_score";
on_tick "conditionals:update_game";
```

### While Loops

```mdl
// loops.mdl
pack "Loops" "Demonstrates while loops" 82;

namespace "loops";

var num counter = 0;
var num max_count = 10;

function "count_up" {
    while "$counter$ < $max_count$" {
        say Counter: $counter$;
        counter = counter + 1;
    }
    say Finished counting!;
}

function "reset_counter" {
    counter = 0;
    say Counter reset to 0;
}

on_load "loops:reset_counter";
on_tick "loops:count_up";
```

## Game Systems

### Health System

```mdl
// health_system.mdl
pack "Health System" "Complete health management" 82;

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

### Level System

```mdl
// level_system.mdl
pack "Level System" "Experience and leveling" 82;

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

## Multi-file Projects

### Project Structure

```
my_game/
├── main.mdl          # Main game logic
├── ui.mdl           # User interface
├── combat.mdl       # Combat system
└── data/
    ├── recipes/
    ├── loot_tables/
    └── advancements/
```

### Main Game File

```mdl
// main.mdl
pack "My Game" "A complete game system" 82;

namespace "game";

var num game_state = 0;  // 0=menu, 1=playing, 2=paused
var num player_count = 0;

function "init_game" {
    say Initializing game...;
    game_state = 0;
    player_count = 0;
}

function "start_game" {
    game_state = 1;
    say Game started!;
    effect give @a minecraft:speed 999999 0;
}

function "pause_game" {
    game_state = 2;
    say Game paused;
    effect clear @a minecraft:speed;
}

on_load "game:init_game";
```

### UI File

```mdl
// ui.mdl (no pack declaration needed)
namespace "ui";

function "show_menu" {
    tellraw @a {"text":"=== GAME MENU ===","color":"gold","bold":true};
    tellraw @a {"text":"Click to start game","color":"green","clickEvent":{"action":"run_command","value":"/function game:start_game"}};
}

function "show_hud" {
    tellraw @a {"text":"Game State: $game_state$","color":"yellow"};
    tellraw @a {"text":"Players: $player_count$","color":"aqua"};
}

on_tick "ui:show_hud";
```

### Combat File

```mdl
// combat.mdl (no pack declaration needed)
namespace "combat";

var num damage_multiplier = 1;

function "calculate_damage" {
    var num base_damage = 5;
    var num final_damage = base_damage * $damage_multiplier$;
    say Damage: $final_damage$;
}

function "power_up" {
    damage_multiplier = damage_multiplier + 0.5;
    say Power up! Multiplier: $damage_multiplier$;
}

on_tick "combat:calculate_damage";
```

## Registry Types

### Recipes

```mdl
// recipes.mdl
pack "Custom Recipes" "Custom crafting recipes" 82;

namespace "custom";

// Reference external JSON files
recipe "diamond_sword" "recipes/diamond_sword.json";
recipe "custom_pickaxe" "recipes/custom_pickaxe.json";

function "announce_recipes" {
    say Custom recipes loaded!;
}
```

### Loot Tables

```mdl
// loot.mdl
pack "Custom Loot" "Custom loot tables" 82;

namespace "loot";

loot_table "diamond_sword" "loot_tables/diamond_sword.json";
loot_table "treasure_chest" "loot_tables/treasure_chest.json";

function "spawn_treasure" {
    say Spawning treasure chest...;
    summon chest ~ ~ ~ {LootTable:"loot:treasure_chest"};
}
```

## Tested Examples

All examples on this page are thoroughly tested and available for download:

- **[hello_world.mdl](test_examples/hello_world.mdl)** - Basic hello world
- **[variables.mdl](test_examples/variables.mdl)** - Number variables
- **[conditionals.mdl](test_examples/conditionals.mdl)** - If/else logic
- **[loops.mdl](test_examples/loops.mdl)** - While and for loops
- **[health_system.mdl](test_examples/health_system.mdl)** - Health management
- **[level_system.mdl](test_examples/level_system.mdl)** - Experience system

**Build and test any example:**
```bash
mdl build --mdl test_examples/example_name.mdl -o dist
# Copy dist/example_name/ to your world's datapacks folder
# Run /reload in-game
```

## Language Benefits

MDL provides a modern, reliable approach to Minecraft datapack development:

1. **Reliability**: Control structures that actually work
2. **Expressiveness**: Variables with expressions and arithmetic operations
3. **Clarity**: Clear, readable syntax with explicit block boundaries
4. **Performance**: Efficient compilation to Minecraft commands
5. **Maintainability**: Easy to understand and modify
6. **Modularity**: Multi-file projects with proper namespace separation
7. **Optimization**: Automatic variable initialization and smart selector handling

This modern approach makes it much easier to create complex, reliable Minecraft datapacks with proper organization and advanced features.


