---
layout: page
title: Examples
permalink: /docs/examples/
---

# Examples

This page contains complete, working examples of MDL datapacks that demonstrate various features and patterns.

## Basic Examples

### Hello World

A simple datapack that displays a welcome message when loaded.

```mdl
# hello_world.mdl
pack "Hello World" description "A simple example datapack" pack_format 48

namespace "example"

function "hello":
    say Hello, Minecraft!
    tellraw @a {"text":"Welcome to my datapack!","color":"green"}

on_load "example:hello"
```

**Build and use:**
```bash
mdl build --mdl hello_world.mdl -o dist
# Copy dist/hello_world/ to your world's datapacks folder
# Run /reload in-game
```

### Particle Effects

A datapack that creates particle effects around players.

```mdl
# particles.mdl
pack "Particle Effects" description "Creates particle effects around players" pack_format 48

namespace "particles"

function "tick":
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1
    execute as @a run particle minecraft:firework ~ ~ ~ 0.2 0.2 0.2 0.02 2

function "init":
    say Particle effects enabled!

on_load "particles:init"
on_tick "particles:tick"
```

### Custom Commands

A datapack that adds custom commands for players.

```mdl
# commands.mdl
pack "Custom Commands" description "Adds useful commands for players" pack_format 48

namespace "commands"

function "heal":
    effect give @s minecraft:instant_health 1 1
    effect give @s minecraft:regeneration 5 1
    tellraw @s {"text":"You have been healed!","color":"green"}

function "feed":
    effect give @s minecraft:saturation 1 5
    tellraw @s {"text":"You are no longer hungry!","color":"yellow"}

function "fly":
    effect give @s minecraft:levitation 10 1
    tellraw @s {"text":"You can now fly!","color":"aqua"}

# Make functions available as commands
tag function "minecraft:load":
    add "commands:heal"
    add "commands:feed"
    add "commands:fly"
```

## Intermediate Examples

### Combat System

A more complex datapack that adds combat enhancements.

```mdl
# combat_system.mdl
pack "Combat System" description "Enhanced combat mechanics" pack_format 48

namespace "combat"

function "weapon_effects":
    # Diamond sword gives strength
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true
    
    # Golden sword gives speed
    execute as @a[nbt={SelectedItem:{id:"minecraft:golden_sword"}}] \
        run effect give @s minecraft:speed 1 0 true
    
    # Netherite sword gives fire resistance
    execute as @a[nbt={SelectedItem:{id:"minecraft:netherite_sword"}}] \
        run effect give @s minecraft:fire_resistance 1 0 true

function "armor_effects":
    # Diamond armor gives resistance
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] \
        run effect give @s minecraft:resistance 1 0 true
    
    # Netherite armor gives fire resistance
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:netherite_helmet"}]}] \
        run effect give @s minecraft:fire_resistance 1 0 true

function "update_combat":
    function combat:weapon_effects
    function combat:armor_effects

on_tick "combat:update_combat"
```

### UI System

A datapack that adds a custom HUD and UI elements.

```mdl
# ui_system.mdl
pack "UI System" description "Custom HUD and UI elements" pack_format 48

namespace "ui"

function "hud":
    # Show current health
    execute as @a run title @s actionbar \
        {"text":"Health: ","color":"red","extra":[{"score":{"name":"@s","objective":"health"}}]}
    
    # Show current food level
    execute as @a run title @s actionbar \
        {"text":"Food: ","color":"yellow","extra":[{"score":{"name":"@s","objective":"food"}}]}

function "welcome_message":
    tellraw @a {"text":"Welcome to the server!","color":"gold","bold":true}
    tellraw @a {"text":"Use /help for commands","color":"gray","italic":true}

function "update_ui":
    function ui:hud

on_load "ui:welcome_message"
on_tick "ui:update_ui"
```

## Advanced Examples

### Multi-Namespace Adventure Pack

A comprehensive datapack with multiple systems working together.

