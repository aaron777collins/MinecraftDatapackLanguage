---
layout: page
title: Python API
permalink: /docs/python-api/
---

# Python API

The MDL Python API provides a clean, programmatic way to create Minecraft datapacks. It's fully compatible with the new JavaScript-style MDL language and supports all advanced features including variables, control flow, and complex nesting.

## Quick Start

```python
from minecraft_datapack_language import Pack

# Create a datapack
p = Pack("My Pack", "A cool datapack", 82)

# Add a namespace
ns = p.namespace("example")

# Add functions
ns.function("hello", "say Hello World!")
ns.function("welcome", "tellraw @a {\"text\":\"Welcome!\",\"color\":\"green\"}")

# Hook into Minecraft lifecycle
p.on_load("example:hello")
p.on_tick("example:welcome")

# Build the datapack
p.build("dist")
```

## Core Classes

### Pack

The main class for creating datapacks.

```python
from minecraft_datapack_language import Pack

# Create a pack
p = Pack(
    name="My Pack",           # Pack name
    description="Description", # Optional description
    pack_format=82            # Minecraft pack format (default: 82)
)
```

**Methods:**
- `namespace(name)` - Create a namespace
- `on_load(function_id)` - Hook function to world load
- `on_tick(function_id)` - Hook function to tick
- `tag(registry, name, values=[], replace=False)` - Create tags
- `build(output_dir)` - Build the datapack

### Namespace

Represents a namespace for organizing functions.

```python
ns = p.namespace("example")

# Add functions to the namespace
ns.function("function_name", "command1", "command2", ...)
```

**Methods:**
- `function(name, *commands)` - Add a function with commands

## Basic Examples

### Hello World

```python
from minecraft_datapack_language import Pack

def create_hello_world():
    p = Pack("Hello World", "A simple hello world datapack", 82)
    
    ns = p.namespace("example")
    ns.function("hello", 
        "say Hello, Minecraft!",
        "tellraw @a {\"text\":\"Welcome to my datapack!\",\"color\":\"green\"}"
    )
    
    # Hook into world load
    p.on_load("example:hello")
    
    return p

# Create and build
pack = create_hello_world()
pack.build("dist")
```

### Particle Effects

```python
from minecraft_datapack_language import Pack

def create_particle_pack():
    p = Pack("Particle Effects", "Creates particle effects around players", 82)
    
    ns = p.namespace("particles")
    
    ns.function("tick",
        "execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1",
        "execute as @a run particle minecraft:firework ~ ~ ~ 0.2 0.2 0.2 0.02 2"
    )
    
    ns.function("init", "say Particle effects enabled!")
    
    # Hook into lifecycle
    p.on_load("particles:init")
    p.on_tick("particles:tick")
    
    return p
```

## Advanced Features

### Variables and Control Flow

The Python API supports all the advanced features of the JavaScript-style MDL language:

```python
from minecraft_datapack_language import Pack

def create_advanced_pack():
    p = Pack("Advanced Features", "Demonstrates advanced features", 82)
    
    ns = p.namespace("advanced")
    
    # Functions with variables and control flow
    ns.function("variable_demo",
        "scoreboard players set @s counter 10",
        "scoreboard players add @s counter 5",
        "execute if score @s counter matches 15 run say Counter is 15!",
        "execute if score @s counter matches 15 run scoreboard players remove @s counter 5"
    )
    
    ns.function("control_flow_demo",
        "execute if entity @s[type=minecraft:player] run say Player detected",
        "execute if entity @s[type=minecraft:player] run effect give @s minecraft:glowing 5 1",
        "execute unless entity @s[type=minecraft:player] run say No player found"
    )
    
    ns.function("loop_demo",
        "scoreboard players set @s countdown 5",
        "execute if score @s countdown matches 1.. run function advanced:loop_body",
        "execute if score @s countdown matches 1.. run function advanced:loop_control"
    )
    
    # Loop body function
    ns.function("loop_body",
        "say Countdown: @s countdown",
        "scoreboard players remove @s countdown 1"
    )
    
    # Loop control function
    ns.function("loop_control",
        "execute if score @s countdown matches 1.. run function advanced:loop_body",
        "execute if score @s countdown matches 1.. run function advanced:loop_control"
    )
    
    p.on_tick("advanced:variable_demo")
    p.on_tick("advanced:control_flow_demo")
    p.on_tick("advanced:loop_demo")
    
    return p
```

