# Minecraft Datapack Language

This is a sample MDL (Minecraft Datapack Language) project.

## Usage

1. Build the datapack:
   ```bash
   mdl build --mdl minecraft_datapack_language.mdl -o dist
   ```

2. Copy the generated `dist` folder to your Minecraft world's `datapacks` directory.

3. Enable the datapack in-game with `/reload` and `/datapack enable`.

## Features

This sample demonstrates:
- Variable declarations and assignments
- List operations
- Control flow (if/else, while, for loops)
- Function calls
- String concatenation
- Arithmetic operations
- And more!

## Files

- `minecraft_datapack_language.mdl` - Main MDL source file
- `dist/` - Generated datapack (after building)