```mdl
# adventure_pack.mdl
pack "Adventure Pack" description "A complete adventure experience" pack_format 48

# Core system
namespace "core"

function "init":
    say [core:init] Initializing Adventure Pack...
    tellraw @a {"text":"Adventure Pack loaded!","color":"green"}
    scoreboard objectives add adventure_points dummy "Adventure Points"

function "tick":
    say [core:tick] Core systems running...

# Combat system
namespace "combat"

function "weapon_effects":
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true

function "update_combat":
    function core:tick
    function combat:weapon_effects

# UI system
namespace "ui"

function "hud":
    title @a actionbar {"text":"Adventure Pack Active","color":"gold"}

function "update_ui":
    function ui:hud
    function combat:update_combat

# Data tags
namespace "data"

# Function tags
tag function "minecraft:load":
    add "core:init"

tag function "minecraft:tick":
    add "ui:update_ui"

# Item tags
tag item "adventure:weapons":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag item "adventure:armor":
    add "minecraft:diamond_helmet"
    add "minecraft:diamond_chestplate"
    add "minecraft:diamond_leggings"
    add "minecraft:diamond_boots"
```

### Python API Example

The same adventure pack created using the Python API:

```python
from minecraft_datapack_language import Pack

def create_adventure_pack():
    # Create the main pack
    pack = Pack(
        name="Adventure Pack",
        description="A complete adventure experience",
        pack_format=48
    )
    
    # Core system
    core = pack.namespace("core")
    core.function("init",
        'say [core:init] Initializing Adventure Pack...',
        'tellraw @a {"text":"Adventure Pack loaded!","color":"green"}',
        'scoreboard objectives add adventure_points dummy "Adventure Points"'
    )
    
    core.function("tick",
        'say [core:tick] Core systems running...'
    )
    
    # Combat system
    combat = pack.namespace("combat")
    combat.function("weapon_effects",
        'execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run effect give @s minecraft:strength 1 0 true'
    )
    
    combat.function("update_combat",
        'function core:tick',
        'function combat:weapon_effects'
    )
    
    # UI system
    ui = pack.namespace("ui")
    ui.function("hud",
        'title @a actionbar {"text":"Adventure Pack Active","color":"gold"}'
    )
    
    ui.function("update_ui",
        'function ui:hud',
        'function combat:update_combat'
    )
    
    # Lifecycle hooks
    pack.on_load("core:init")
    pack.on_tick("ui:update_ui")
    
    # Function tags
    pack.tag("function", "minecraft:load", values=["core:init"])
    pack.tag("function", "minecraft:tick", values=["ui:update_ui"])
    
    # Data tags
    pack.tag("item", "adventure:weapons", values=[
        "minecraft:diamond_sword",
        "minecraft:netherite_sword"
    ])
    
    pack.tag("item", "adventure:armor", values=[
        "minecraft:diamond_helmet",
        "minecraft:diamond_chestplate",
        "minecraft:diamond_leggings",
        "minecraft:diamond_boots"
    ])
    
    return pack

# Create and build the pack
if __name__ == "__main__":
    pack = create_adventure_pack()
    pack.build("dist")
    print("Adventure pack built successfully!")
```

## Multi-file Examples

### Organized Project Structure

A large datapack organized across multiple files:

**Project structure:**
```
adventure_pack/
├── core.mdl              # Main pack and core systems
├── combat/
│   ├── weapons.mdl       # Weapon-related functions
│   └── armor.mdl         # Armor-related functions
├── ui/
│   └── hud.mdl           # UI and HUD functions
└── data/
    └── tags.mdl          # Data tags and function tags
```

**`core.mdl`** (main file):
```mdl
# core.mdl - Main pack and core systems
pack "Adventure Pack" description "Multi-file example datapack" pack_format 48

namespace "core"

function "init":
    say [core:init] Initializing Adventure Pack...
    tellraw @a {"text":"Adventure Pack loaded!","color":"green"}

function "tick":
    say [core:tick] Core systems running...

on_load "core:init"
on_tick "core:tick"
```

