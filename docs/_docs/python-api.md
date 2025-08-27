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
