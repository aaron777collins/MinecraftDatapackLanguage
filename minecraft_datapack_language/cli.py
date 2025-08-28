
import argparse, os, sys, json, traceback, re, zipfile, shutil, glob
from typing import Dict, Any, List
from .pack import Pack, Function
from .utils import ensure_dir
from .mdl_parser_js import parse_mdl_js
from .expression_processor import expression_processor, ProcessedExpression
from . import __version__

def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9._-]+', '-', s)
    return s or "pack"

def _zip_dir(src_dir: str, zip_path: str):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                abs_path = os.path.join(root, f)
                rel = os.path.relpath(abs_path, src_dir)
                zf.write(abs_path, rel)

def _gather_mdl_files(path: str):
    """Gather MDL files from a path. Supports:
    - Directory: recursively finds all .mdl files
    - Single file: returns just that file
    - Space-separated file list: returns all specified files
    """
    # Check if it's a space-separated list of files
    if ' ' in path and not os.path.exists(path):
        files = path.split()
        # Validate each file exists
        for f in files:
            if not os.path.isfile(f):
                raise SystemExit(f"File not found: {f}")
        return files
    
    if os.path.isdir(path):
        files = [p for p in glob.glob(os.path.join(path, "**", "*.mdl"), recursive=True)]
        # Sort files, but prioritize files with pack declarations
        def sort_key(f):
            # Check if file has a pack declaration
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                    has_pack = any(line.strip().startswith("pack ") for line in content.splitlines())
                    # Files with pack declarations come first (lower sort key)
                    return (0 if has_pack else 1, f)
            except:
                # If we can't read the file, treat it as a regular file
                return (1, f)
        
        return sorted(files, key=sort_key)
    elif os.path.isfile(path):
        return [path]
    else:
        raise SystemExit(f"Path not found: {path}")

def _parse_many(files, default_pack_format: int, verbose: bool = False):
    root_pack = None
    if verbose:
        print(f"Processing {len(files)} MDL file(s)...")
    
    for i, fp in enumerate(files, 1):
        if verbose:
            print(f"  [{i}/{len(files)}] {fp}")
        with open(fp, "r", encoding="utf-8") as f:
            src = f.read()
        
        # Check if this file has a pack declaration
        has_pack_declaration = any(line.strip().startswith("pack ") for line in src.splitlines())
        
        if has_pack_declaration and root_pack is not None:
            raise RuntimeError(f"{fp}: duplicate pack declaration (only the first file should have a pack declaration)")
        
        try:
            # Parse with JavaScript-style parser
            ast = parse_mdl_js(src)
            
            # Convert AST to Pack object
            p = _ast_to_pack(ast, default_pack_format)
        except Exception as e:
            # Bubble up with filename context
            raise RuntimeError(f"{fp}: {e}")
        
        if root_pack is None:
            root_pack = p
            if verbose:
                print(f"    Using pack: {p.name} (format: {p.pack_format})")
        else:
            # Ensure consistent pack_format; prefer explicit default
            if p.pack_format != root_pack.pack_format and default_pack_format is not None:
                p.pack_format = default_pack_format
            if verbose:
                print(f"    Merging into: {root_pack.name}")
            root_pack.merge(p)
    
    if root_pack is None:
        raise SystemExit("No .mdl files found")
    
    if verbose:
        print(f"Successfully merged {len(files)} file(s) into datapack: {root_pack.name}")
    return root_pack