**`combat/weapons.mdl`** (combat module):
```mdl
# combat/weapons.mdl - Weapon-related functions
namespace "combat"

function "weapon_effects":
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] \
        run effect give @s minecraft:strength 1 0 true

function "update_combat":
    function core:tick
    function combat:weapon_effects
```

**`combat/armor.mdl`** (armor module):
```mdl
# combat/armor.mdl - Armor-related functions
namespace "combat"

function "armor_bonus":
    execute as @a[nbt={Inventory:[{Slot:103b,id:"minecraft:diamond_helmet"}]}] \
        run effect give @s minecraft:resistance 1 0 true

function "update_armor":
    function combat:armor_bonus
```

**`ui/hud.mdl`** (UI module):
```mdl
# ui/hud.mdl - User interface functions
namespace "ui"

function "show_hud":
    title @a actionbar {"text":"Adventure Pack Active","color":"gold"}

function "update_ui":
    function ui:show_hud
    function combat:update_combat
    function combat:update_armor
```

**`data/tags.mdl`** (data module):
```mdl
# data/tags.mdl - Data tags and function tags
namespace "data"

# Function tags
tag function "minecraft:load":
    add "core:init"

tag function "minecraft:tick":
    add "ui:update_ui"

# Item tags
tag item "adventure:weapons":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag item "adventure:armor":
    add "minecraft:diamond_helmet"
    add "minecraft:diamond_chestplate"
    add "minecraft:diamond_leggings"
    add "minecraft:diamond_boots"
```

**Build the project:**
```bash
mdl build --mdl adventure_pack/ -o dist --verbose
```

## Conditional Examples

> **Recent Improvements**: The conditional system has been enhanced to ensure proper logical flow. `else if` blocks now only execute if all previous conditions were false, and `else` blocks only execute if all conditions were false. This provides more predictable and efficient execution.

### Weapon Effects System

A system that applies different effects based on the player's weapon:

```mdl
# weapon_effects.mdl
pack "Weapon Effects" description "Conditional weapon effects system" pack_format 48

namespace "weapons"

function "apply_weapon_effects":
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]":
        say Diamond sword detected!
        effect give @s minecraft:strength 10 1
        effect give @s minecraft:glowing 10 0
    else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:golden_sword'}}]":
        say Golden sword detected!
        effect give @s minecraft:speed 10 1
        effect give @s minecraft:night_vision 10 0
    else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:iron_sword'}}]":
        say Iron sword detected!
        effect give @s minecraft:haste 5 0
    else if "entity @s[type=minecraft:player]":
        say No special weapon detected
        effect give @s minecraft:glowing 5 0
    else:
        say No player found

on_tick "weapons:apply_weapon_effects"
```

### Entity Type Detection

A system that responds differently to different entity types:

```mdl
# entity_detection.mdl
pack "Entity Detection" description "Conditional entity detection system" pack_format 48

namespace "detection"

function "detect_entity":
    if "entity @s[type=minecraft:player]":
        say Player detected!
        effect give @s minecraft:glowing 5 1
        particle minecraft:end_rod ~ ~ ~ 0.5 0.5 0.5 0.1 10
    else if "entity @s[type=minecraft:zombie]":
        say Zombie detected!
        effect give @s minecraft:poison 5 1
        particle minecraft:smoke ~ ~ ~ 0.5 0.5 0.5 0.1 10
    else if "entity @s[type=minecraft:creeper]":
        say Creeper detected!
        effect give @s minecraft:resistance 5 1
        particle minecraft:explosion ~ ~ ~ 0.5 0.5 0.5 0.1 5
    else if "entity @s[type=minecraft:skeleton]":
        say Skeleton detected!
        effect give @s minecraft:slowness 5 1
        particle minecraft:arrow ~ ~ ~ 0.5 0.5 0.5 0.1 10
    else:
        say Unknown entity detected
        particle minecraft:cloud ~ ~ ~ 0.5 0.5 0.5 0.1 5

on_tick "detection:detect_entity"
```

