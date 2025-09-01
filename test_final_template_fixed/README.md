# test_final_template_fixed

A Minecraft datapack created with MDL (Minecraft Datapack Language).

## 🎮 About

This datapack was generated using the MDL CLI tool. MDL is a simplified language for creating Minecraft datapacks with variables, control structures, and easy syntax.

## 📁 Project Structure

```
test_final_template_fixed/
├── README.md              # This file
└── test_final_template_fixed.mdl    # Main MDL source file
```

## 🚀 Getting Started

### Prerequisites

- Minecraft Java Edition (1.20+ recommended)
- MDL CLI tool installed (`pipx install minecraft-datapack-language`)

### Building the Datapack

1. **Build the project:**
   ```bash
   mdl build --mdl test_final_template_fixed.mdl -o dist
   ```

2. **Check for errors:**
   ```bash
   mdl check test_final_template_fixed.mdl
   ```

3. **Install in Minecraft:**
   - Copy the `dist` folder to your world's `datapacks` directory
   - Or use the `--wrapper` option to create a zip file:
     ```bash
     mdl build --mdl test_final_template_fixed.mdl -o dist --wrapper test_final_template_fixed
     ```

### Using the Datapack

1. Load your world in Minecraft
2. The datapack will automatically load
3. Run the main function: `/function test_final_template_fixed:main`

## 🔧 Development

### Editing the Code

Open `test_final_template_fixed.mdl` in your favorite text editor. The file contains:

- **Pack declaration** - Datapack metadata
- **Variables** - Scoreboard variables for storing data
- **Functions** - The main logic of your datapack
- **Control structures** - If/else statements and loops
- **Raw commands** - Direct Minecraft commands when needed

### Key Features

- **Variables**: Use `variable name = value` to create scoreboard objectives
- **Functions**: Define reusable code blocks with `function name Ellipsis`
- **Conditionals**: Use `if (condition) Ellipsis else Ellipsis`
- **Loops**: Use `while (condition) Ellipsis` for repeating actions
- **Variable substitution**: Use `$variable$` in commands to insert values

### Example Code

```mdl
// Set a variable
score = 10

// Use it in a command
say "Your score is: $score$"

// Conditional logic
if (score > 5) {
  say "Great job!"
} else {
  say "Keep trying!"
}
```

## 📚 Resources

- **Language Reference**: https://mdl-lang.com/docs/language-reference
- **CLI Reference**: https://mdl-lang.com/docs/cli-reference
- **Examples**: https://mdl-lang.com/docs/examples
- **Website**: https://www.mcmdl.com
- **GitHub**: https://github.com/aaron777collins/MinecraftDatapackLanguage

## 🐛 Troubleshooting

### Common Issues

1. **"No .mdl files found"**
   - Make sure you're in the correct directory
   - Check that the file has a `.mdl` extension

2. **Syntax errors**
   - Use `mdl check test_final_template_fixed.mdl` to find and fix errors
   - Check the error messages for line numbers and suggestions

3. **Datapack not loading**
   - Verify the pack format is correct for your Minecraft version
   - Check that the `dist` folder is in the right location

### Getting Help

- Check the error messages - they include helpful suggestions
- Visit the documentation: https://mdl-lang.com/docs
- Report bugs: https://www.mcmdl.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Happy coding! 🎮
