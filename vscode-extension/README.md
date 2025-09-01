# Minecraft Datapack Language (MDL) - VSCode Extension

A comprehensive VSCode extension for the JavaScript-style MDL language, providing syntax highlighting, IntelliSense, snippets, and build tools for creating Minecraft datapacks.

## Features

### 🎨 Syntax Highlighting
- Full support for JavaScript-style MDL syntax
- Highlighting for all keywords, operators, and Minecraft commands
- Support for comments (`//` and `/* */`)
- Variable and function highlighting
- Entity selector highlighting (`@p`, `@r`, `@a`, `@e`, `@s`)

### 💡 IntelliSense & Auto-completion
- Smart completion for all MDL keywords
- Variable type suggestions (`num`, `str`, `list`)
- Control flow keywords (`if`, `else`, `while`, `for`, `switch`, `try`, `catch`)
- Minecraft command suggestions
- Entity selector completion
- Function and namespace completion

### 📝 Code Snippets
Comprehensive snippets for all MDL features:

#### Basic Structure
- `pack82` - Pack declaration with format 82
- `namespace` - Namespace declaration
- `function` - Function declaration

#### Variables
- `var` - Variable declaration
- `varnum` - Number variable
- `varstr` - String variable
- `varlist` - List variable

#### Control Flow
- `if` - If statement
- `ifelse` - If-else statement
- `ifelseif` - If-else if-else statement
- `while` - While loop
- `for` - For loop
- `switch` - Switch statement
- `trycatch` - Try-catch block

#### Error Handling
- `throw` - Throw statement
- `break` - Break statement
- `continue` - Continue statement
- `return` - Return statement

#### Minecraft Commands
- `say` - Say command
- `tellraw` - Tellraw command
- `effect` - Effect command
- `particle` - Particle command
- `execute` - Execute command
- `scoreboard` - Scoreboard command
- `function` - Function call

#### Lifecycle Hooks
- `ontick` - On tick hook
- `onload` - On load hook

#### Complete Examples
- `example` - Complete MDL example with all features

### 🛠️ Build Tools
- **MDL: Build current file** - Build the current MDL file to a datapack
- **MDL: Check Workspace** - Check all MDL files in the workspace
- **MDL: Create new project** - Create a new MDL project

### 🔧 Language Features
- Auto-closing brackets and quotes
- Smart indentation for blocks
- Code folding support
- Bracket matching
- Comment toggling

## Installation

1. Install the extension from the VSCode marketplace
2. Open any `.mdl` file to activate the extension
3. Start coding with full IntelliSense support!

## Usage

### Creating a New Project

1. Open the command palette (`Ctrl+Shift+P`)
2. Run "MDL: Create new project"
3. Enter project name and description
4. A new MDL project will be created

### Building a Datapack

1. Open an MDL file
2. Press `Ctrl+Shift+P` and run "MDL: Build current file"
3. Enter output directory
4. Your datapack will be built!

### Using Snippets

Type the snippet prefix and press `Tab` to expand:

```mdl
// Type 'pack82' and press Tab
pack "My Pack" description "Description" pack_format 82;

// Type 'function' and press Tab
function "my_function" {
    // Type 'say' and press Tab
    say Hello World;
}

// Type 'varnum' and press Tab
var num counter = 0;

// Type 'if' and press Tab
if "condition" {
    // commands
}
```

## Language Features

### Variables

```mdl
// Number variables (stored in scoreboard)
var num counter = 0;
var num health = 20;

// String variables (stored in NBT)
var str message = "Hello World";
var str player_name = "Steve";

// List variables (stored in multiple scoreboards)
var list items = ["sword", "shield", "potion"];
```

### Control Flow

```mdl
// If statements
if "entity @s[type=minecraft:player]" {
    say Player detected;
} else if "entity @s[type=minecraft:zombie]" {
    say Zombie detected;
} else {
    say Unknown entity;
}

// While loops
while "score @s counter matches 1.." {
    say Counter: @s counter;
    counter = counter - 1;
}

// For loops
for player in @a {
    effect give @s minecraft:speed 10 1;
}

// Switch statements
switch (counter) {
    case 1:
        say One;
        break;
    case 2:
        say Two;
        break;
    default:
        say Other;
        break;
}
```

### Error Handling

```mdl
try {
    say Trying operation;
    throw "error_message";
} catch (error) {
    say Caught error: error;
}
```

### Functions

```mdl
function "init" {
    say Initializing...;
    var num counter = 0;
    return counter;
}

function "tick" {
    counter = counter + 1;
    if "score @s counter matches 10" {
        say Counter reached 10!;
        counter = 0;
    }
}
```

### Lifecycle Hooks

```mdl
// Hook functions to Minecraft lifecycle
on_load "example:init";
on_tick "example:tick";
```

### Tags

```mdl
// Function tags
tag "function" "minecraft:load" values ["example:init"];
tag "function" "minecraft:tick" values ["example:tick"];

// Item tags
tag "item" "example:swords" values ["minecraft:diamond_sword", "minecraft:netherite_sword"];
```

## Keyboard Shortcuts

- `Ctrl+Shift+P` - Open command palette
- `Tab` - Expand snippets
- `Ctrl+/` - Toggle line comment
- `Shift+Alt+F` - Format document
- `Ctrl+Space` - Trigger suggestions

## Configuration

The extension automatically detects MDL files and provides appropriate syntax highlighting and IntelliSense. No additional configuration is required.

## Troubleshooting

### Extension Not Working
1. Make sure you have a `.mdl` file open
2. Check that the file extension is `.mdl`
3. Reload VSCode if needed

### Build Commands Not Working
1. Ensure MDL CLI is installed: `pip install minecraft-datapack-language`
2. Check that `mdl` command is available in your PATH
3. Verify your MDL syntax is correct

### IntelliSense Not Working
1. Make sure the file is saved with `.mdl` extension
2. Check that the language mode is set to "MDL"
3. Try reloading the window

## Contributing

This extension is part of the Minecraft Datapack Language project. Contributions are welcome!

## License

This extension is licensed under the same license as the main MDL project.

## Support

For issues and questions:
- Check the [MDL documentation](https://github.com/aaron777collins/MinecraftDatapackLanguage)
- Report issues on the GitHub repository
- Join the community discussions

---

**Happy coding with MDL! 🎮**
