# test_color_project

A Minecraft datapack created with MDL (Minecraft Datapack Language).

## [GAME] About

This datapack was generated using the MDL CLI tool. MDL is a simplified language for creating Minecraft datapacks with clean, readable syntax.

## [DIR] Project Structure

```
test_color_project/
├── README.md              # This file
└── main.mdl              # Main MDL source file with basic hello world example
```

## [NEXT] Getting Started

### Prerequisites

- Minecraft Java Edition (1.20+ recommended)
- MDL CLI tool installed (`pipx install minecraft-datapack-language`)

### Building the Datapack

1. **Build the project:**
   ```bash
   mdl build --mdl main.mdl -o dist
   ```

2. **Check for errors:**
   ```bash
   mdl check main.mdl
   ```

3. **Install in Minecraft:**
   - Copy the `dist` folder to your world's `datapacks` directory
   - Or use the `--wrapper` option to create a zip file:
     ```bash
     mdl build --mdl main.mdl -o dist --wrapper test_color_project
     ```

### Using the Datapack

1. Load your world in Minecraft
2. The datapack will automatically load
3. Run the main function: `/function test_color_project:main`

## [OPT] Development

### Editing the Code

Open `main.mdl` in your favorite text editor. The file contains:

- **Pack declaration** - Datapack metadata
- **Namespace** - Datapack namespace for organization
- **Functions** - The main logic of your datapack
- **on_load hook** - Automatically runs when the datapack loads

### Key Features

- **Functions**: Define reusable code blocks with `function "name" { ... }`
- **Basic commands**: Use `say` and `tellraw` for player communication
- **Automatic loading**: The `on_load` hook runs your main function automatically
- **Clean syntax**: Simple, readable MDL syntax that compiles to Minecraft commands

### Example Code

```mdl
// Define a function
function "main" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome!","color":"green"};
}

// Hook it to run when loaded
on_load "test_color_project:main";
```

## [INFO] Resources

- **Language Reference**: https://www.mcmdl.com/docs/language-reference
- **CLI Reference**: https://www.mcmdl.com/docs/cli-reference
- **Examples**: https://www.mcmdl.com/docs/examples
- **Website**: https://www.mcmdl.com
- **GitHub**: https://github.com/aaron777collins/MinecraftDatapackLanguage

## 🐛 Troubleshooting

### Common Issues

1. **"No .mdl files found"**
   - Make sure you're in the correct directory
   - Check that the file has a `.mdl` extension

2. **Syntax errors**
   - Use `mdl check main.mdl` to find and fix errors
   - Check the error messages for line numbers and suggestions

3. **Datapack not loading**
   - Verify the pack format is correct for your Minecraft version
   - Check that the `dist` folder is in the right location

### Getting Help

- Check the error messages - they include helpful suggestions
- Visit the documentation: https://www.mcmdl.com/docs
- Report bugs: https://github.com/aaron777collins/MinecraftDatapackLanguage/issues

## [FILE] License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Happy coding! [GAME]
