---
layout: page
title: Python API
permalink: /docs/python-api/
---

# Python API

MDL provides a clean Python API for programmatically creating datapacks. This is useful for generating datapacks dynamically or integrating MDL into other tools.

## Basic Usage

### Creating a Pack

```python
from minecraft_datapack_language import Pack

# Create a new pack
pack = Pack(
    name="My Datapack",
    description="A datapack created with Python",
    pack_format=48
)
```

### Adding Functions

```python
# Create a namespace
example = pack.namespace("example")

# Add functions to the namespace
example.function("hello",
    'say Hello from Python!',
    'tellraw @a {"text":"Welcome!","color":"green"}'
)

example.function("tick",
    'execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1'
)
```

### Adding Lifecycle Hooks

```python
# Hook functions into Minecraft's lifecycle
pack.on_load("example:hello")
pack.on_tick("example:tick")
```

### Adding Tags

```python
# Function tags
pack.tag("function", "minecraft:load", values=["example:hello"])
pack.tag("function", "minecraft:tick", values=["example:tick"])

# Data tags
pack.tag("item", "example:swords", values=[
    "minecraft:diamond_sword",
    "minecraft:netherite_sword"
])
```

### Building the Pack

```python
# Build to a directory
pack.build("dist")

# Or get the pack object for further processing
pack_data = pack.to_dict()
```

## Complete Example

Here's a complete example that demonstrates all the features:

```python
from minecraft_datapack_language import Pack

def create_adventure_pack():
    # Create the main pack
    pack = Pack(
        name="Adventure Pack",
        description="A datapack created with Python API",
        pack_format=48
    )
    
    # Core namespace
    core = pack.namespace("core")
    core.function("init",
        'say [core:init] Initializing Adventure Pack...',
        'tellraw @a {"text":"Adventure Pack loaded!","color":"green"}'
    )
    
    core.function("tick",
        'say [core:tick] Core systems running...',
        'execute as @a run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1'
    )
    
    # Combat namespace
    combat = pack.namespace("combat")
    combat.function("weapon_effects",
        'say [combat:weapon_effects] Applying weapon effects...',
        'execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] run effect give @s minecraft:strength 1 0 true'
    )
    
    combat.function("update_combat",
        'function core:tick',
        'function combat:weapon_effects'
    )
    
    # UI namespace
    ui = pack.namespace("ui")
    ui.function("hud",
        'say [ui:hud] Updating HUD...',
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
    pack.tag("item", "example:swords", values=[
        "minecraft:diamond_sword",
        "minecraft:netherite_sword"
    ])
    
    pack.tag("block", "example:glassy", values=[
        "minecraft:glass",
        "minecraft:tinted_glass"
    ])
    
    return pack

# Create and build the pack
if __name__ == "__main__":
    pack = create_adventure_pack()
    pack.build("dist")
    print("Datapack built successfully!")
```

## API Reference

### Pack Class

The main class for creating datapacks.

#### Constructor

```python
Pack(name, description=None, pack_format=48)
```

**Parameters:**
- `name` (str): The name of the datapack
- `description` (str, optional): Description of the datapack
- `pack_format` (int, optional): Minecraft pack format (default: 48)

#### Methods

##### namespace(name)

Creates a new namespace and returns a `Namespace` object.

```python
namespace_obj = pack.namespace("example")
```

##### on_load(function_id)

Adds a function to run when the datapack loads.

```python
pack.on_load("example:init")
```

##### on_tick(function_id)

Adds a function to run every tick.

```python
pack.on_tick("example:tick")
```

##### tag(registry, tag_name, values=None, replace=False)

Creates a tag in the specified registry.

```python
pack.tag("function", "minecraft:load", values=["example:init"])
pack.tag("item", "example:swords", values=["minecraft:diamond_sword"])
```

**Parameters:**
- `registry` (str): The registry type (`function`, `item`, `block`, etc.)
- `tag_name` (str): The name of the tag
- `values` (list, optional): List of values to add to the tag
- `replace` (bool, optional): Whether to replace existing tag (default: False)

##### build(output_dir, wrapper_name=None)

Builds the datapack to the specified directory.

```python
pack.build("dist", wrapper_name="mypack")
```

**Parameters:**
- `output_dir` (str): Directory to output the datapack
- `wrapper_name` (str, optional): Name for the wrapper folder/zip

##### to_dict()

Returns the pack data as a dictionary.

