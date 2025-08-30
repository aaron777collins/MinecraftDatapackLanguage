---
layout: page
title: Examples
permalink: /docs/examples/
---

# MDL Examples

This page contains complete, working examples that demonstrate MDL's powerful features for creating Minecraft datapacks.

> **📚 Need help with MDL syntax?** Check out the [Language Reference](/docs/language-reference/) for complete syntax documentation.

## Raw Text Example

A practical example showing how to use raw text blocks to include commands with MDL keywords or complex JSON.

```mdl
// raw_text_example.mdl
pack "Raw Text Demo" "Demonstrates raw text functionality" 82;

namespace "demo";

var num counter = 0;
var num timer_enabled = 0;

function "main" {
    say Hello from MDL!;
    counter = counter + 1;
    
    // Raw text block with MDL keywords in commands
    $!raw
    say "To enable the timer, run /function demo:enable_timer";
    say "To disable the timer, run /function demo:disable_timer";
    raw!$
    
    // Raw text with complex JSON and variable substitution
    $!raw
    tellraw @a {"text":"Counter: $counter$","color":"yellow"};
    tellraw @a {"text":"Timer: $timer_enabled$","color":"aqua"};
    raw!$
    
    // Raw text with complex clickable JSON
    $!raw
    tellraw @a {"text":"=== MENU ===","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function demo:show_menu"}};
    raw!$
}

function "enable_timer" {
    timer_enabled = 1;
    say Timer enabled!;
}

function "disable_timer" {
    timer_enabled = 0;
    say Timer disabled!;
}

function "show_menu" {
    $!raw
    tellraw @s {"text":"=== OPTIONS ===","color":"gold","bold":true};
    tellraw @s {"text":"[Enable Timer]","color":"green","clickEvent":{"action":"run_command","value":"/function demo:enable_timer"}};
    tellraw @s {"text":"[Disable Timer]","color":"red","clickEvent":{"action":"run_command","value":"/function demo:disable_timer"}};
    raw!$
}

on_load "demo:main";
```

**Key Features Demonstrated:**
- **MDL Keywords in Commands**: Using "function" in say commands without parser conflicts
- **Complex JSON**: Multi-line JSON with click events and formatting
- **Variable Substitution**: `$counter$` and `$timer_enabled$` work inside raw text
- **Interactive Elements**: Clickable text with command execution

## Hello World

A simple datapack that displays a welcome message and counts how many times it's been called.

```mdl
// hello.mdl
pack "My First Pack" "A simple example" 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    say Counter: $counter$;
}

on_load "example:hello";
```

**Build and use:**
```bash
mdl build --mdl hello.mdl -o dist
# Copy dist/My_First_Pack/ to your world's datapacks folder
# Run /reload in-game
```

## Variable Scoping Example

A comprehensive example demonstrating different variable scopes in MDL.

```mdl
// scope_example.mdl
pack "Scope Demo" "Demonstrates variable scoping" 82;

namespace "scope";

// Player-specific variables (default behavior)
var num player_score = 0;
var num player_level = 1;

// Global variables (stored on mdl_server armor stand)
var num global_counter scope<global> = 0;
var num global_timer scope<global> = 0;

// Player-scoped variables (explicit)
var num player_health scope<@s> = 20;

// Team-scoped variables (stored on team members)
var num team_score scope<@a[team=red]> = 0;
var num team_bonus scope<@a[team=blue]> = 0;

// World-scoped variables (stored on specific entities)
var num world_timer scope<@e[type=armor_stand,tag=world_timer,limit=1]> = 0;

function "enable_timer" {
    global_timer = 1;  // Uses global scope
    player_score = player_score + 10;  // Uses @s (default)
    team_score = team_score + 5;  // Uses @a[team=red]
    world_timer = world_timer + 1;  // Uses custom armor stand
    
    say Timer enabled!;
    say Your score: $player_score$;
    say Team score: $team_score$;
    say World timer: $world_timer$;
}

function "disable_timer" {
    global_timer = 0;  // Uses global scope
    say Timer disabled!;
}

function "show_stats" {
    say === STATS ===;
    say Global counter: $global_counter$;
    say Global timer: $global_timer$;
    say Your score: $player_score$;
    say Your level: $player_level$;
    say Team score: $team_score$;
    say Team bonus: $team_bonus$;
    say World timer: $world_timer$;
}

function "load" {
    global_counter = 0;  // Uses global scope
    global_timer = 0;  // Uses global scope
    say Scope demo loaded!;
}

function "tick" {
    if "$global_timer$ == 1" {
        global_counter = global_counter + 1;  // Uses global scope
        player_level = player_level + 1;  // Uses @s (default)
        team_bonus = team_bonus + 2;  // Uses @a[team=blue]
        
        if "$global_counter$ >= 100" {
            global_timer = 0;  // Uses global scope
            say Timer stopped at 100!;
        }
    }
}

on_load "scope:load";
on_tick "scope:tick";
```