def cmd_new(args):
    # Create a sample project
    root = os.path.abspath(args.path)
    
    # Check if the path already exists
    if os.path.exists(root):
        print(f"ERROR: Path {root} already exists")
        return 1
    
    # Create the directory
    ensure_dir(root)
    
    # Create the pack declaration separately to avoid f-string issues with array literals
    pack_declaration = 'pack "{}" description "Example datapack" pack_format {} min_format [{}, 0] max_format [{}, 1] min_engine_version "1.21.4";'.format(args.name, args.pack_format, args.pack_format, args.pack_format)
    
    sample = """// mypack.mdl - Advanced example showcasing ALL MDL features
""" + pack_declaration + """
namespace "example";

// Global state variables
var num global_counter = 0;
var str global_message = "System Ready";
var list global_numbers = [1, 2, 3, 4, 5];
var list global_strings = ["apple", "banana", "cherry"];

function "inner" {
    say [example:inner] This is the inner function;
    tellraw @a {"text":"Running inner","color":"yellow"};
}

function "hello" {
    say [example:hello] Outer says hi;
    function example:inner;
    tellraw @a {"text":"Back in hello","color":"aqua"};
}

// Advanced variable operations with all data types
function "variable_demo" {
    var num local_counter = 10;
    var str player_name = "Steve";
    var list local_items = ["sword", "shield", "potion"];
    
    // Number operations
    local_counter = local_counter + 5;
    global_counter = global_counter + 1;
    
    // String operations
    player_name = "Alex";
    global_message = "Updated: " + player_name;
    var str full_name = player_name + " Minecraft";
    
    // List operations
    local_items.append("bow");
    local_items.insert(1, "armor");
    var num first_item = local_items[0];
    var num item_count = local_items.length;
    
    // Complex calculations
    var num result = (local_counter * 2) + global_counter;
    var num modulo_result = result % 7;
    
    // String concatenation with variables
    var str status = player_name + " has " + item_count + " items";
    
    say Variable demo complete;
    tellraw @s {"text":"Result: " + result};
    tellraw @s {"text":"Modulo: " + modulo_result};
    tellraw @s {"text":"Status: " + status};
}

// Advanced conditional logic with nested structures
function "conditional_demo" {
    var num player_level = 15;
    var str player_class = "warrior";
    var num experience = 75;
    
    if "score @s player_level >= 10" {
        if "score @s player_class == 'warrior'" {
            if "score @s experience >= 50" {
                say Advanced warrior detected!;
                effect give @s minecraft:strength 10 2;
                effect give @s minecraft:glowing 10 0;
            } else {
                say Novice warrior;
                effect give @s minecraft:haste 10 0;
            }
        } else if "score @s player_class == 'mage'" {
            say Advanced mage detected!;
            effect give @s minecraft:night_vision 10 0;
            effect give @s minecraft:levitation 5 0;
        } else {
            say Unknown advanced class;
            effect give @s minecraft:glowing 10 0;
        }
    } else if "score @s player_level >= 5" {
        say Intermediate player;
        effect give @s minecraft:speed 10 0;
    } else {
        say Beginner player;
        effect give @s minecraft:jump_boost 10 0;
    }
}

// Advanced weapon effects with list operations
function "weapon_effects" {
    var list weapons = ["diamond_sword", "golden_sword", "bow"];
    var num weapon_index = 0;
    
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
        weapon_index = 0;
        say Diamond sword detected!;
        effect give @s minecraft:strength 10 1;
        effect give @s minecraft:glowing 10 0;
    } else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:golden_sword'}}]" {
        weapon_index = 1;
        say Golden sword detected!;
        effect give @s minecraft:speed 10 1;
        effect give @s minecraft:night_vision 10 0;
    } else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:bow'}}]" {
        weapon_index = 2;
        say Bow detected!;
        effect give @s minecraft:jump_boost 10 1;
    } else if "entity @s[type=minecraft:player]" {
        say Player without special weapon;
        effect give @s minecraft:haste 5 0;
    } else {
        say No player found;
    }
    
    // Use list to get weapon name
    if "score @s weapon_index < weapons.length" {
        var str current_weapon = weapons[weapon_index];
        tellraw @s {"text":"Using weapon: " + current_weapon};
    }
}

// Advanced loop patterns with break and continue
function "loop_demo" {
    var num outer_count = 0;
    var num inner_count = 0;
    var num total_iterations = 0;
    
    // Nested loops
    while "score @s outer_count < 3" {
        inner_count = 0;
        
        while "score @s inner_count < 2" {
            total_iterations = total_iterations + 1;
            
            // Complex calculation within loop
            var num calculation = (outer_count * 10) + inner_count;
            var num modulo_result = calculation % 5;
            
            if "score @s modulo_result == 0" {
                say Perfect calculation: calculation;
            } else {
                say Calculation: calculation (mod 5 = modulo_result);
            }
            
            inner_count = inner_count + 1;
        }
        
        outer_count = outer_count + 1;
    }
    
    // Loop with break and continue
    var num break_counter = 0;
    var num continue_counter = 0;
    var num break_sum = 0;
    var num continue_sum = 0;
    
    while "score @s break_counter < 10" {
        break_counter = break_counter + 1;
        
        if "score @s break_counter == 7" {
            break;
        }
        
        break_sum = break_sum + break_counter;
    }
    
    while "score @s continue_counter < 10" {
        continue_counter = continue_counter + 1;
        
        if "score @s continue_counter % 2 == 0" {
            continue;
        }
        
        continue_sum = continue_sum + continue_counter;
    }
    
    say Loop demo complete;
    tellraw @s {"text":"Total iterations: " + total_iterations};
    tellraw @s {"text":"Break sum: " + break_sum};
    tellraw @s {"text":"Continue sum: " + continue_sum};
}

// Mathematical algorithms
function "calculate_fibonacci" {
    var num n = 10;
    var num a = 0;
    var num b = 1;
    var num i = 2;
    var num temp = 0;
    
    while "score @s i <= n" {
        temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }
    
    say Fibonacci result: b;
    tellraw @s {"text":"Fibonacci(" + n + ") = " + b};
}

// Data processing with lists
function "process_data" {
    var list scores = [85, 92, 78, 96, 88];
    var list names = ["Alice", "Bob", "Charlie", "Diana", "Eve"];
    var num total_score = 0;
    var num highest_score = 0;
    var str best_player = "";
    
    // Calculate total and find highest
    var num i = 0;
    while "score @s i < scores.length" {
        var num current_score = scores[i];
        var str current_name = names[i];
        
        total_score = total_score + current_score;
        
        if "score @s current_score > highest_score" {
            highest_score = current_score;
            best_player = current_name;
        }
        i = i + 1;
    }
    
    var num average_score = total_score / scores.length;
    
    say Data processing complete;
    tellraw @s {"text":"Total score: " + total_score};
    tellraw @s {"text":"Average score: " + average_score};
    tellraw @s {"text":"Best player: " + best_player + " (" + highest_score + ")"};
}

// Error handling and edge cases
function "error_handling" {
    // Test division by zero handling
    var num dividend = 10;
    var num divisor = 0;
    var num result = 0;
    
    if "score @s divisor != 0" {
        result = dividend / divisor;
    } else {
        result = 0;
        say Division by zero prevented;
    }
    
    // Test list bounds checking
    var list test_list = [1, 2, 3];
    var num safe_index = 1;
    var num unsafe_index = 10;
    var num safe_value = 0;
    var num unsafe_value = 0;
    
    if "score @s safe_index < test_list.length" {
        safe_value = test_list[safe_index];
    }
    
    if "score @s unsafe_index < test_list.length" {
        unsafe_value = test_list[unsafe_index];
    } else {
        unsafe_value = -1;
        say List bounds check passed;
    }
    
    say Error handling complete;
    tellraw @s {"text":"Safe value: " + safe_value};
    tellraw @s {"text":"Unsafe value: " + unsafe_value};
}

// Hook the functions into load and tick
on_load "example:hello";
on_tick "example:hello";
on_tick "example:variable_demo";
on_tick "example:conditional_demo";
on_tick "example:weapon_effects";
on_tick "example:loop_demo";
on_tick "example:calculate_fibonacci";
on_tick "example:process_data";
on_tick "example:error_handling";

// Second namespace with cross-namespace calls
namespace "util";

function "helper" {
    say [util:helper] Helping out...;
}

function "boss" {
    say [util:boss] Calling example functions;
    function example:hello;
    function example:variable_demo;
    function example:loop_demo;
    function util:helper;
}

// Run boss every tick
on_tick "util:boss";

// Function tag examples
tag function minecraft:load {
    add example:hello;
}

tag function minecraft:tick {
    add example:hello;
    add example:variable_demo;
    add example:conditional_demo;
    add example:weapon_effects;
    add example:loop_demo;
    add example:calculate_fibonacci;
    add example:process_data;
    add example:error_handling;
    add util:boss;
}

// Data tag examples across registries
tag item example:swords {
    add minecraft:diamond_sword;
    add minecraft:netherite_sword;
    add minecraft:golden_sword;
}

tag block example:glassy {
    add minecraft:glass;
    add minecraft:tinted_glass;
    add minecraft:white_stained_glass;
}

// Garbage collection
function "cleanup" {
    function mdl:garbage_collect;
    say Cleanup complete;
}

on_tick "example:cleanup";
"""
    # Create the main MDL file with a better name
    mdl_filename = f"{args.name.lower().replace(' ', '_')}.mdl"
    with open(os.path.join(root, mdl_filename), "w", encoding="utf-8") as f:
        f.write(sample.strip() + os.linesep)
    
    # Create a README file
    readme_content = f"""# {args.name}

This is a sample MDL (Minecraft Datapack Language) project.

## Usage

1. Build the datapack:
   ```bash
   mdl build --mdl {mdl_filename} -o dist
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

- `{mdl_filename}` - Main MDL source file
- `dist/` - Generated datapack (after building)
"""
    
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"Created sample project at {root}")
    print(f"Main file: {mdl_filename}")
    print(f"Build with: mdl build --mdl {mdl_filename} -o dist")