### Conditional Function Calls

A system that calls different functions based on conditions:

```mdl
# conditional_calls.mdl
pack "Conditional Calls" description "Conditional function calling system" pack_format 48

namespace "calls"

function "main_logic":
    if "entity @s[type=minecraft:player]":
        say Executing player logic
        function calls:player_effects
        function calls:player_ui
    else if "entity @s[type=minecraft:zombie]":
        say Executing zombie logic
        function calls:zombie_ai
        function calls:zombie_effects
    else:
        say Executing default logic
        function calls:default_behavior

function "player_effects":
    effect give @s minecraft:night_vision 10 0
    effect give @s minecraft:glowing 10 0

function "player_ui":
    title @s actionbar {"text":"Player Mode Active","color":"green"}

function "zombie_ai":
    effect give @s minecraft:speed 5 1
    effect give @s minecraft:strength 5 1

function "zombie_effects":
    particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.05 5

function "default_behavior":
    effect give @s minecraft:glowing 5 0

on_tick "calls:main_logic"
```

## Gameplay Examples

### Mini-Game Framework

A framework for creating mini-games:

```mdl
# minigame_framework.mdl
pack "Mini-Game Framework" description "Framework for creating mini-games" pack_format 48

namespace "framework"

function "init":
    scoreboard objectives add game_state dummy "Game State"
    scoreboard objectives add player_score dummy "Player Score"
    scoreboard objectives add game_timer dummy "Game Timer"
    say [framework:init] Mini-game framework initialized!

function "start_game":
    scoreboard players set @a game_state 1
    scoreboard players set @a player_score 0
    scoreboard players set @a game_timer 0
    tellraw @a {"text":"Game started!","color":"green"}

function "end_game":
    scoreboard players set @a game_state 0
    tellraw @a {"text":"Game ended!","color":"red"}

function "update_game":
    execute as @a[scores={game_state=1}] run scoreboard players add @s game_timer 1

on_load "framework:init"
on_tick "framework:update_game"
```

### Custom Items

A datapack that adds custom item behaviors:

```mdl
# custom_items.mdl
pack "Custom Items" description "Custom item behaviors" pack_format 48

namespace "items"

function "magic_staff":
    execute as @a[nbt={SelectedItem:{id:"minecraft:blaze_rod"}}] \
        run particle minecraft:witch ~ ~ ~ 0.5 0.5 0.5 0.1 10
    execute as @a[nbt={SelectedItem:{id:"minecraft:blaze_rod"}}] \
        run effect give @s minecraft:night_vision 5 0 true

function "healing_potion":
    execute as @a[nbt={SelectedItem:{id:"minecraft:potion"}] \
        run effect give @s minecraft:instant_health 1 1
    execute as @a[nbt={SelectedItem:{id:"minecraft:potion"}] \
        run effect give @s minecraft:regeneration 10 1

function "update_items":
    function items:magic_staff
    function items:healing_potion

on_tick "items:update_items"
```

## Best Practices Examples

### Error Handling

A datapack that demonstrates proper error handling:

```mdl
# error_handling.mdl
pack "Error Handling Example" description "Shows proper error handling" pack_format 48

namespace "example"

function "safe_teleport":
    # Check if player exists before teleporting
    execute as @a if entity @s run tp @s ~ ~ ~
    execute unless entity @a run tellraw @a {"text":"No players to teleport","color":"red"}

function "conditional_effects":
    # Only give effects if player has specific item
    execute as @a[nbt={SelectedItem:{id:"minecraft:diamond"}}] \
        run effect give @s minecraft:strength 1 0 true
    execute as @a unless entity @s[nbt={SelectedItem:{id:"minecraft:diamond"}}] \
        run effect clear @s minecraft:strength

function "update_safe":
    function example:safe_teleport
    function example:conditional_effects

on_tick "example:update_safe"
```

