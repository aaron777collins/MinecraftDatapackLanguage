# test1

A simple hello world MDL (Minecraft Datapack Language) project.

## Documentation

- Full docs: https://aaron777collins.github.io/MinecraftDatapackLanguage/docs/
- Language quick reference: see `LANGUAGE_REFERENCE.md` in this folder

## What This Does

This simple datapack demonstrates:
- **Basic Output**: Uses `say` and `tellraw` commands to display messages
- **Variables**: A simple counter that increments each time the function runs
- **Variable Substitution**: Shows how to embed variables in text using `$variable$`
- **Load Hooks**: Automatically runs when the datapack loads in Minecraft

## Building

```bash
mdl build --mdl . --output dist
```

## Testing

1. Build the datapack: `mdl build --mdl . --output dist`
2. Copy the generated `dist` folder to your Minecraft world's `datapacks` folder
3. In Minecraft, run `/reload` to load the datapack
4. You should see the hello messages appear!

## What You'll See

When the datapack loads, you'll see:
- "Hello, Minecraft!" in chat
- A green "Welcome to my datapack!" message
- "Counter: 1" showing the variable substitution working

## Next Steps

Check out the full documentation for more advanced features like:
- Control structures (if/else, while loops)
- More complex variable operations
- Multi-file projects
- Registry types (recipes, loot tables, etc.)
