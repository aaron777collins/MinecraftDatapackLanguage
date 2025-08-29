# test_simplified_features

A simplified MDL (Minecraft Datapack Language) project demonstrating core features.

## Features Demonstrated

- **Number Variables**: Stored in scoreboard objectives
- **Variable Substitution**: Using `$variable$` syntax
- **Control Structures**: If/else statements and loops
- **For Loops**: Entity iteration with `@a` selector
- **While Loops**: Counter-based loops
- **Hooks**: Automatic execution with `on_tick`

## Building

```bash
mdl build --mdl . --output dist
```

## Simplified Syntax

This project uses the simplified MDL syntax:
- Only number variables (no strings or lists)
- Direct scoreboard integration with `$variable$`
- Simple control structures that actually work
- Focus on reliability over complexity

## Generated Commands

The compiler will generate:
- Scoreboard objectives for all variables
- Minecraft functions with proper control flow
- Hook files for automatic execution
- Pack metadata
