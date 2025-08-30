# MDL Language Quick Reference

For full documentation, visit: https://aaron777collins.github.io/MinecraftDatapackLanguage/docs/

## Basic Structure
```mdl
pack "my_pack" "Description" 82;
namespace "example";
```

## Variables
```mdl
var num counter = 0;
counter = counter + 1;
```

## Functions
```mdl
function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome!","color":"green"};
}
```

## Variable Substitution
```mdl
say Counter: $counter$;
```

## Hooks
```mdl
on_load "example:hello";  // Runs when datapack loads
on_tick "example:main";    // Runs every tick
```

## Output Commands
```mdl
say Hello World;                    // Simple text output
tellraw @a {"text":"Hello"};        // JSON text with formatting
```