def _ast_to_pack(ast: Dict[str, Any], default_pack_format: int) -> Pack:
    """Convert JavaScript-style AST to Pack object."""
    # Extract pack information
    pack_info = ast.get('pack')
    if pack_info:
        pack_name = pack_info.name
        pack_format = pack_info.pack_format
        description = pack_info.description
        min_format = pack_info.min_format.values if pack_info.min_format else None
        max_format = pack_info.max_format.values if pack_info.max_format else None
        min_engine_version = pack_info.min_engine_version
    else:
        pack_name = "Generated Pack"
        pack_format = default_pack_format
        description = ""
        min_format = None
        max_format = None
        min_engine_version = None
    
    # Create pack with all metadata
    pack = Pack(
        name=pack_name,
        description=description,
        pack_format=pack_format,
        min_format=min_format,
        max_format=max_format,
        min_engine_version=min_engine_version
    )
    
    # Add garbage collection function
    gc_namespace = pack.namespace("mdl")
    gc_function = gc_namespace.functions.setdefault("garbage_collect", Function("garbage_collect", []))
    gc_function.commands.extend([
        "# Garbage collection for MDL variables",
        "# Clear temporary storage",
        "data remove storage mdl:temp",
        "# Reset scoreboard objectives (optional - uncomment if needed)",
        "# scoreboard objectives remove temp dummy",
        "# scoreboard objectives remove temp2 dummy"
    ])
    
    # Process functions by their namespace
    current_namespace = 'minecraft'  # Default namespace
    
    # First, get the current namespace from namespace declarations
    namespaces = ast.get('namespaces', [])
    if namespaces:
        current_namespace = namespaces[-1].name  # Use the last declared namespace
    
    for func in ast.get('functions', []):
        if hasattr(func, 'name'):
            func_name = func.name
            # Use the current namespace (or function-specific namespace if it has one)
            namespace_name = getattr(func, 'namespace', current_namespace)
            ns = pack.namespace(namespace_name)
            
            # Convert function body to commands
            commands = _ast_to_commands(func.body, namespace_name, pack)
            print(f"DEBUG: Generated {len(commands)} commands for {namespace_name}:{func_name}: {commands}")
            if commands:
                # Create function directly without going through old processing pipeline
                fn = ns.functions.setdefault(func_name, Function(func_name, []))
                fn.commands.extend(commands)
                print(f"DEBUG: Function {namespace_name}:{func_name} now has {len(fn.commands)} commands: {fn.commands}")
    
    # Process hooks (on_load, on_tick)
    for hook in ast.get('hooks', []):
        if hook.hook_type == 'load':
            pack.on_load(hook.function_name)
        elif hook.hook_type == 'tick':
            pack.on_tick(hook.function_name)
    
    # Process tags
    for tag in ast.get('tags', []):
        pack.tag(tag.tag_type, tag.name, tag.values)
    
    return pack

