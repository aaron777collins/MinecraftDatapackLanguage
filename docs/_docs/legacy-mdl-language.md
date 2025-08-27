# Legacy MDL Language Reference (v9 and below)

> **⚠️ Legacy Format Notice**: This page documents the **old MDL language format** used in version 9 and below. For the new JavaScript-style MDL language (v10+), see the [Language Reference](language-reference.md).

The legacy MDL format used indentation-based blocks and a simpler syntax structure. This format is still supported for backward compatibility but is no longer actively developed.

## Legacy vs New Format

| Feature | Legacy (v9-) | New (v10+) |
|---------|-------------|------------|
| **Block syntax** | Indentation-based | Curly braces `{}` |
| **Statement termination** | Implicit | Semicolons `;` |
| **Comments** | `#` | `//` and `/* */` |
| **Variables** | Not supported | `var num/str/list` |
| **Control flow** | Basic if/while/for | Advanced with switch/try-catch |
| **Error handling** | Not supported | try-catch blocks |
| **Import system** | Not supported | import/from/as |
| **Pack format** | 48 | 82 |

## Legacy Syntax

### Comments
```mdl
# This is a legacy comment
# Comments start with # and continue to end of line
```

### Pack Declaration
```mdl
pack "My Pack" description "Description" pack_format 48
```

### Namespace Declaration
```mdl
namespace "example"
```

### Function Declaration
```mdl
function "my_function":
    say Hello World
    effect give @a minecraft:speed 10 1
```

### Control Flow

#### If Statements
```mdl
if "entity @s[type=minecraft:player]":
    say Player detected
else if "entity @s[type=minecraft:zombie]":
    say Zombie detected
else:
    say Unknown entity
```

#### While Loops
```mdl
while "score @s counter matches 1..":
    say Counter: @s counter
    scoreboard players remove @s counter 1
```

#### For Loops
```mdl
for player in @a:
    effect give @s minecraft:speed 10 1
    particle minecraft:cloud ~ ~ ~ 0.5 0.5 0.5 0.1 5
```

### Hooks
```mdl
on_tick "example:tick_function"
on_load "example:load_function"
```

### Tags
```mdl
tag function "minecraft:tick":
    add "example:tick_function"

tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"
```

## Legacy Examples

### Simple Legacy Pack
```mdl
pack "Legacy Example" description "Simple legacy pack" pack_format 48

namespace "example"

function "tick":
    for player in @a:
        if "entity @s[type=minecraft:player]":
            effect give @s minecraft:speed 5 0
        else:
            effect give @s minecraft:slowness 5 0

on_tick "example:tick"
```

### Legacy Multi-file Project
```mdl
# core.mdl
pack "Legacy Multi-file" description "Multi-file example" pack_format 48

namespace "core"

function "init":
    say Core initialized

# features.mdl
namespace "features"

function "feature1":
    say Feature 1 running

function "feature2":
    say Feature 2 running
```

## Migration to v10

To migrate from legacy MDL to the new JavaScript-style format:

### 1. Update Pack Declaration
```mdl
# Legacy
pack "My Pack" description "Description" pack_format 48

# New
pack "My Pack" description "Description" pack_format 82;
```

### 2. Update Comments
```mdl
# Legacy
# This is a comment

# New
// This is a comment
/* This is a block comment */
```

### 3. Update Function Blocks
```mdl
# Legacy
function "my_function":
    say Hello
    effect give @a minecraft:speed 10 1

# New
function "my_function" {
    say Hello;
    effect give @a minecraft:speed 10 1;
}
```

### 4. Update Control Flow
```mdl
# Legacy
if "condition":
    say True
else:
    say False

# New
if "condition" {
    say True;
} else {
    say False;
}
```

### 5. Update Hooks
```mdl
# Legacy
on_tick "example:tick"

# New
on_tick "example:tick";
```

## Legacy CLI Usage

For legacy projects, use pack-format 48:

```bash
# Build legacy MDL files
mdl build --mdl legacy_pack.mdl -o dist --pack-format 48

# Check legacy syntax
mdl check legacy_pack.mdl --pack-format 48
```

## Legacy Limitations

The legacy MDL format has several limitations compared to the new JavaScript-style format:

- **No variables**: Cannot declare or use variables
- **No advanced control flow**: No switch statements or try-catch blocks
- **No error handling**: No built-in error handling mechanisms
- **No import system**: Cannot import modules or functions
- **Limited nesting**: Complex nested structures can be difficult to read
- **No type system**: No support for different data types
- **No function parameters**: Functions cannot accept parameters
- **No return values**: Functions cannot return values

## When to Use Legacy Format

Consider using the legacy format only if:

1. **Existing projects**: You have existing v9- projects that you don't want to migrate
2. **Simple scripts**: You only need basic functionality
3. **Learning**: You're learning MDL and want to understand the evolution
4. **Compatibility**: You need to maintain compatibility with older tools

For all new projects, we strongly recommend using the new JavaScript-style MDL format (v10+).

## Support

If you need help with legacy MDL:

1. Check the [migration guide](migration-guide.md) for step-by-step instructions
2. Use the automatic migration tools provided with v10
3. Refer to the [legacy examples](legacy-examples.md) for working code
4. Report issues on the GitHub repository

---

**Next**: [Migration Guide](migration-guide.md) | [New Language Reference](language-reference.md)
