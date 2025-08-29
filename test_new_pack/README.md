# test_new_pack

A simplified MDL (Minecraft Datapack Language) project demonstrating core features.

## Pack Format Information

This project uses **pack format 82** (Minecraft 1.21+) with the new directory structure:
- **Functions**: `data/<namespace>/function/` (not `functions/`)
- **Tags**: `data/minecraft/tags/function/` (not `functions/`)
- **Pack Metadata**: Uses `min_format` and `max_format` instead of `pack_format`

For Minecraft 1.20 and below, use pack format < 82 with legacy directory structure.

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
- Pack metadata with correct format for pack version 82+

## Pack Format Examples

### Post-82 (Minecraft 1.21+)
```mdl
pack "my_pack" "My datapack" 82;
// Uses: data/<namespace>/function/ and min_format/max_format
```

### Pre-82 (Minecraft 1.20 and below)
```mdl
pack "my_pack" "My datapack" 15;
// Uses: data/<namespace>/functions/ and pack_format
```
