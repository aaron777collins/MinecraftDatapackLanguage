# Minecraft Datapack Language (MDL) - VSCode Extension

A comprehensive VSCode extension for the MDL language, providing syntax highlighting, IntelliSense, snippets, and build tools for creating Minecraft datapacks with explicit scoping and modern syntax.

## Features

### 🎨 Syntax Highlighting
- Full support for MDL syntax with explicit scoping
- Highlighting for all keywords, operators, and Minecraft commands
- Support for comments (`//` and `/* */`)
- Variable and function highlighting with scope selectors
- Entity selector highlighting (`@p`, `@r`, `@a`, `@e`, `@s`)
- **Explicit scope selector syntax highlighting** - Angle brackets `<@s>`, `<@a[team=red]>`, etc.
- Tag declaration highlighting for all resource types

### 💡 IntelliSense & Auto-completion
- Smart completion for all MDL keywords
- Variable type suggestions (`num`)
- **Explicit scope selector system support** - Complete scope syntax for variables and functions
- Control flow keywords (`if`, `else`, `while`)
- Minecraft command suggestions
- Entity selector completion
- Function and namespace completion
- Tag type completion (`recipe`, `loot_table`, `advancement`, etc.)

### 📝 Code Snippets
Comprehensive snippets for all MDL features:

#### Basic Structure
- `pack` - Pack declaration with metadata
- `namespace` - Namespace declaration
- `function` - Function declaration with scope

#### Variables
- `var` - Variable declaration with scope
- `assign` - Variable assignment with scope
- `varread` - Variable substitution with scope

#### Control Flow
- `if` - If statement with condition
- `ifelse` - If-else statement with condition
- `while` - While loop with condition

#### Functions and Execution
- `exec` - Execute function with scope
- `onload` - Hook that runs when datapack loads
- `ontick` - Hook that runs every tick

#### Tags and Resources
- `tagrecipe` - Recipe tag declaration
- `tagloot` - Loot table tag declaration
- `tagadvancement` - Advancement tag declaration
- `tagitemmod` - Item modifier tag declaration
- `tagpredicate` - Predicate tag declaration
- `tagstructure` - Structure tag declaration

#### Minecraft Commands
- `say` - Say command (auto-converts to tellraw)
- `sayvar` - Say command with variable substitution
- `raw` - Raw block for direct Minecraft commands
- `scoreboard` - Scoreboard operation command
- `execute` - Execute command with conditions
- `team` - Team management command
- `effect` - Apply status effect
- `particle` - Create particle effect
- `playsound` - Play sound effect
- `give` - Give item to player
- `tp` - Teleport entity
- `kill` - Kill entity
- `summon` - Summon entity

#### Comments and Documentation
- `comment` - Multi-line comment block
- `//` - Single line comment

### 🛠️ Build Tools
- **MDL: Build current file** - Build the current MDL file to a datapack
- **MDL: Check Workspace** - Check all MDL files in the workspace
- **MDL: Create new project** - Create a new MDL project

### 🔧 Language Features
- Auto-closing brackets, quotes, and angle brackets
- Smart indentation for blocks
- Code folding support
- Bracket matching
- Comment toggling

### 🎯 Explicit Scope Selector System
The extension provides comprehensive support for MDL's explicit scope selector system:

- **Variable Declaration Scopes**: `<@s>`, `<@a>`, `<@a[team=red]>`
- **Variable Assignment Scopes**: `variable<@s>`, `counter<@a>`, `score<@a[team=red]>`
- **Variable Substitution Scopes**: `$variable<@s>$`, `$counter<@a>$`
- **Function Call Scopes**: `exec namespace:func<@a>`
- **Hook Scopes**: `on_load namespace:func<@s>`
- **Team Scopes**: `<@a[team=red]>`, `<@a[team=blue]>`
- **Smart Completions**: Context-aware scope suggestions based on current code position

## Installation

### From VSCode Marketplace
1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Minecraft Datapack Language"
4. Click Install

### From VSIX File
1. Download the `.vsix` file from releases
2. In VSCode, go to Extensions
3. Click the "..." menu and select "Install from VSIX..."
4. Select the downloaded file

## Usage

### Creating a New MDL File
1. Create a new file with `.mdl` extension
2. The extension will automatically activate
3. Start typing to see syntax highlighting and IntelliSense

### Basic MDL Syntax
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

### Using Snippets
Type the snippet prefix and press Tab to expand:
- Type `pack` and press Tab for pack declaration
- Type `function` and press Tab for function declaration
- Type `var` and press Tab for variable declaration

### Building Datapacks
1. Open an MDL file
2. Press Ctrl+Shift+P to open command palette
3. Type "MDL: Build current file"
4. Enter output directory when prompted

## Language Features

### Explicit Scoping
Every variable operation in MDL requires explicit scope specification:
- **Reading**: `$variable<@s>$` - Read variable value from player scope
- **Writing**: `variable<@s> = value` - Write value to player scope
- **Functions**: `function namespace:name<@s> { ... }` - Function with scope

### Variable System
- **Types**: Currently supports `num` (number) variables
- **Storage**: Variables are stored in Minecraft scoreboard objectives
- **Scopes**: Each variable operation specifies its own scope
- **No Inheritance**: Functions don't inherit scope from caller

### Control Structures
- **If Statements**: `if condition { ... } else { ... }`
- **While Loops**: `while condition { ... }`
- **Conditions**: Use variable substitutions like `$score<@s>$ > 10`

### Hooks
- **on_load**: Runs when datapack loads
- **on_tick**: Runs every game tick
- Both support scope specification

### Tags
Support for all Minecraft datapack resource types:
- Recipes, loot tables, advancements
- Item modifiers, predicates, structures
- Automatic JSON file generation

### Raw Blocks
Use `$!raw ... raw!$` to insert raw Minecraft commands:
```mdl
$!raw
execute as @a run particle minecraft:explosion ~ ~ ~ 1 1 1 0 10
raw!$
```

## Configuration

### Language Settings
The extension automatically configures:
- File association for `.mdl` files
- Syntax highlighting rules
- IntelliSense providers
- Code snippets

### Customization
You can customize the extension behavior through VSCode settings:
- Indentation rules
- Bracket matching
- Auto-closing pairs

## Troubleshooting

### Extension Not Working
1. Ensure the file has `.mdl` extension
2. Check VSCode Extensions panel for errors
3. Reload VSCode window (Ctrl+Shift+P → "Developer: Reload Window")

### Syntax Highlighting Issues
1. Verify file extension is `.mdl`
2. Check for syntax errors in the file
3. Try reloading the VSCode window

### Build Issues
1. Ensure `mdl` command is available in PATH
2. Check MDL installation: `mdl --version`
3. Verify file syntax is correct

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- **Issues**: Report bugs on GitHub
- **Documentation**: See the main MDL documentation
- **Community**: Join our Discord server

## License

This extension is licensed under the same license as the main MDL project.

## Changelog

### v1.0.0
- Complete rewrite for new MDL language specification
- Explicit scope selector support
- Updated syntax highlighting and IntelliSense
- New snippets for all language features
- Tag system support
- Raw block support
- Hook system support

### v0.3.0 (Legacy)
- JavaScript-style MDL support
- Flexible scope selectors
- Legacy syntax features