def _ast_to_commands(body: List[Any], current_namespace: str = "test", current_pack: Any = None) -> List[str]:
    """Convert AST function body to list of valid Minecraft commands."""
    print(f"DEBUG: _ast_to_commands called with {len(body)} nodes")
    commands = []
    
    # Performance optimization: Pre-allocate common variables
    temp_var_counter = 0
    
    for i, node in enumerate(body):
        print(f"DEBUG: Processing node {i}: {type(node).__name__}")
        if hasattr(node, '__class__'):
            class_name = node.__class__.__name__
            print(f"DEBUG: Node class: {class_name}")
            
            try:
                if class_name == 'Command':
                    # Remove semicolon from command and clean up
                    command = node.command.rstrip(';').strip()
                    commands.append(command)
                    
                elif class_name == 'FunctionCall':
                    # Convert function call to Minecraft function command
                    function_name = node.function_name
                    commands.append(f"function {function_name}")
                    
                elif class_name == 'VariableDeclaration':
                    # Convert variable declarations to scoreboard commands
                    var_type = node.data_type
                    var_name = node.name
                    
                    # Initialize the variable based on type
                    if var_type == 'num':
                        commands.append(f"scoreboard objectives add {var_name} dummy")
                    elif var_type == 'str':
                        commands.append(f"data modify storage mdl:variables {var_name} set value \"\"")
                    elif var_type == 'list':
                        commands.append(f"data modify storage mdl:variables {var_name} set value []")
                    
                    # Handle the value using expression processor
                    if node.value:
                        processed = expression_processor.process_expression(node.value, var_name)
                        commands.extend(processed.temp_assignments)
                        
                        # If there's a final command, add it
                        if processed.final_command:
                            commands.append(processed.final_command)
                                
                elif class_name == 'VariableAssignment':
                    # Convert variable assignments to appropriate Minecraft commands
                    var_name = node.name
                    
                    # Handle the value using expression processor
                    if node.value:
                        processed = expression_processor.process_expression(node.value, var_name)
                        commands.extend(processed.temp_assignments)
                        
                        # If there's a final command, add it
                        if processed.final_command:
                            commands.append(processed.final_command)
                            
                elif class_name == 'IfStatement':
                    # Convert if statements to Minecraft conditional commands
                    condition = node.condition.strip('"')
                    
                    # Convert if body to commands
                    if_commands = _ast_to_commands(node.body, current_namespace, current_pack)
                    
                    # Convert else body to commands (if it exists)
                    else_commands = []
                    if node.else_body:
                        else_commands = _ast_to_commands(node.else_body, current_namespace, current_pack)
                    
                    # Generate conditional execution
                    if if_commands:
                        # Add if condition and commands
                        commands.append(f"# If statement: {condition}")
                        for cmd in if_commands:
                            commands.append(f"execute if {condition} run {cmd}")
                    
                    if else_commands:
                        # Add else commands with inverted condition
                        unless_conditions = condition.replace('==', '!=').replace('!=', '==')
                        commands.append(f"# Else statement")
                        for cmd in else_commands:
                            commands.append(f"execute {unless_conditions} run {cmd}")
                            
                elif class_name == 'ForLoop':
                    # Convert for loops to Minecraft iteration commands
                    variable = node.variable
                    selector = node.selector.strip('"')
                    loop_body = _ast_to_commands(node.body, current_namespace, current_pack)
                    
                    # Generate loop commands
                    commands.append(f"# For loop over {selector}")
                    for cmd in loop_body:
                        commands.append(f"execute as {selector} run {cmd}")
                        
                elif class_name == 'ForInLoop':
                    # Convert for-in loops to Minecraft list iteration commands
                    variable = node.variable
                    list_name = node.list_name
                    loop_body = _ast_to_commands(node.body, current_namespace, current_pack)

                    commands.append(f"# For-in loop over {list_name}")
                    commands.append(f"execute store result storage mdl:temp list_length int 1 run data get storage mdl:variables {list_name}")
                    commands.append(f"execute if data storage mdl:variables {list_name} run function {current_namespace}:for_in_{variable}_{list_name}")

                    # Generate the loop body function
                    loop_func_name = f"for_in_{variable}_{list_name}"
                    loop_func_commands = []

                    # Add loop initialization
                    loop_func_commands.append(f"# Initialize loop index")
                    loop_func_commands.append(f"scoreboard players set @s loop_index 0")

                    # Add loop condition and body
                    loop_func_commands.append(f"# Loop condition")
                    loop_func_commands.append(f"execute if score @s loop_index < @s list_length run function {current_namespace}:for_in_body_{variable}_{list_name}")

                    # Generate the loop body function
                    body_func_name = f"for_in_body_{variable}_{list_name}"
                    body_commands = []

                    # Get current element and store it in a variable
                    body_commands.append(f"# Get current element")
                    body_commands.append(f"data modify storage mdl:temp current_element set from storage mdl:variables {list_name}[score @s loop_index]")

                    # Replace variable references in loop body
                    for cmd in loop_body:
                        modified_cmd = cmd.replace(f"@{variable}", "storage mdl:temp current_element")
                        body_commands.append(modified_cmd)

                    # Increment loop index and continue
                    body_commands.append(f"# Increment index and continue")
                    body_commands.append(f"scoreboard players add @s loop_index 1")
                    body_commands.append(f"execute if score @s loop_index < @s list_length run function {current_namespace}:for_in_body_{variable}_{list_name}")

                    # Store the functions for later generation
                    if not hasattr(current_pack, 'loop_functions'):
                        current_pack.loop_functions = {}
                    current_pack.loop_functions[loop_func_name] = loop_func_commands
                    current_pack.loop_functions[body_func_name] = body_commands
                    
                elif class_name == 'WhileLoop':
                    # Convert while loops to Minecraft conditional commands
                    condition = node.condition.strip('"')
                    loop_body = _ast_to_commands(node.body, current_namespace, current_pack)
                    
                    # Generate loop commands
                    commands.append(f"# While loop: {condition}")
                    for cmd in loop_body:
                        commands.append(f"execute if {condition} run {cmd}")
                        
                elif class_name == 'BreakStatement':
                    # Handle break statements in loops
                    commands.append(f"# Break statement - exit current loop")
                    commands.append(f"execute unless score @s break_flag matches 1.. run scoreboard players set @s break_flag 1")
                
                elif class_name == 'ContinueStatement':
                    # Handle continue statements in loops
                    commands.append(f"# Continue statement - skip to next iteration")
                    commands.append(f"execute unless score @s continue_flag matches 1.. run scoreboard players set @s continue_flag 1")
                
                elif class_name == 'ReturnStatement':
                    # Convert return statements to Minecraft commands
                    if hasattr(node, 'value') and node.value:
                        if hasattr(node.value, 'value'):
                            return_value = node.value.value
                            commands.append(f"# Return value: {return_value}")
                        else:
                            commands.append(f"# Return statement")
                    else:
                        commands.append(f"# Return (no value)")
                    
                elif class_name == 'ListAccessExpression':
                    # Convert list access to Minecraft NBT commands
                    list_name = node.list_name
                    if hasattr(node.index, 'value'):
                        index = node.index.value
                        commands.append(f"# Access element at index {index} from {list_name}")
                        commands.append(f"execute store result storage mdl:temp index int 1 run scoreboard players get @s {index}")
                        commands.append(f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[storage mdl:temp index]")
                    elif hasattr(node.index, 'name'):
                        # Variable index
                        index_var = node.index.name
                        commands.append(f"# Access element at variable index {index_var} from {list_name}")
                        commands.append(f"execute store result storage mdl:temp index int 1 run scoreboard players get @s {index_var}")
                        commands.append(f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[storage mdl:temp index]")
                    else:
                        commands.append(f"# Access element from {list_name} (complex index)")
                        commands.append(f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[0]")
                        
                elif class_name == 'ListLengthExpression':
                    # Convert list length to Minecraft commands
                    list_name = node.list_name
                    commands.append(f"# Get length of {list_name}")
                    commands.append(f"execute store result score @s {list_name}_length run data get storage mdl:variables {list_name}")
                    commands.append(f"# Store length in a more accessible variable")
                    commands.append(f"scoreboard players operation @s list_length = @s {list_name}_length")
                    
                elif class_name == 'ListAppendOperation':
                    # Convert list append operations to Minecraft NBT commands
                    list_name = node.list_name
                    if hasattr(node.value, 'value'):
                        # Handle string literals
                        if hasattr(node.value, 'type') and node.value.type == 'string':
                            value = node.value.value.strip('"')
                            commands.append(f"data modify storage mdl:variables {list_name} append value \"{value}\"")
                        elif hasattr(node.value, 'type') and node.value.type == 'number':
                            value = node.value.value
                            commands.append(f"data modify storage mdl:variables {list_name} append value {value}")
                        else:
                            # Try to determine type from value
                            try:
                                value = int(node.value.value)
                                commands.append(f"data modify storage mdl:variables {list_name} append value {value}")
                            except (ValueError, TypeError):
                                # Assume string
                                value = node.value.value.strip('"')
                                commands.append(f"data modify storage mdl:variables {list_name} append value \"{value}\"")
                    else:
                        # Unknown value type - skip
                        continue
                        
                elif class_name == 'ListRemoveOperation':
                    # Convert list remove operations to Minecraft NBT commands
                    list_name = node.list_name
                    if hasattr(node.value, 'value'):
                        # Handle string literals
                        if hasattr(node.value, 'type') and node.value.type == 'string':
                            value = node.value.value.strip('"')
                            # Use a temporary storage to find and remove the item
                            commands.append(f"# Remove '{value}' from {list_name}")
                            commands.append(f"execute store result storage mdl:temp index int 1 run data get storage mdl:variables {list_name}")
                            commands.append(f"execute if data storage mdl:variables {list_name}[{{value:\"{value}\"}}] run data remove storage mdl:variables {list_name}[{{value:\"{value}\"}}]")
                        elif hasattr(node.value, 'type') and node.value.type == 'number':
                            value = node.value.value
                            commands.append(f"# Remove {value} from {list_name}")
                            commands.append(f"execute if data storage mdl:variables {list_name}[{{value:{value}}}] run data remove storage mdl:variables {list_name}[{{value:{value}}}]")
                        else:
                            # Try to determine type from value
                            try:
                                value = int(node.value.value)
                                commands.append(f"# Remove {value} from {list_name}")
                                commands.append(f"execute if data storage mdl:variables {list_name}[{{value:{value}}}] run data remove storage mdl:variables {list_name}[{{value:{value}}}]")
                            except (ValueError, TypeError):
                                # Assume string
                                value = node.value.value.strip('"')
                                commands.append(f"# Remove '{value}' from {list_name}")
                                commands.append(f"execute if data storage mdl:variables {list_name}[{{value:\"{value}\"}}] run data remove storage mdl:variables {list_name}[{{value:\"{value}\"}}]")
                    else:
                        # Unknown value type - skip
                        continue
                        
                elif class_name == 'ListInsertOperation':
                    # Convert list insert operations to Minecraft NBT commands
                    list_name = node.list_name
                    if hasattr(node.index, 'value') and hasattr(node.value, 'value'):
                        index = node.index.value
                        if hasattr(node.value, 'type') and node.value.type == 'string':
                            value = node.value.value.strip('"')
                            commands.append(f"# Insert '{value}' at index {index} in {list_name}")
                            commands.append(f"data modify storage mdl:variables {list_name} insert {index} value \"{value}\"")
                        elif hasattr(node.value, 'type') and node.value.type == 'number':
                            value = node.value.value
                            commands.append(f"# Insert {value} at index {index} in {list_name}")
                            commands.append(f"data modify storage mdl:variables {list_name} insert {index} value {value}")
                        else:
                            # Try to determine type from value
                            try:
                                value = int(node.value.value)
                                commands.append(f"# Insert {value} at index {index} in {list_name}")
                                commands.append(f"data modify storage mdl:variables {list_name} insert {index} value {value}")
                            except (ValueError, TypeError):
                                # Assume string
                                value = node.value.value.strip('"')
                                commands.append(f"# Insert '{value}' at index {index} in {list_name}")
                                commands.append(f"data modify storage mdl:variables {list_name} insert {index} value \"{value}\"")
                    else:
                        # Unknown value type - skip
                        continue
                        
                elif class_name == 'ListPopOperation':
                    # Convert list pop operations to Minecraft NBT commands
                    list_name = node.list_name
                    commands.append(f"# Pop last element from {list_name}")
                    commands.append(f"execute store result storage mdl:temp last_index int 1 run data get storage mdl:variables {list_name}")
                    commands.append(f"execute if data storage mdl:variables {list_name} run data remove storage mdl:variables {list_name}[storage mdl:temp last_index]")
                    
                elif class_name == 'ListClearOperation':
                    # Convert list clear operations to Minecraft NBT commands
                    list_name = node.list_name
                    commands.append(f"# Clear list {list_name}")
                    commands.append(f"data modify storage mdl:variables {list_name} set value []")
                    
                else:
                    # Unknown node type - skip for now
                    continue
                    
            except Exception as e:
                print(f"ERROR: Failed to process node {i} of type {class_name}: {str(e)}")
                commands.append(f"# ERROR: Failed to process {class_name} - {str(e)}")
                continue
                
    return commands

def _convert_arithmetic_expression(var_name: str, expr: Any) -> List[str]:
    """Convert arithmetic expressions to Minecraft scoreboard commands."""
    commands = []
    
    if hasattr(expr, 'operator'):
        op = expr.operator
        left = expr.left
        right = expr.right
        
        # Handle simple cases first
        if op == '+':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                result = left + right
                commands.append(f"scoreboard players set @s {var_name} {result}")
            elif isinstance(left, (int, float)):
                commands.append(f"scoreboard players set @s {var_name} {left}")
                if isinstance(right, (int, float)):
                    commands.append(f"scoreboard players add @s {var_name} {right}")
            elif isinstance(right, (int, float)):
                commands.append(f"scoreboard players set @s {var_name} {right}")
                if isinstance(left, (int, float)):
                    commands.append(f"scoreboard players add @s {var_name} {left}")
            else:
                # Both are variables - use operation
                commands.append(f"scoreboard players operation @s {var_name} = @s {left}")
                commands.append(f"scoreboard players add @s {var_name} {right}")
        elif op == '-':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                result = left - right
                commands.append(f"scoreboard players set @s {var_name} {result}")
            elif isinstance(left, (int, float)):
                commands.append(f"scoreboard players set @s {var_name} {left}")
                if isinstance(right, (int, float)):
                    commands.append(f"scoreboard players remove @s {var_name} {right}")
            elif isinstance(right, (int, float)):
                commands.append(f"scoreboard players set @s {var_name} {left}")
                commands.append(f"scoreboard players remove @s {var_name} {right}")
            else:
                commands.append(f"scoreboard players operation @s {var_name} = @s {left}")
                commands.append(f"scoreboard players remove @s {var_name} {right}")
        elif op == '*':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                result = left * right
                commands.append(f"scoreboard players set @s {var_name} {result}")
            else:
                # For complex multiplication, set to 0 for now
                commands.append(f"scoreboard players set @s {var_name} 0")
        elif op == '/':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)) and right != 0:
                result = left // right  # Integer division
                commands.append(f"scoreboard players set @s {var_name} {result}")
            else:
                commands.append(f"scoreboard players set @s {var_name} 0")
        elif op == '%':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)) and right != 0:
                result = left % right  # Modulo
                commands.append(f"scoreboard players set @s {var_name} {result}")
            elif isinstance(left, (int, float)) and hasattr(right, 'name'):
                # Constant % variable
                commands.append(f"scoreboard players set @s {var_name} {left}")
                commands.append(f"execute store result storage mdl:temp remainder int 1 run scoreboard players get @s {right.name}")
                commands.append(f"execute if score @s {right.name} matches 0.. run scoreboard players set @s {var_name} 0")
                commands.append(f"execute unless score @s {right.name} matches 0.. run scoreboard players operation @s {var_name} %= @s {right.name}")
            elif hasattr(left, 'name') and isinstance(right, (int, float)):
                # Variable % constant
                if right != 0:
                    commands.append(f"scoreboard players operation @s {var_name} = @s {left.name}")
                    commands.append(f"scoreboard players set @s temp_mod {right}")
                    commands.append(f"scoreboard players operation @s {var_name} %= @s temp_mod")
                else:
                    commands.append(f"scoreboard players set @s {var_name} 0")
            elif hasattr(left, 'name') and hasattr(right, 'name'):
                # Variable % variable
                commands.append(f"scoreboard players operation @s {var_name} = @s {left.name}")
                commands.append(f"scoreboard players operation @s {var_name} %= @s {right.name}")
            else:
                commands.append(f"scoreboard players set @s {var_name} 0")
        else:
            # Unknown operator, set to 0
            commands.append(f"scoreboard players set @s {var_name} 0")
    else:
        # Simple value assignment
        if isinstance(expr, (int, float)):
            commands.append(f"scoreboard players set @s {var_name} {expr}")
        else:
            commands.append(f"scoreboard players set @s {var_name} 0")
    
    return commands