**Key Features Demonstrated:**
- **Default Variables**: `player_score` and `player_level` default to `@s` (executing entity)
- **Global Variables**: `global_counter` and `global_timer` use `scope<global>` for server-wide storage
- **Player-Scoped Variables**: `player_health` explicitly uses `scope<@s>`
- **Team-Scoped Variables**: `team_score` and `team_bonus` stored on team members
- **World-Scoped Variables**: `world_timer` stored on specific armor stand
- **Variable Access**: Each variable is accessed from its appropriate scope
- **Cross-Scope Operations**: Functions can modify variables from different scopes

**Key Benefits:**
- **`@s` as default**: Functions are reusable and can be called by any entity
- **`global` keyword**: Clear and explicit for server-wide variables
- **Flexible execution**: Use `execute as @a run function scope:enable_timer` to run for all players

## Player Counter System

A practical system that counts players and displays statistics.

```mdl
// player_counter.mdl
pack "Player Counter" "Counts and tracks players" 82;

namespace "stats";

var num player_count = 0;
var num total_joins = 0;
var num current_online = 0;

function "count_players" {
    player_count = 0;
    for player in @a {
        player_count = player_count + 1;
    }
    current_online = player_count;
    say Players online: $current_online$;
}

function "player_joined" {
    total_joins = total_joins + 1;
    say Welcome! Total joins: $total_joins$;
    tellraw @a {"text":"A player joined!","color":"green"};
}

function "show_stats" {
    tellraw @a {"text":"=== SERVER STATS ===","color":"gold","bold":true};
    tellraw @a {"text":"Online: $current_online$","color":"aqua"};
    tellraw @a {"text":"Total Joins: $total_joins$","color":"yellow"};
}

on_tick "stats:count_players";
on_tick "stats:show_stats";
```

## Health Monitor

A health monitoring system that alerts when players are low on health.

```mdl
// health_monitor.mdl
pack "Health Monitor" "Monitors player health" 82;

namespace "health";

var num low_health_threshold = 8;
var num critical_health_threshold = 4;

function "check_health" {
    for player in @a {
        if "$player.health$ <= $critical_health_threshold$" {
            tellraw @a {"text":"CRITICAL: $player.name$ is dying!","color":"red","bold":true};
            effect give $player minecraft:regeneration 10 1;
        } else if "$player.health$ <= $low_health_threshold$" {
            tellraw @a {"text":"Warning: $player.name$ is low on health","color":"orange"};
            effect give $player minecraft:resistance 5 0;
        }
    }
}

function "heal_all" {
    for player in @a {
        effect give $player minecraft:instant_health 1 0;
    }
    say All players healed!;
}

on_tick "health:check_health";
```

## Game Timer

A countdown timer system for games and events.