```python
pack_data = pack.to_dict()
```

### Namespace Class

Represents a namespace within a datapack.

#### Methods

##### function(name, *commands)

Creates a function with the specified commands.

```python
namespace.function("hello",
    'say Hello!',
    'tellraw @a {"text":"Welcome","color":"green"}'
)
```

**Parameters:**
- `name` (str): The function name
- `*commands` (str): Variable number of command strings

## Advanced Usage

### Dynamic Function Generation

You can generate functions dynamically based on data:

{% raw %}
```python
def create_weapon_functions(pack, weapons):
    combat = pack.namespace("combat")
    
    for weapon in weapons:
        combat.function(f"{weapon['name']}_effects",
            f'execute as @a[nbt={{SelectedItem:{{id:"{weapon["id"]}"}}}}] run effect give @s {weapon["effect"]} 1 0 true'
        )

# Usage
weapons = [
    {"name": "diamond_sword", "id": "minecraft:diamond_sword", "effect": "minecraft:strength"},
    {"name": "golden_sword", "id": "minecraft:golden_sword", "effect": "minecraft:speed"}
]

create_weapon_functions(pack, weapons)
```
{% endraw %}

### Conditional Logic

> **Enhanced Implementation**: The conditional system now ensures proper logical flow where `else if` conditions only execute if all previous conditions were false, and `else` blocks only execute if all conditions were false.

You can use Python logic to conditionally add features:

```python
def create_feature_pack(features):
    pack = Pack(name="Feature Pack", pack_format=48)
    
    if "combat" in features:
        combat = pack.namespace("combat")
        combat.function("weapon_effects", 'say Combat enabled!')
        pack.on_tick("combat:weapon_effects")
    
    if "ui" in features:
        ui = pack.namespace("ui")
        ui.function("hud", 'title @a actionbar {"text":"UI Active"}')
        pack.on_tick("ui:hud")
    
    return pack

# Usage
pack = create_feature_pack(["combat", "ui"])
pack.build("dist")
```

### Implementing Conditional Logic

While MDL files support native if/else if/else syntax, you can implement the same logic using the Python API with execute commands:

```python
def create_conditional_pack():
    pack = Pack(name="Conditional Example", pack_format=48)
    ns = pack.namespace("test")
    
    # Create the main function with conditional logic
    ns.function("weapon_effects",
        "execute if entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] run function test:diamond_effects",
        "execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] if entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}] run function test:golden_effects",
        "execute unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}] unless entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}] if entity @s[type=minecraft:player] run function test:default_effects"
    )
    
    # Create the conditional function implementations
    ns.function("diamond_effects",
        "say Diamond sword detected!",
        "effect give @s minecraft:strength 10 1"
    )
    
    ns.function("golden_effects",
        "say Golden sword detected!",
        "effect give @s minecraft:speed 10 1"
    )
    
    ns.function("default_effects",
        "say Default weapon detected",
        "effect give @s minecraft:haste 5 0"
    )
    
    pack.on_tick("test:weapon_effects")
    return pack
```

This is equivalent to the MDL syntax:

```mdl
function "weapon_effects":
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:diamond_sword\"}}]":
        say Diamond sword detected!
        effect give @s minecraft:strength 10 1
    else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:\"minecraft:golden_sword\"}}]":
        say Golden sword detected!
        effect give @s minecraft:speed 10 1
    else if "entity @s[type=minecraft:player]":
        say Default weapon detected
        effect give @s minecraft:haste 5 0
```

### Advanced Conditional Examples

Here are more comprehensive examples of implementing conditional logic with the Python API:

