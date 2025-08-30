#!/usr/bin/env python3

from minecraft_datapack_language.mdl_parser_js import parse_mdl_js

# Test the hook parsing
test_mdl = '''
// test1.mdl - Hello World Example
pack "test1" "A simple hello world datapack" 82;

namespace "test1";

// Simple counter variable
var num counter = 0;
var num tickcounter = 0;
var num timerenabled = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    
    // Regular MDL syntax for variable substitution
    tellraw @a {"text":"Counter: $counter$","color":"blue"};
    tellraw @a {"text":"Timerenabled: $timerenabled$","color":"blue"};
    
    // Raw text only for commands that contain MDL keywords
    $!raw
    say "To enable the timer, run /function test1:enabletimer"
    say "To disable the timer, run /function test1:disabletimer"
    raw!$
}

function "enabletimer" {
    timerenabled = 1;
    say Timer enabled;
}

function "disabletimer" {
    timerenabled = 0;
    say Timer disabled;
}

function "tick" {
    tickcounter = tickcounter + 1;
    if "$tickcounter$ > 100" {
        if "$timerenabled$ == 1" {
            function "test1:hello";
        }
        tickcounter = 0;
    }
}

// Hook to run hello function when datapack loads
on_load "test1:hello";
on_tick "test1:tick";
'''

ast = parse_mdl_js(test_mdl)
print("AST keys:", list(ast.keys()))
print("Hooks:", ast.get('hooks', []))
print("Functions:", [f.get('name', 'unknown') for f in ast.get('functions', [])])

# Simulate the hook processing logic
namespace = "test1"
load_functions = []
tick_functions = []

for hook in ast.get('hooks', []):
    function_name = hook['function_name']
    print(f"Processing hook: {hook}")
    
    # Skip hooks for function_name "load" as this is reserved for the global load function
    if function_name == "load":
        print(f"Skipping load function")
        continue
        
    # Check if function_name already contains a namespace (has a colon)
    if ':' in function_name:
        # Function name already includes namespace, use as-is
        full_function_name = function_name
    else:
        # Function name doesn't include namespace, add it
        full_function_name = f"{namespace}:{function_name}"
    
    print(f"Full function name: {full_function_name}")
    
    if hook['hook_type'] == "load":
        load_functions.append(full_function_name)
        print(f"Added to load_functions: {full_function_name}")
    elif hook['hook_type'] == "tick":
        tick_functions.append(full_function_name)
        print(f"Added to tick_functions: {full_function_name}")

print(f"Final load_functions: {load_functions}")
print(f"Final tick_functions: {tick_functions}")