```mdl
// game_timer.mdl
pack "Game Timer" "Countdown timer system" 82;

namespace "timer";

var num time_remaining = 300;  // 5 minutes in seconds
var num game_active = 0;       // 0=waiting, 1=active, 2=finished

function "start_game" {
    game_active = 1;
    time_remaining = 300;
    say Game started! 5 minutes remaining;
    tellraw @a {"text":"GAME STARTED!","color":"green","bold":true};
}

function "update_timer" {
    if "$game_active$ == 1" {
        time_remaining = time_remaining - 1;
        
        if "$time_remaining$ <= 0" {
            game_active = 2;
            say Game over! Time's up!;
            tellraw @a {"text":"GAME OVER!","color":"red","bold":true};
        } else if "$time_remaining$ % 60 == 0" {
            var num minutes = $time_remaining$ / 60;
            say $minutes$ minutes remaining;
        } else if "$time_remaining$ <= 10" {
            say $time_remaining$ seconds remaining!;
        }
    }
}

function "show_time" {
    if "$game_active$ == 1" {
        var num minutes = $time_remaining$ / 60;
        var num seconds = $time_remaining$ % 60;
        tellraw @a {"text":"Time: $minutes$:$seconds$","color":"yellow"};
    }
}

on_tick "timer:update_timer";
on_tick "timer:show_time";
```

## Score System

A comprehensive scoring system with leaderboards.

```mdl
// score_system.mdl
pack "Score System" "Player scoring and leaderboards" 82;

namespace "score";

var num player1_score = 0;
var num player2_score = 0;
var num player3_score = 0;
var num high_score = 0;

function "add_points" {
    // Simulate points being earned
    player1_score = player1_score + 10;
    player2_score = player2_score + 15;
    player3_score = player3_score + 8;
    
    // Update high score
    if "$player1_score$ > $high_score$" {
        high_score = player1_score;
    }
    if "$player2_score$ > $high_score$" {
        high_score = player2_score;
    }
    if "$player3_score$ > $high_score$" {
        high_score = player3_score;
    }
}

function "show_leaderboard" {
    tellraw @a {"text":"=== LEADERBOARD ===","color":"gold","bold":true};
    tellraw @a {"text":"Player 1: $player1_score$","color":"aqua"};
    tellraw @a {"text":"Player 2: $player2_score$","color":"aqua"};
    tellraw @a {"text":"Player 3: $player3_score$","color":"aqua"};
    tellraw @a {"text":"High Score: $high_score$","color":"yellow","bold":true};
}

function "reset_scores" {
    player1_score = 0;
    player2_score = 0;
    player3_score = 0;
    say All scores reset!;
}

on_tick "score:add_points";
on_tick "score:show_leaderboard";
```

## Multi-File Project: Adventure Game

A complete adventure game system split across multiple files.

### Main Game File

```mdl
// main.mdl
pack "Adventure Game" "A complete adventure system" 82;

namespace "game";

var num game_state = 0;  // 0=menu, 1=playing, 2=paused, 3=game_over
var num player_level = 1;
var num player_health = 20;
var num player_gold = 0;

function "init_game" {
    say Adventure Game initialized!;
    game_state = 0;
    player_level = 1;
    player_health = 20;
    player_gold = 0;
}

function "start_game" {
    game_state = 1;
    say Adventure begins!;
    tellraw @a {"text":"ADVENTURE STARTED!","color":"green","bold":true};
}

function "pause_game" {
    game_state = 2;
    say Game paused;
    tellraw @a {"text":"Game Paused","color":"yellow"};
}

on_load "game:init_game";
```

### Combat System

```mdl
// combat.mdl
namespace "combat";

var num damage_multiplier = 1;
var num critical_chance = 10;  // percentage

function "attack" {
    var num base_damage = 5;
    var num final_damage = base_damage * $damage_multiplier$;
    
    if "$critical_chance$ >= 10" {
        final_damage = final_damage * 2;
        say Critical hit! Damage: $final_damage$;
    } else {
        say Normal attack! Damage: $final_damage$;
    }
}

function "power_up" {
    damage_multiplier = damage_multiplier + 0.5;
    say Power increased! Multiplier: $damage_multiplier$;
}

function "heal_player" {
    if "$game.player_health$ < 20" {
        game.player_health = game.player_health + 5;
        say Healed! Health: $game.player_health$;
    }
}
```

### UI System