```python
def create_advanced_conditional_pack():
    pack = Pack(name="Advanced Conditional Example", pack_format=48)
    ns = pack.namespace("advanced")
    
    # Entity type detection with multiple conditions
    ns.function("entity_detection",
        "execute if entity @s[type=minecraft:player] run function advanced:player_logic",
        "execute unless entity @s[type=minecraft:player] if entity @s[type=minecraft:zombie] run function advanced:zombie_logic",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] if entity @s[type=minecraft:creeper] run function advanced:creeper_logic",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] unless entity @s[type=minecraft:creeper] run function advanced:unknown_logic"
    )
    
    # Player logic
    ns.function("player_logic",
        "say Player detected!",
        "effect give @s minecraft:glowing 5 1",
        "tellraw @a {\"text\":\"A player is nearby!\",\"color\":\"green\"}"
    )
    
    # Zombie logic
    ns.function("zombie_logic",
        "say Zombie detected!",
        "effect give @s minecraft:poison 5 1",
        "tellraw @a {\"text\":\"A zombie is nearby!\",\"color\":\"red\"}"
    )
    
    # Creeper logic
    ns.function("creeper_logic",
        "say Creeper detected!",
        "effect give @s minecraft:resistance 5 1",
        "tellraw @a {\"text\":\"A creeper is nearby!\",\"color\":\"dark_red\"}"
    )
    
    # Unknown entity logic
    ns.function("unknown_logic",
        "say Unknown entity detected",
        "tellraw @a {\"text\":\"Something unknown is nearby...\",\"color\":\"gray\"}"
    )
    
    pack.on_tick("advanced:entity_detection")
    return pack
```

### Conditional with Function Calls

You can create complex conditional systems that call different functions based on conditions:

```python
def create_conditional_function_calls():
    pack = Pack(name="Conditional Function Calls", pack_format=48)
    ns = pack.namespace("calls")
    
    # Main logic function with conditional calls
    ns.function("main_logic",
        "execute if entity @s[type=minecraft:player] run function calls:execute_player_logic",
        "execute unless entity @s[type=minecraft:player] if entity @s[type=minecraft:zombie] run function calls:execute_zombie_logic",
        "execute unless entity @s[type=minecraft:player] unless entity @s[type=minecraft:zombie] run function calls:execute_default_logic"
    )
    
    # Player logic execution
    ns.function("execute_player_logic",
        "say Executing player logic",
        "function calls:player_effects",
        "function calls:player_ui"
    )
    
    # Zombie logic execution
    ns.function("execute_zombie_logic",
        "say Executing zombie logic",
        "function calls:zombie_ai",
        "function calls:zombie_effects"
    )
    
    # Default logic execution
    ns.function("execute_default_logic",
        "say Executing default logic",
        "function calls:default_behavior"
    )
    
    # Individual logic functions
    ns.function("player_effects",
        "effect give @s minecraft:night_vision 10 0",
        "effect give @s minecraft:speed 5 0"
    )
    
    ns.function("player_ui",
        "title @s actionbar {\"text\":\"Player Mode Active\",\"color\":\"green\"}"
    )
    
    ns.function("zombie_ai",
        "effect give @s minecraft:slowness 5 0",
        "particle minecraft:smoke ~ ~ ~ 0.5 0.5 0.5 0.1 10"
    )
    
    ns.function("zombie_effects",
        "effect give @s minecraft:poison 5 0"
    )
    
    ns.function("default_behavior",
        "say No special logic for this entity type"
    )
    
    pack.on_tick("calls:main_logic")
    return pack
```

### Dynamic Conditional Generation

You can generate conditional logic dynamically based on configuration:

```python
def create_dynamic_conditional_pack(weapon_configs):
    pack = Pack(name="Dynamic Conditional Example", pack_format=48)
    ns = pack.namespace("dynamic")
    
    # Generate execute commands for each weapon
    execute_commands = []
    for i, weapon in enumerate(weapon_configs):
        if i == 0:
            # First condition
            execute_commands.append(
                f"execute if entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"{weapon['id']}\"}}}}] run function dynamic:{weapon['name']}_effects"
            )
        else:
            # Subsequent conditions need unless clauses
            unless_clauses = " ".join([
                f"unless entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"{prev_weapon['id']}\"}}}}]"
                for prev_weapon in weapon_configs[:i]
            ])
            execute_commands.append(
                f"execute {unless_clauses} if entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"{weapon['id']}\"}}}}] run function dynamic:{weapon['name']}_effects"
            )
    
    # Add default case
    unless_clauses = " ".join([
        f"unless entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"{weapon['id']}\"}}}}]"
        for weapon in weapon_configs
    ])
    execute_commands.append(
        f"execute {unless_clauses} if entity @s[type=minecraft:player] run function dynamic:default_effects"
    )
    
    # Create main function
    ns.function("weapon_effects", *execute_commands)
    
    # Create effect functions for each weapon
    for weapon in weapon_configs:
        ns.function(f"{weapon['name']}_effects",
            f"say {weapon['name'].title()} detected!",
            f"effect give @s {weapon['effect']} 10 1"
        )
    
    # Create default effects
    ns.function("default_effects",
        "say No special weapon detected",
        "effect give @s minecraft:haste 5 0"
    )
    
    pack.on_tick("dynamic:weapon_effects")
    return pack

# Usage
weapons = [
    {"name": "diamond_sword", "id": "minecraft:diamond_sword", "effect": "minecraft:strength"},
    {"name": "golden_sword", "id": "minecraft:golden_sword", "effect": "minecraft:speed"},
    {"name": "iron_sword", "id": "minecraft:iron_sword", "effect": "minecraft:haste"}
]

pack = create_dynamic_conditional_pack(weapons)
pack.build("dist")
```