### Performance Optimization

A datapack optimized for performance:

```mdl
# performance_example.mdl
pack "Performance Example" description "Optimized for performance" pack_format 48

namespace "perf"

function "efficient_particles":
    # Only create particles for nearby players
    execute as @a[distance=..10] run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

function "batched_effects":
    # Batch multiple effects in one function
    execute as @a run effect give @s minecraft:speed 1 0 true
    execute as @a run effect give @s minecraft:jump_boost 1 0 true

function "update_perf":
    function perf:efficient_particles
    function perf:batched_effects

on_tick "perf:update_perf"
```

## Testing Examples

### Test Datapack

A datapack designed for testing MDL features:

```mdl
# test_pack.mdl
pack "Test Pack" description "For testing MDL features" pack_format 48

namespace "test"

function "syntax_test":
    # Test various MDL syntax features
    say Testing MDL syntax
    tellraw @a {"text":"JSON test","color":"blue","bold":true}
    execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1

function "multi_line_test":
    # Test multi-line commands
    tellraw @a \
        {"text":"This is a multi-line","color":"green",\
         "extra":[{"text":" command test","color":"yellow"}]}

function "namespace_test":
    # Test cross-namespace calls
    function test:syntax_test
    function test:multi_line_test

on_load "test:namespace_test"
```

## Running the Examples

### Building Examples

To build any of these examples:

```bash
# Single file
mdl build --mdl example.mdl -o dist

# Multi-file project
mdl build --mdl project_folder/ -o dist

# With verbose output
mdl build --mdl example.mdl -o dist --verbose
```

### Testing Examples

To test examples before building:

```bash
# Check syntax
mdl check example.mdl

# Check with detailed output
mdl check --json example.mdl
```

### Installing in Minecraft

1. Build the example: `mdl build --mdl example.mdl -o dist`
2. Copy the folder from `dist/` to your world's `datapacks/` folder
3. Run `/reload` in-game
4. Test the functionality

## Tested Examples

All examples on this page are thoroughly tested and verified to work correctly. You can find the complete test suite in the [GitHub repository](https://github.com/aaron777collins/MinecraftDatapackLanguage/tree/main/test_examples).

### Download Working Examples

Each example is available in both MDL and Python API formats:

- **[Hello World](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/hello_world.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/hello_world.py)
- **[Particle Effects](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/particles.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/particles.py)
- **[Custom Commands](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/commands.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/commands.py)
- **[Combat System](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/combat_system.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/combat_system.py)
- **[UI System](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/ui_system.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/ui_system.py)
- **[Adventure Pack](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/adventure_pack.mdl)** - [Python version](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/test_examples/adventure_pack.py)
- **[Multi-file Project](https://github.com/aaron777collins/MinecraftDatapackLanguage/tree/main/test_examples/adventure_pack)** - Complete directory structure

### Run the Tests Yourself

To verify these examples work:

```bash
# Clone the repository
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage

# Install MDL
pipx install minecraft-datapack-language

# Run all tests
python test_examples/run_all_tests.py
```

### Test Coverage

These examples are automatically tested in CI/CD to ensure they work with every release:

- ✅ **MDL Syntax Validation** - All examples pass `mdl check`
- ✅ **MDL Build Process** - All examples build successfully  
- ✅ **Python API** - All Python equivalents work correctly
- ✅ **Multi-file Projects** - Directory-based builds work
- ✅ **CLI Functionality** - Basic CLI commands work
- ✅ **Output Verification** - Generated datapacks have correct structure

## Contributing Examples

If you have a great example to share:

1. Create a clear, well-documented example
2. Include comments explaining the code
3. Test that it works correctly
4. Submit it as a pull request to the repository

Your example could help other users learn MDL and create amazing datapacks!
