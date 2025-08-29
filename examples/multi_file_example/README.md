# Multi-File MDL Example

This example demonstrates the power of MDL's multi-file system with proper namespace separation. Each file represents a different module of functionality, and they all work together seamlessly.

## 📁 File Structure

```
multi_file_example/
├── test.mdl      # Core game logic
├── other.mdl     # Combat system
├── ui.mdl        # User interface
└── README.md     # This file
```

## 🚀 Building the Example

```bash
# Build all files together
mdl build --mdl . -o dist

# Or build individual files
mdl build --mdl test.mdl -o test_dist
mdl build --mdl other.mdl -o other_dist
mdl build --mdl ui.mdl -o ui_dist
```

## 📋 Generated Structure

After building, you'll get:

```
dist/
├── data/
│   ├── minecraft/
│   │   └── tags/
│   │       └── function/
│   │           ├── load.json    # Contains all load functions
│   │           └── tick.json    # Contains all tick functions
│   ├── test/                    # test.mdl namespace
│   │   └── function/
│   │       ├── main.mcfunction
│   │       ├── helper.mcfunction
│   │       └── health_check.mcfunction
│   ├── other/                   # other.mdl namespace
│   │   └── function/
│   │       ├── main.mcfunction
│   │       ├── combat.mcfunction
│   │       └── timer.mcfunction
│   └── ui/                      # ui.mdl namespace
│       └── function/
│           ├── main.mcfunction
│           ├── button_handler.mcfunction
│           └── animate.mcfunction
└── pack.mcmeta
```

## 🎯 Key Features Demonstrated

### 1. **Namespace Separation**
Each file has its own namespace, preventing function name conflicts:

```mdl
// test.mdl
namespace "test";
function "main" { ... }

// other.mdl  
namespace "other";
function "main" { ... }  // Different from test:main!

// ui.mdl
namespace "ui";
function "main" { ... }  // Different from both!
```

### 2. **Variable Declarations**
Variables are automatically initialized and managed:

```mdl
var num player_count = 0;
var num game_timer = 0;
var num player_score = 100;
var num health = 20;
```

### 3. **Control Structures**
Full JavaScript-like syntax with if/else, while loops:

```mdl
// If-else if-else chain
if "$enemy_count$ > 10" {
    say "Too many enemies!";
} else if "$enemy_count$ > 5" {
    say "Moderate enemy count: $enemy_count$";
} else {
    say "Few enemies: $enemy_count$";
}

// While loops
while "$game_timer$ < 5" {
    game_timer = $game_timer$ + 1;
    say "Timer: $game_timer$";
}
```

### 4. **Variable Substitution**
Use `$variable_name$` to substitute values in strings:

```mdl
say "Timer: $game_timer$";
tellraw @a [{"text":"Score: "},{"score":{"name":"@a","objective":"player_score"}}];
```

### 5. **Function Hooks**
Connect functions to Minecraft events:

```mdl
on_load "test:main";    // Runs when datapack loads
on_tick "other:main";   // Runs every tick
```

### 6. **Expressions**
Mathematical operations and comparisons:

```mdl
result = 5 + 3;
total_damage = $damage$ * 2;
if "$player_score$ > 50" { ... }
```

## 🔧 Advanced Features

### **Automatic Variable Initialization**
All variables are automatically initialized to 0 (or their specified value) in the global load function. No need to manually set up scoreboard objectives!

### **Smart Selector Handling**
- `say` commands automatically convert to `tellraw @a` for system messages
- `tellraw @a` commands are preserved as-is
- Server functions use armor stand selectors for reliable execution

### **Multi-File Merging**
When building multiple files:
- Functions are properly namespaced
- Variables are merged and initialized together
- Hooks are combined into appropriate tag files
- No conflicts between same-named functions in different namespaces

## 🎮 Usage in Minecraft

1. **Install the datapack** in your world's `datapacks` folder
2. **Enable it** with `/reload` or `/datapack enable multi_file_example`
3. **Watch the magic happen!** All functions will run automatically based on their hooks

## 🛠️ Development Workflow

1. **Edit individual files** for different features
2. **Build together** to test integration
3. **Deploy** the generated datapack
4. **Iterate** and improve!

## 📚 More Examples

Check out the other examples in the `examples/` directory:
- `hello_world.mdl` - Basic introduction
- `conditionals.mdl` - Control structures
- `loops.mdl` - Loop examples
- `variables.mdl` - Variable usage
- `namespaces.mdl` - Namespace examples

## 🚀 Next Steps

- Add more namespaces for different game systems
- Create complex interactions between modules
- Build a complete game with multiple MDL files
- Explore the full power of MDL's modern syntax!