def _convert_string_expression(var_name: str, expr: Any) -> List[str]:
    """Convert string expressions to Minecraft NBT commands."""
    commands = []
    
    if hasattr(expr, 'operator') and expr.operator == '+':
        # String concatenation
        left = expr.left
        right = expr.right
        
        if isinstance(left, str) and isinstance(right, str):
            result = left.strip('"') + right.strip('"')
            commands.append(f"data modify storage mdl:variables {var_name} set value \"{result}\"")
        elif isinstance(left, str):
            left_val = left.strip('"')
            commands.append(f"data modify storage mdl:variables {var_name} set value \"{left_val}\"")
        elif isinstance(right, str):
            right_val = right.strip('"')
            commands.append(f"data modify storage mdl:variables {var_name} set value \"{right_val}\"")
        else:
            commands.append(f"data modify storage mdl:variables {var_name} set value \"\"")
    else:
        # Simple string assignment
        if isinstance(expr, str):
            value = expr.strip('"')
            commands.append(f"data modify storage mdl:variables {var_name} set value \"{value}\"")
        else:
            commands.append(f"data modify storage mdl:variables {var_name} set value \"\"")
    
    return commands

def _determine_wrapper(pack: Pack, override: str | None):
    if override:
        return override
    if pack.namespaces:
        return next(iter(pack.namespaces.keys()))
    return _slug(pack.name)

