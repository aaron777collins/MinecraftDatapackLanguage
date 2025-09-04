# <img src="https://github.com/aaron777collins/MinecraftDatapackLanguage/raw/main/icons/icon-128.png" width="32" height="32" alt="MDL Icon"> Minecraft Datapack Language (MDL)

A **modern, scope-aware language** that lets you write Minecraft datapacks with **explicit scoping, variables, control structures, and expressions** that actually work.

📖 **[View Full Documentation](https://www.mcmdl.com/)** - Complete guides, examples, and API reference  
📦 **[View on PyPI](https://pypi.org/project/minecraft-datapack-language/)** - Download and install from PyPI  
🔧 **[VS Code Extension](https://marketplace.visualstudio.com/items?itemName=mdl.minecraft-datapack-language)** - Syntax highlighting, IntelliSense, and snippets

![CI](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/CI/badge.svg)
![Documentation](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Build%20and%20Deploy%20Documentation/badge.svg)
![PyPI](https://img.shields.io/pypi/v/minecraft-datapack-language?style=flat-square)
![Release](https://github.com/aaron777collins/MinecraftDatapackLanguage/workflows/Release/badge.svg)

## 🎯 **MODERN** MDL Language with Explicit Scoping

**MDL uses a modern, scope-aware language format** with **explicit scoping, control structures, variables, and expressions**:

### ✨ **MODERN** Features
- **🎯 Explicit scoping** with angle brackets `<@s>`, `<@a[team=red]>` for all operations
- **📝 Modern comments** using `//` and `/* */`
- **🔢 Number variables** with `var num` type (stored in scoreboards)
- **🔄 Full control structures** including `if/else`, `while` loops
- **💲 Variable substitution** with `$variable<scope>$` syntax
- **🧮 Expressions** with arithmetic operations (`+`, `-`, `*`, `/`)
- **📦 Namespace system** for modular code organization
- **🏷️ Tag system** for all datapack resources (recipes, loot tables, advancements, etc.)
- **🎨 VS Code extension** with full IntelliSense and snippets
- **🧪 Comprehensive testing** with E2E validation
- **📚 Extensive documentation** with examples for every feature

### 🏗️ Core Features
- ✅ **Modern pack format 15** by default for latest Minecraft features
- ✅ **Explicit scoping** - every variable operation specifies its scope
- ✅ **Real control structures** - `if/else`, `while` loops
- ✅ **Number variables** stored in scoreboards with `$variable<scope>$` substitution
- ✅ **Expressions** with arithmetic operations and variable substitution
- ✅ **Multi-file projects** with automatic merging and dependency resolution
- ✅ **Variable optimization** - automatic load function generation for initialization
- ✅ **Selector optimization** - proper `@a` usage for system commands
- ✅ **Easy hooks** into `minecraft:tick` and `minecraft:load` via function tags
- ✅ **Tag support** for `recipe`, `loot_table`, `advancement`, `item_modifier`, `predicate`, and `structure`
- ✅ **Raw blocks** for direct Minecraft command injection
- ✅ **Say commands** that auto-convert to `tellraw` with JSON formatting

> **Note**: Version 1.0+ uses **pack_format 15** by default for the modern MDL syntax.

---

## 🚀 Install

### Option A — from PyPI (recommended for users)
Global, isolated CLI via **pipx**:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath    # reopen terminal
pipx install minecraft-datapack-language

mdl --help
```

Virtualenv (if you prefer):
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install minecraft-datapack-language
```

### Option B — from source (for contributors)
```bash
# inside the repo
python -m pip install -e .
```

---

## 🔄 Update

- **pipx**: `pipx upgrade minecraft-datapack-language`  
- **pip (venv)**: `pip install -U minecraft-datapack-language`  
- Pin a version: `pipx install "minecraft-datapack-language==<version>"` (replace `<version>` with desired version)

---

## 💻 CLI

### Modern MDL (v1.0+)
```bash
# Build MDL files
mdl build --mdl my_pack/mypack.mdl -o dist --wrapper mypack
mdl check my_pack/mypack.mdl

# Validate generated mcfunction files
mdl check my_pack/mypack.mdl

# Multi-file projects
mdl build --mdl my_pack/ -o dist      # Build entire directory
mdl build --mdl "file1.mdl file2.mdl" -o dist  # Build specific files

# Create new projects
mdl new my_awesome_pack
```

### Quick Start
```bash
# Create a new project
mdl new my_first_pack

# Build it
cd my_first_pack
mdl build --mdl main.mdl -o dist

# Check for errors
mdl check main.mdl
```

---

## 📝 Language Examples

### Basic Structure
```mdl
pack "MyPack" "My awesome datapack" 15;
namespace "game";

var num player_score<@s> = 0;
var num team_score<@a[team=red]> = 0;

function game:start<@s> {
    player_score<@s> = 100;
    say "Welcome! Your score is $player_score<@s>$";
}

on_load game:start<@s>;
```

### Control Structures
```mdl
function game:check_score<@s> {
    if $player_score<@s>$ > 10 {
        say "Great score!";
        player_score<@s> = $player_score<@s>$ + 5;
    } else {
        say "Keep trying!";
    }
    
    while $player_score<@s>$ < 100 {
        player_score<@s> = $player_score<@s>$ + 1;
    }
}
```

### Tags and Resources
```mdl
// Recipe tags
tag recipe "diamond_sword" "recipes/diamond_sword.json";
tag loot_table "epic_loot" "loot_tables/epic_loot.json";
tag advancement "first_spell" "advancements/first_spell.json";

// Item modifiers and predicates
tag item_modifier "enchanted_tool" "item_modifiers/enchanted_tool.json";
tag predicate "has_mana" "predicates/has_mana.json";
tag structure "wizard_tower" "structures/wizard_tower.json";
```

### Raw Blocks and Say Commands
```mdl
function game:special_effect<@s> {
    $!raw
    execute as @s run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
    execute as @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1
    raw!$
    
    say "Special effect triggered! Score: $player_score<@s>$";
}
```

---

## 🔧 Development

### Building from Source
```bash
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage
python -m pip install -e .
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_comprehensive_end_to_end.py

# Run with coverage
python -m pytest --cov=minecraft_datapack_language
```

### Building the Extension
```bash
cd vscode-extension
npm install
npm run compile
```

---

## 📚 Documentation

- **[Language Reference](docs/_docs/language-reference.md)** - Complete language specification
- **[VS Code Extension](vscode-extension/README.md)** - Extension documentation
- **[Examples](examples/)** - Sample projects and code snippets

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Minecraft community for inspiration
- Contributors and testers
- VS Code team for the excellent extension API

---

**Happy coding with MDL! 🎮**
