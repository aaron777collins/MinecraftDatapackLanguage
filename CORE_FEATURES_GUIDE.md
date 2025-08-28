# MDL Core Features Guide

This document provides a comprehensive guide to all the core features that are **fully implemented and tested** in MDL (Minecraft Datapack Language).

## ✅ **FULLY IMPLEMENTED & TESTED**

### 1. Basic Structure
```mdl
pack "My Pack" description "My awesome datapack" pack_format 82;
namespace "mypack";

function "main" {
    // Your code here
}
```

### 2. Variables
MDL supports three types of variables:

#### Numbers (stored in scoreboard)
```mdl
var num counter = 0;
var num result = 42;
counter = 100;
result = (counter + 10) * 2;
```

#### Strings (stored in NBT)
```mdl
var str message = "Hello, MDL!";
var str greeting = "Welcome";
message = "Updated message";
```

#### Lists (stored in NBT)
```mdl
var list items = ["sword", "shield", "potion"];
var list numbers = [1, 2, 3, 4, 5];
```

### 3. List Operations
All list operations are fully implemented:

#### Access Elements
```mdl
var str first_item = items[0];
var str second_item = items[1];
var num index = 2;
var str dynamic_item = items[index];
```

#### Modify Lists
```mdl
append items "axe";           // Add to end
insert items[1] "new_item";   // Insert at specific index
remove items[2];              // Remove by index
pop items;                    // Remove last element
clear items;                  // Clear entire list
```

#### List Information
```mdl
var num list_size = length(items);  // Get list length
```

### 4. Control Flow

#### If/Else Statements
```mdl
if "score @s counter > 40" {
    say "Counter is greater than 40";
    counter = counter - 10;
} else {
    say "Counter is 40 or less";
    counter = counter + 10;
}
```

#### While Loops
```mdl
while "score @s counter > 0" {
    say "Counter: " + counter;
    counter = counter - 1;
}
```

#### For Loops (Entity Iteration)
```mdl
for player in @a {
    tellraw @s {"text":"Hello player!","color":"blue"};
}
```

#### For-In Loops (List Iteration)
```mdl
for (var item in items) {
    say "Processing item: " + item;
}
```

### 5. Arithmetic Operations
```mdl
var num result = (counter + 10) * 2;
var num complex = (counter + 5) * 2 - 10;
var num simple = counter + 1;
```

### 6. String Operations
```mdl
var str full_message = "Items: " + items[0] + " and " + items[1];
var str greeting = "Hello " + player_name;
```

### 7. Basic Commands
```mdl
say "Hello, Minecraft!";
tellraw @a {"text":"Welcome!","color":"green"};
```

### 8. Functions
```mdl
function "main" {
    say "Main function called!";
}

function "helper" {
    say "Helper function called!";
    var num helper_var = 100;
    say "Helper value: " + helper_var;
}
```

### 9. Hooks
```mdl
on_load "mypack:main";
on_tick "mypack:helper";
```

### 10. Tags
```mdl
tag function minecraft:load {
    add "mypack:main";
}

tag function minecraft:tick {
    add "mypack:helper";
}
```

## 🧪 **Testing**

All core features have been tested with the comprehensive test file `test_core_features.mdl` which includes:

- ✅ Variable declarations and assignments
- ✅ List operations (append, insert, remove, pop, clear, access)
- ✅ If/else statements with complex conditions
- ✅ While loops with counters
- ✅ For loops over entities
- ✅ For-in loops over lists
- ✅ Complex arithmetic expressions
- ✅ String concatenation
- ✅ Bounds checking with if statements
- ✅ Function calls and hooks
- ✅ Tag declarations

## 📁 **Generated Output**

The compiler generates proper Minecraft datapack structure:

```
output/
├── pack.mcmeta
├── data/
│   ├── minecraft/
│   │   └── tags/
│   │       └── function/
│   │           ├── load.json
│   │           └── tick.json
│   └── [namespace]/
│       └── function/
│           ├── main.mcfunction
│           ├── helper.mcfunction
│           └── _global_vars.mcfunction
```

## 🔧 **How It Works**

### Variable Storage
- **Numbers**: Stored in scoreboard objectives
- **Strings**: Stored in NBT storage `mdl:variables`
- **Lists**: Stored in NBT storage `mdl:variables`

### Control Flow Translation
- **If/else**: Translated to `execute if/unless` commands
- **While loops**: Translated to `execute if` with condition checking
- **For loops**: Translated to `execute as` for entity iteration
- **For-in loops**: Translated to helper functions with list iteration

### Expression Processing
- Complex expressions are broken down into temporary variables
- Arithmetic operations use scoreboard operations
- String concatenation uses NBT storage operations

## 🎯 **Ready for Production**

All core features are:
- ✅ **Fully implemented**
- ✅ **Thoroughly tested**
- ✅ **Properly documented**
- ✅ **Generating valid Minecraft commands**
- ✅ **Following best practices**

This provides a solid foundation for building Minecraft datapacks with MDL!