def cmd_build(args):
    out_root = os.path.abspath(args.out)
    ensure_dir(out_root)

    # Resolve pack: from --mdl/--src or --py-module
    pack = None
    if args.mdl or args.src:
        path = args.mdl or args.src
        files = _gather_mdl_files(path)
        pack = _parse_many(files, default_pack_format=args.pack_format, verbose=args.verbose)
    else:
        # from python module path containing a function create_pack()
        sys.path.insert(0, os.path.abspath("."))
        mod = __import__(args.py_module)
        if not hasattr(mod, "create_pack"):
            raise SystemExit("Python module must expose create_pack() -> Pack")
        pack = mod.create_pack()

    wrapper = _determine_wrapper(pack, args.wrapper)
    wrapped_dir = os.path.join(out_root, wrapper)
    if os.path.exists(wrapped_dir):
        shutil.rmtree(wrapped_dir)
    os.makedirs(wrapped_dir, exist_ok=True)

    pack.build(wrapped_dir)

    zip_path = f"{wrapped_dir}.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    _zip_dir(wrapped_dir, zip_path)

    print(f"Built datapack at {wrapped_dir}")
    print(f"Zipped datapack at {zip_path}")

def cmd_check(args):
    errors = []
    try:
        path = args.path
        if os.path.isdir(path):
            # Use the same multi-file logic as build command
            files = _gather_mdl_files(path)
            try:
                _parse_many(files, default_pack_format=args.pack_format, verbose=args.verbose)
            except Exception as e:
                # Try to extract filename and line info from the error
                error_str = str(e)
                if ":" in error_str:
                    # Format: "filename: error message" or "filename: Line N: error message"
                    parts = error_str.split(":", 2)
                    if len(parts) >= 2:
                        file_path = parts[0]
                        if len(parts) >= 3 and "Line" in parts[1]:
                            # "Line N: error message" format
                            line_match = re.search(r'Line (\d+):\s*(.*)', parts[1] + ":" + parts[2])
                            if line_match:
                                errors.append({"file": file_path, "line": int(line_match.group(1)), "message": line_match.group(2)})
                            else:
                                errors.append({"file": file_path, "line": None, "message": parts[2]})
                        else:
                            # "error message" format
                            errors.append({"file": file_path, "line": None, "message": parts[1]})
                    else:
                        errors.append({"file": path, "line": None, "message": error_str})
                else:
                    errors.append({"file": path, "line": None, "message": error_str})
        else:
            # Single file - parse individually
            with open(path, "r", encoding="utf-8") as f:
                src = f.read()
            ast = parse_mdl_js(src)
            # Convert AST to Pack for validation
            _ast_to_pack(ast, args.pack_format)
    except Exception as e:
        # For top-level failures
        m = re.search(r'Line (\d+):\s*(.*)', str(e))
        if m:
            errors.append({"file": path, "line": int(m.group(1)), "message": m.group(2)})
        else:
            errors.append({"file": path, "line": None, "message": str(e)})

    if args.json:
        print(json.dumps({"ok": len(errors) == 0, "errors": errors}, indent=2))
        return 0 if not errors else 1

    if errors:
        for err in errors:
            loc = f"{err['file']}"
            if err["line"]:
                loc += f":{err['line']}"
            print(f"ERROR {loc} -> {err['message']}")
        return 1
    else:
        print("OK")
        return 0

