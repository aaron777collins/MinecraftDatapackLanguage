---
layout: page
title: Examples
permalink: /docs/examples/
---

# JavaScript-style MDL Examples (v10+)

This page contains complete, working examples of the new JavaScript-style MDL format that demonstrate all the modern features and patterns.

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

### Variable System

Demonstrates the new variable system with different data types.

```mdl
// variables.mdl
pack "Variable System" description "Demonstrates variables and data types" pack_format 82;

namespace "variables";

// Global variables
var num player_count = 0;
var str welcome_message = "Welcome to the server!";
var list effects = ["speed", "jump_boost", "night_vision"];

function "init" {
    say Initializing variable system...;
    player_count = 0;
    welcome_message = "System ready!";
}

function "count_players" {
    player_count = 0;
    for player in @a {
        player_count = player_count + 1;
    }
    say Player count: player_count;
}

function "show_welcome" {
    tellraw @a {"text":welcome_message,"color":"green"};
}

function "apply_effects" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            effect give @s minecraft:speed 10 1;
            effect give @s minecraft:jump_boost 10 0;
        }
    }
}

on_load "variables:init";
on_tick "variables:count_players";
```

### Particle Effects

A datapack that creates particle effects around players with variables.

```mdl
// particles.mdl
pack "Particle Effects" description "Creates particle effects around players" pack_format 82;

namespace "particles";

// Configuration variables
var num particle_count = 5;
var str particle_type = "minecraft:end_rod";

function "tick" {
    for player in @a {
        particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 particle_count;
        particle minecraft:firework ~ ~ ~ 0.2 0.2 0.2 0.02 2;
    }
}

function "init" {
    say Particle effects enabled!;
    particle_count = 10;
}

on_load "particles:init";
on_tick "particles:tick";
```

## Control Flow Examples

### Advanced Conditional Logic

Demonstrates complex conditional statements with variables.

```mdl
// conditionals.mdl
pack "Advanced Conditionals" description "Complex conditional logic" pack_format 82;

namespace "conditionals";

// State variables
var num player_level = 0;
var str player_class = "warrior";
var num experience = 0;

function "check_player_status" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            if "entity @s[gamemode=survival]" {
                if "score @s experience matches 100.." {
                    player_level = player_level + 1;
                    experience = 0;
                    say Level up! New level: player_level;
                }
                
                if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
                    player_class = "warrior";
                    effect give @s minecraft:strength 10 1;
                } else if "entity @s[nbt={SelectedItem:{id:'minecraft:bow'}}]" {
                    player_class = "archer";
                    effect give @s minecraft:speed 10 1;
                } else if "entity @s[nbt={SelectedItem:{id:'minecraft:stick'}}]" {
                    player_class = "mage";
                    effect give @s minecraft:night_vision 10 0;
                }
            } else {
                say Creative mode detected;
            }
        }
    }
}

on_tick "conditionals:check_player_status";
```

### Switch Statements

Demonstrates the new switch statement feature.

```mdl
// switch_example.mdl
pack "Switch Statements" description "Using switch statements" pack_format 82;

namespace "switch_example";

var num item_type = 0;

function "handle_item" {
    for player in @a {
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
            item_type = 1;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:bow'}}]" {
            item_type = 2;
        } else if "entity @s[nbt={SelectedItem:{id:'minecraft:shield'}}]" {
            item_type = 3;
        } else {
            item_type = 0;
        }
        
        switch (item_type) {
            case 1:
                say You have a sword;
                effect give @s minecraft:strength 10 1;
                break;
            case 2:
                say You have a bow;
                effect give @s minecraft:speed 10 1;
                break;
            case 3:
                say You have a shield;
                effect give @s minecraft:resistance 10 1;
                break;
            default:
                say No special item detected;
                break;
        }
    }
}

on_tick "switch_example:handle_item";
```

### Loop Examples

Demonstrates various loop patterns with variables.

```mdl
// loops.mdl
pack "Loop Examples" description "Advanced loop patterns" pack_format 82;

namespace "loops";

var num counter = 0;
var num max_count = 10;
var list entities = ["zombie", "skeleton", "creeper"];

function "countdown" {
    counter = max_count;
    while "score @s counter matches 1.." {
        say Countdown: counter;
        counter = counter - 1;
        if "score @s counter matches 0" {
            say Blast off!;
            break;
        }
    }
}

function "process_entities" {
    for entity in @e[type=minecraft:zombie] {
        effect give @s minecraft:glowing 10 0;
        particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.1 3;
    }
    
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            counter = counter + 1;
            if "score @s counter matches 10" {
                say Processed 10 players;
                counter = 0;
                continue;
            }
        }
    }
}

on_tick "loops:process_entities";
```