### Conditional with Complex NBT Data

For complex NBT conditions, you can create helper functions:

```python
def create_complex_nbt_conditional():
    pack = Pack(name="Complex NBT Conditional", pack_format=48)
    ns = pack.namespace("nbt")
    
    # Complex NBT conditions
    ns.function("item_detection",
        "execute if entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:diamond_sword\",Count:1b}]}] run function nbt:diamond_sword_effects",
        "execute unless entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:diamond_sword\",Count:1b}]}] if entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:golden_sword\",Count:1b}]}] run function nbt:golden_sword_effects",
        "execute unless entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:diamond_sword\",Count:1b}]}] unless entity @s[type=minecraft:player,nbt={Inventory:[{Slot:0b,id:\"minecraft:golden_sword\",Count:1b}]}] if entity @s[type=minecraft:player] run function nbt:default_effects"
    )
    
    ns.function("diamond_sword_effects",
        "say Player has diamond sword in first slot!",
        "effect give @s minecraft:strength 10 1"
    )
    
    ns.function("golden_sword_effects",
        "say Player has golden sword in first slot!",
        "effect give @s minecraft:speed 10 1"
    )
    
    ns.function("default_effects",
        "say Player has no special sword",
        "effect give @s minecraft:haste 5 0"
    )
    
    pack.on_tick("nbt:item_detection")
    return pack
```

### Integration with CLI

You can use the Python API with the CLI for building:

```python
from minecraft_datapack_language.cli import main as cli_main

def build_from_python():
    # Create your pack using the Python API
    pack = create_my_pack()
    
    # Use CLI to build it
    cli_main(['build', '--py-object', 'my_module:create_my_pack', '-o', 'dist'])

# In your module file (my_module.py)
def create_my_pack():
    pack = Pack(name="My Pack", pack_format=48)
    # ... add functions, etc.
    return pack
```

## Error Handling

The Python API provides clear error messages for common issues:

```python
try:
    pack = Pack(name="My Pack")
    example = pack.namespace("example")
    
    # This will raise an error if the function name is invalid
    example.function("invalid-name", 'say Hello')
    
except ValueError as e:
    print(f"Error: {e}")
```

## Best Practices

### Organization

- Create separate functions for different features
- Use descriptive namespace and function names
- Group related functionality together

### Reusability

- Create factory functions for common patterns
- Use configuration dictionaries for customizable packs
- Separate data from logic

### Error Prevention

- Validate input data before creating functions
- Use type hints for better code clarity
- Test your pack generation with `mdl check`

### Performance

- For large packs, consider using generators for command lists
- Reuse namespace objects when adding multiple functions
- Use list comprehensions for bulk operations

## Integration Examples

### Web Application

```python
from flask import Flask, request
from minecraft_datapack_language import Pack

app = Flask(__name__)

@app.route('/generate-pack', methods=['POST'])
def generate_pack():
    data = request.json
    
    pack = Pack(name=data['name'], pack_format=48)
    
    for feature in data['features']:
        namespace = pack.namespace(feature['namespace'])
        namespace.function(feature['name'], *feature['commands'])
    
    pack.build("temp_packs")
    return {"status": "success", "path": "temp_packs"}
```

### Configuration-Driven

```python
import yaml
from minecraft_datapack_language import Pack

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def create_pack_from_config(config):
    pack = Pack(
        name=config['name'],
        description=config.get('description'),
        pack_format=config.get('pack_format', 48)
    )
    
    for namespace_config in config['namespaces']:
        namespace = pack.namespace(namespace_config['name'])
        
        for function_config in namespace_config['functions']:
            namespace.function(
                function_config['name'],
                *function_config['commands']
            )
    
    return pack

# Usage
config = load_config('pack_config.yaml')
pack = create_pack_from_config(config)
pack.build("dist")
```
