# MDL Language Quick Reference

For full documentation, visit: https://aaron777collins.github.io/MinecraftDatapackLanguage/docs/

## Pack and Namespace
```mdl
pack "my_pack" "Description" 82;
namespace "example";
```

## Variables and Substitution
```mdl
var num counter = 0;
counter = $counter$ + 1;
say "Counter: $counter$";
```

## Functions
```mdl
function "main" {
    say "Hello";
}
```

## Control Flow
```mdl
if "$counter$ > 5" {
    say "High";
} else {
    say "Low";
}

while "$counter$ < 10" {
    counter = $counter$ + 1;
}
```

## Hooks
```mdl
on_load "example:init";
on_tick "example:main";
```