## Error Handling Examples

### Try-Catch Blocks

Demonstrates error handling with try-catch blocks.

```mdl
// error_handling.mdl
pack "Error Handling" description "Using try-catch blocks" pack_format 82;

namespace "error_handling";

var str error_message = "No error";

function "safe_operation" {
    for player in @a {
        try {
            say Attempting risky operation...;
            // Simulate a risky operation
            if "entity @s[type=minecraft:player]" {
                effect give @s minecraft:levitation 10 1;
            } else {
                throw "Invalid entity type";
            }
        } catch (error) {
            error_message = error;
            say Operation failed: error_message;
            effect give @s minecraft:slowness 10 0;
        }
    }
}

function "divide_by_zero" {
    var num result = 0;
    try {
        result = 10 / 0;
        say Result: result;
    } catch (error) {
        say Division error: error;
        result = 0;
    }
}

on_tick "error_handling:safe_operation";
```

## Function System Examples

### Functions with Parameters and Return Values

Demonstrates advanced function features.

```mdl
// functions.mdl
pack "Advanced Functions" description "Functions with parameters and returns" pack_format 82;

namespace "functions";

var num health = 20;
var num mana = 100;

function "heal_player" (amount) {
    health = health + amount;
    if "score @s health > 20" {
        health = 20;
    }
    effect give @s minecraft:instant_health 1 1;
    return health;
}

function "use_mana" (cost) {
    if "score @s mana >= cost" {
        mana = mana - cost;
        return true;
    } else {
        return false;
    }
}

function "cast_spell" {
    var num spell_cost = 25;
    var bool success = use_mana(spell_cost);
    
    if (success) {
        say Spell cast successfully!;
        effect give @s minecraft:night_vision 30 0;
    } else {
        say Not enough mana!;
    }
}

function "restore_health" {
    var num old_health = health;
    health = heal_player(10);
    say Health restored from old_health to health;
}

on_tick "functions:cast_spell";
```

## Multi-file Project Examples

### Modular Architecture

Demonstrates how to organize code across multiple files.

```mdl
// core.mdl
pack "Modular Project" description "Multi-file project example" pack_format 82;

namespace "core";

// Global state
var num game_time = 0;
var str game_state = "running";

function "init" {
    say Core module initialized;
    game_time = 0;
    game_state = "running";
}

function "tick" {
    game_time = game_time + 1;
    if "score @s game_time matches 1200" {
        say One minute has passed;
        game_time = 0;
    }
}

on_load "core:init";
on_tick "core:tick";
```

```mdl
// combat.mdl
namespace "combat";

import "core" from "./core.mdl";

function "attack" {
    for player in @a {
        if "entity @s[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
            execute as @s at @s if entity @e[type=minecraft:zombie,distance=..3] run function combat:damage;
        }
    }
}

function "damage" {
    effect give @e[type=minecraft:zombie,distance=..3] minecraft:instant_damage 1 1;
    particle minecraft:crit ~ ~ ~ 0.5 0.5 0.5 0.1 10;
}

on_tick "combat:attack";
```

```mdl
// ui.mdl
namespace "ui";

import "core" from "./core.mdl";

function "show_hud" {
    for player in @a {
        tellraw @s {"text":"Game Time: ","color":"yellow","extra":[{"score":{"name":"@s","objective":"game_time"},"color":"white"}]};
        tellraw @s {"text":"Game State: ","color":"blue","extra":[{"text":"game_state","color":"white"}]};
    }
}

on_tick "ui:show_hud";
```

## Game Mechanics Examples

### RPG System

A comprehensive RPG system using all new features.