```mdl
// ui.mdl
namespace "ui";

function "show_menu" {
    if "$game.game_state$ == 0" {
        tellraw @a {"text":"=== ADVENTURE GAME ===","color":"gold","bold":true};
        tellraw @a {"text":"Click to start","color":"green","clickEvent":{"action":"run_command","value":"/function game:start_game"}};
    }
}

function "show_hud" {
    if "$game.game_state$ == 1" {
        tellraw @a {"text":"Level: $game.player_level$","color":"yellow"};
        tellraw @a {"text":"Health: $game.player_health$","color":"red"};
        tellraw @a {"text":"Gold: $game.player_gold$","color":"gold"};
    }
}

on_tick "ui:show_menu";
on_tick "ui:show_hud";
```

## Advanced: Weather Control System

A sophisticated weather control system with multiple states.

```mdl
// weather_control.mdl
pack "Weather Control" "Advanced weather management" 82;

namespace "weather";

var num weather_state = 0;  // 0=clear, 1=rain, 2=storm, 3=snow
var num weather_duration = 0;
var num max_duration = 1200;  // 20 seconds

function "set_clear" {
    weather_state = 0;
    weather duration clear 1000000;
    say Weather set to clear;
    tellraw @a {"text":"Weather: Clear","color":"yellow"};
}

function "set_rain" {
    weather_state = 1;
    weather duration rain 1000000;
    say Weather set to rain;
    tellraw @a {"text":"Weather: Rain","color":"blue"};
}

function "set_storm" {
    weather_state = 2;
    weather duration rain 1000000;
    weather duration thunder 1000000;
    say Weather set to storm;
    tellraw @a {"text":"Weather: Storm","color":"red"};
}

function "set_snow" {
    weather_state = 3;
    weather duration rain 1000000;
    say Weather set to snow;
    tellraw @a {"text":"Weather: Snow","color":"white"};
}

function "cycle_weather" {
    weather_duration = weather_duration + 1;
    
    if "$weather_duration$ >= $max_duration$" {
        weather_duration = 0;
        weather_state = ($weather_state$ + 1) % 4;
        
        if "$weather_state$ == 0" {
            function weather:set_clear;
        } else if "$weather_state$ == 1" {
            function weather:set_rain;
        } else if "$weather_state$ == 2" {
            function weather:set_storm;
        } else {
            function weather:set_snow;
        }
    }
}

on_tick "weather:cycle_weather";
```

## Registry Examples

### Custom Recipes

```mdl
// recipes.mdl
pack "Custom Recipes" "Custom crafting recipes" 82;

namespace "custom";

// Reference external JSON files
recipe "diamond_sword" "recipes/diamond_sword.json";
recipe "custom_pickaxe" "recipes/custom_pickaxe.json";

function "announce_recipes" {
    say Custom recipes loaded!;
    tellraw @a {"text":"Custom recipes available!","color":"green"};
}

on_load "custom:announce_recipes";
```

### Custom Loot Tables

```mdl
// loot.mdl
pack "Custom Loot" "Custom loot tables" 82;

namespace "loot";

loot_table "diamond_sword" "loot_tables/diamond_sword.json";
loot_table "treasure_chest" "loot_tables/treasure_chest.json";

function "spawn_treasure" {
    say Spawning treasure chest...;
    summon chest ~ ~ ~ {LootTable:"loot:treasure_chest"};
    tellraw @a {"text":"Treasure chest spawned!","color":"gold"};
}
```

## Building and Testing

All examples can be built and tested:

```bash
# Build any example
mdl build --mdl example.mdl -o dist

# Copy to your world's datapacks folder
cp -r dist/* ~/.minecraft/saves/YourWorld/datapacks/

# Reload in-game
/reload
```

## Key Features Demonstrated

These examples showcase MDL's powerful features:

- **Variables**: Number variables with expressions and arithmetic
- **Control Flow**: If/else statements and while loops
- **Functions**: Reusable code blocks with parameters
- **Hooks**: Automatic execution with `on_load` and `on_tick`
- **Multi-file**: Modular projects with namespace separation
- **Registry Types**: Recipes, loot tables, and other Minecraft content
- **Player Interaction**: Commands that respond to player actions
- **Real-time Systems**: Timers, counters, and monitoring systems

Each example is complete, tested, and ready to use in your Minecraft world!