def main(argv=None):
    p = argparse.ArgumentParser(prog="mdl", description="Minecraft Datapack Language (compiler)")
    
    # Add version argument
    p.add_argument("--version", action="version", version="%(prog)s " + __version__)
    
    sub = p.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="Create a sample .mdl project")
    p_new.add_argument("path")
    p_new.add_argument("--name", default="Minecraft Datapack Language")
    p_new.add_argument("--pack-format", type=int, default=82, help="Pack format (default: 82 for modern)")
    p_new.set_defaults(func=cmd_new)

    p_build = sub.add_parser("build", help="Build a datapack")
    g = p_build.add_mutually_exclusive_group(required=True)
    g.add_argument("--mdl", help="Path to .mdl source (file or directory)")
    g.add_argument("--src", help="Path to .mdl source (file or directory)")
    g.add_argument("--py-module", help="Python module path exposing create_pack() -> Pack")
    p_build.add_argument("-o", "--out", required=True, help="Output folder (MDL creates <out>/<wrapper>/ and <out>/<wrapper>.zip)")
    p_build.add_argument("--pack-format", type=int, default=82, help="Pack format (default: 82 for modern)")
    p_build.add_argument("--wrapper", help="Wrapper folder/zip name (default: first namespace or slug of pack name)")
    p_build.add_argument("-v", "--verbose", action="store_true", help="Show detailed processing information")
    p_build.set_defaults(func=cmd_build)

    p_check = sub.add_parser("check", help="Validate .mdl (file or directory)")
    p_check.add_argument("path", help="Path to .mdl file or directory")
    p_check.add_argument("--pack-format", type=int, default=82, help="Pack format (default: 82 for modern)")
    p_check.add_argument("--json", action="store_true", help="Emit JSON diagnostics")
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.set_defaults(func=cmd_check)

    args = p.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