```mdl
// rpg_system.mdl
pack "RPG System" description "Complete RPG mechanics" pack_format 82;

namespace "rpg";

// Player stats
var num player_level = 1;
var num experience = 0;
var num health = 20;
var num mana = 100;
var str player_class = "adventurer";
var list inventory = ["sword", "shield", "potion"];

function "init_player" {
    player_level = 1;
    experience = 0;
    health = 20;
    mana = 100;
    player_class = "adventurer";
    say Player initialized as level player_level player_class;
}

function "gain_experience" (amount) {
    experience = experience + amount;
    say Gained amount experience points;
    
    // Level up logic
    if "score @s experience >= 100" {
        player_level = player_level + 1;
        experience = experience - 100;
        health = health + 5;
        mana = mana + 10;
        say Level up! You are now level player_level;
        effect give @s minecraft:glowing 60 0;
    }
}

function "use_item" (item_name) {
    switch (item_name) {
        case "potion":
            if "score @s health < 20" {
                health = heal_player(10);
                say Used health potion;
            }
            break;
        case "mana_potion":
            if "score @s mana < 100" {
                mana = mana + 25;
                say Used mana potion;
            }
            break;
        default:
            say Unknown item: item_name;
            break;
    }
}

function "heal_player" (amount) {
    var num old_health = health;
    health = health + amount;
    if "score @s health > 20" {
        health = 20;
    }
    effect give @s minecraft:instant_health 1 1;
    return health;
}

function "combat_tick" {
    for player in @a {
        if "entity @s[type=minecraft:player]" {
            // Auto-heal over time
            if "score @s health < 20" {
                health = health + 1;
            }
            
            // Mana regeneration
            if "score @s mana < 100" {
                mana = mana + 2;
            }
        }
    }
}

on_load "rpg:init_player";
on_tick "rpg:combat_tick";
```

### Inventory System

Advanced inventory management with variables and error handling.

```mdl
// inventory_system.mdl
pack "Inventory System" description "Advanced inventory management" pack_format 82;

namespace "inventory";

var num inventory_size = 36;
var list items = [];
var num gold_coins = 0;

function "add_item" (item_name) {
    try {
        if "score @s items < inventory_size" {
            items = items + [item_name];
            say Added item_name to inventory;
        } else {
            throw "Inventory full";
        }
    } catch (error) {
        say Cannot add item: error;
    }
}

function "remove_item" (item_name) {
    try {
        var num index = find_item(item_name);
        if (index >= 0) {
            items = remove_from_list(items, index);
            say Removed item_name from inventory;
        } else {
            throw "Item not found";
        }
    } catch (error) {
        say Cannot remove item: error;
    }
}

function "find_item" (item_name) {
    for i in range(len(items)) {
        if (items[i] == item_name) {
            return i;
        }
    }
    return -1;
}

function "show_inventory" {
    for player in @a {
        tellraw @s {"text":"Inventory: ","color":"yellow"};
        for item in items {
            tellraw @s {"text":"- item","color":"white"};
        }
        tellraw @s {"text":"Gold: gold_coins","color":"gold"};
    }
}

on_tick "inventory:show_inventory";
```

## Performance Examples

### Optimized Systems

Demonstrates performance optimization techniques.

```mdl
// performance.mdl
pack "Performance" description "Optimized systems" pack_format 82;

namespace "performance";

var num frame_count = 0;
var num update_interval = 20;

function "optimized_tick" {
    frame_count = frame_count + 1;
    
    // Only update every 20 ticks (1 second)
    if "score @s frame_count % update_interval == 0" {
        // Process only nearby entities
        for entity in @e[type=minecraft:zombie,distance=..32] {
            effect give @s minecraft:glowing 10 0;
        }
        
        // Batch process players
        for player in @a[limit=5] {
            effect give @s minecraft:speed 10 0;
        }
    }
}

function "memory_management" {
    // Clear old data periodically
    if "score @s frame_count >= 1200" {
        frame_count = 0;
        say Memory cleanup performed;
    }
}

on_tick "performance:optimized_tick";
on_tick "performance:memory_management";
```

## Building and Testing

To build these examples:

```bash
# Build a single file
mdl build --mdl example.mdl -o dist

# Build multi-file project
mdl build --mdl "core.mdl combat.mdl ui.mdl" -o dist

# Check syntax
mdl check example.mdl

# Run tests
mdl test --mdl example.mdl
```

## VS Code Integration

These examples work perfectly with the VS Code extension:

1. **Install the extension** from the marketplace
2. **Open any .mdl file** to get syntax highlighting
3. **Use snippets** for rapid development
4. **Get IntelliSense** for all keywords and functions
5. **Build directly** from the command palette

## Next Steps

After exploring these examples:

1. **Try the VS Code extension** for the best development experience
2. **Check the language reference** for complete syntax documentation
3. **Explore the Python API** for programmatic datapack creation
4. **Join the community** to share your creations

---

**Previous**: [Language Reference](language-reference.md) | **Next**: [Python API](python-api.md)