### Function Calls and Cross-Namespace References

```python
from minecraft_datapack_language import Pack

def create_function_pack():
    p = Pack("Function Calls", "Demonstrates function calls", 82)
    
    # Core namespace
    core = p.namespace("core")
    core.function("init", "say Initializing...")
    core.function("tick", "say Tick...")
    
    # Utility namespace
    util = p.namespace("util")
    util.function("helper", "say Helper function")
    util.function("helper2", "say Another helper")
    
    # Main namespace with cross-namespace calls
    main = p.namespace("main")
    main.function("start",
        "say Starting...",
        "function core:init",
        "function util:helper"
    )
    
    main.function("update",
        "function core:tick",
        "function util:helper2"
    )
    
    # Lifecycle hooks
    p.on_load("main:start")
    p.on_tick("main:update")
    
    return p
```

### Tags and Data

```python
from minecraft_datapack_language import Pack

def create_tag_pack():
    p = Pack("Tags and Data", "Demonstrates tags and data", 82)
    
    ns = p.namespace("example")
    ns.function("init", "say Tags initialized!")
    
    # Function tags
    p.tag("function", "minecraft:load", values=["example:init"])
    p.tag("function", "minecraft:tick", values=["example:tick"])
    
    # Item tags
    p.tag("item", "example:swords", values=[
        "minecraft:diamond_sword",
        "minecraft:netherite_sword"
    ])
    
    # Block tags
    p.tag("block", "example:glassy", values=[
        "minecraft:glass",
        "minecraft:tinted_glass"
    ])
    
    return p
```

## Multi-Namespace Projects

```python
from minecraft_datapack_language import Pack

def create_complex_pack():
    p = Pack("Complex Pack", "Multi-namespace project", 82)
    
    # Core systems
    core = p.namespace("core")
    core.function("init", "say Core systems initialized")
    core.function("tick", "say Core tick")
    
    # Combat system
    combat = p.namespace("combat")
    combat.function("weapon_effects",
        "execute as @a[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 1 0 true"
    )
    combat.function("update_combat",
        "function core:tick",
        "function combat:weapon_effects"
    )
    
    # UI system
    ui = p.namespace("ui")
    ui.function("hud", "title @a actionbar {\"text\":\"Pack Active\",\"color\":\"gold\"}")
    ui.function("update_ui",
        "function ui:hud",
        "function combat:update_combat"
    )
    
    # Lifecycle hooks
    p.on_load("core:init")
    p.on_tick("ui:update_ui")
    
    return p
```

## Error Handling and Validation

```python
from minecraft_datapack_language import Pack

def create_safe_pack():
    p = Pack("Safe Pack", "Demonstrates error handling", 82)
    
    ns = p.namespace("safe")
    
    # Safe function calls
    ns.function("safe_teleport",
        "execute as @a if entity @s run tp @s ~ ~ ~",
        "execute unless entity @a run tellraw @a {\"text\":\"No players to teleport\",\"color\":\"red\"}"
    )
    
    # Conditional effects
    ns.function("conditional_effects",
        "execute as @a[nbt={SelectedItem:{id:'minecraft:diamond'}}] run effect give @s minecraft:strength 1 0 true",
        "execute as @a unless entity @s[nbt={SelectedItem:{id:'minecraft:diamond'}}] run effect clear @s minecraft:strength"
    )
    
    p.on_tick("safe:safe_teleport")
    p.on_tick("safe:conditional_effects")
    
    return p
```

## Building and Output

### Basic Build

```python
from minecraft_datapack_language import Pack

p = Pack("My Pack", "Description", 82)
ns = p.namespace("example")
ns.function("hello", "say Hello World")

# Build to directory
p.build("dist")
```

### Custom Output

```python
# Build with custom options
p.build("output_dir", wrapper="my_pack")
```

## Integration with MDL Files

You can use the Python API alongside MDL files:

```python
from minecraft_datapack_language import Pack
from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

def create_hybrid_pack():
    # Parse MDL file
    with open("my_functions.mdl", "r") as f:
        mdl_content = f.read()
    
    ast = parse_mdl_js(mdl_content)
    
    # Create pack via Python API
    p = Pack("Hybrid Pack", "Combines MDL and Python", 82)
    
    # Add functions from MDL
    for func in ast['functions']:
        ns = p.namespace(func.namespace)
        ns.function(func.name, *func.commands)
    
    # Add additional functions via Python API
    ns = p.namespace("python")
    ns.function("python_func", "say Created via Python API!")
    
    return p
```

## Best Practices

### 1. Organize by Namespace

```python
def create_organized_pack():
    p = Pack("Organized Pack", "Well-organized datapack", 82)
    
    # Core systems
    core = p.namespace("core")
    core.function("init", "say Initializing...")
    core.function("tick", "say Tick...")
    
    # Feature modules
    combat = p.namespace("combat")
    ui = p.namespace("ui")
    data = p.namespace("data")
    
    # Each namespace handles its own functionality
    return p
```

### 2. Use Function Composition

```python
def create_composable_pack():
    p = Pack("Composable Pack", "Uses function composition", 82)
    
    ns = p.namespace("example")
    
    # Small, focused functions
    ns.function("check_player", "execute if entity @s[type=minecraft:player]")
    ns.function("give_effect", "effect give @s minecraft:speed 10 1")
    ns.function("send_message", "tellraw @s {\"text\":\"Effect applied!\",\"color\":\"green\"}")
    
    # Compose functions
    ns.function("player_effects",
        "function example:check_player run function example:give_effect",
        "function example:check_player run function example:send_message"
    )
    
    return p
```

### 3. Error Handling

```python
def create_robust_pack():
    p = Pack("Robust Pack", "Handles errors gracefully", 82)
    
    ns = p.namespace("robust")
    
    # Always check conditions before operations
    ns.function("safe_operation",
        "execute if entity @a run say Players found",
        "execute unless entity @a run say No players found",
        "execute if entity @a run effect give @a minecraft:speed 5 1"
    )
    
    return p
```

## Complete Example

Here's a complete example that demonstrates all features:

```python
from minecraft_datapack_language import Pack

def create_complete_pack():
    """Create a complete datapack demonstrating all features."""
    
    # Create the pack
    p = Pack("Complete Example", "Demonstrates all MDL features", 82)
    
    # Core namespace
    core = p.namespace("core")
    core.function("init",
        "say [core:init] Initializing Complete Example...",
        "tellraw @a {\"text\":\"Complete Example loaded!\",\"color\":\"green\"}",
        "scoreboard objectives add example_counter dummy \"Example Counter\""
    )
    
    core.function("tick",
        "say [core:tick] Core systems running...",
        "execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1"
    )
    
    # Combat namespace
    combat = p.namespace("combat")
    combat.function("weapon_effects",
        "execute as @a[nbt={SelectedItem:{id:'minecraft:diamond_sword'}}] run effect give @s minecraft:strength 1 0 true",
        "execute as @a[nbt={SelectedItem:{id:'minecraft:golden_sword'}}] run effect give @s minecraft:speed 1 0 true"
    )
    
    combat.function("update_combat",
        "function core:tick",
        "function combat:weapon_effects"
    )
    
    # UI namespace
    ui = p.namespace("ui")
    ui.function("hud",
        "title @a actionbar {\"text\":\"Complete Example Active\",\"color\":\"gold\"}"
    )
    
    ui.function("update_ui",
        "function ui:hud",
        "function combat:update_combat"
    )
    
    # Data namespace
    data = p.namespace("data")
    data.function("setup_data",
        "say Setting up data..."
    )
    
    # Lifecycle hooks
    p.on_load("core:init")
    p.on_tick("ui:update_ui")
    
    # Function tags
    p.tag("function", "minecraft:load", values=["core:init"])
    p.tag("function", "minecraft:tick", values=["ui:update_ui"])
    
    # Data tags
    p.tag("item", "example:swords", values=[
        "minecraft:diamond_sword",
        "minecraft:netherite_sword"
    ])
    
    p.tag("block", "example:glassy", values=[
        "minecraft:glass",
        "minecraft:tinted_glass"
    ])
    
    return p

# Create and build the pack
if __name__ == "__main__":
    pack = create_complete_pack()
    pack.build("dist")
    print("Complete example pack built successfully!")
```

The Python API provides a powerful, flexible way to create Minecraft datapacks with full support for the JavaScript-style MDL language features.
