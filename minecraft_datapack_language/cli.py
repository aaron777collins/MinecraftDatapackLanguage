
import argparse, os, sys, json, traceback, re, zipfile, shutil, glob
from typing import Dict, Any, List
from .pack import Pack, Function
from .utils import ensure_dir
from .mdl_parser_js import parse_mdl_js
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
    ensure_dir(root)
    
    # Add format-specific comment
    format_comment = "# Using modern JavaScript-style MDL format (v10+)"
    
    # Create the pack declaration separately to avoid f-string issues with array literals
    pack_declaration = 'pack "{}" description "Example datapack" pack_format {} min_format [{}, 0] max_format [{}, 1] min_engine_version "1.21.4";'.format(args.name, args.pack_format, args.pack_format, args.pack_format)
    
    sample = """// mypack.mdl - minimal example for Minecraft Datapack Language (JavaScript-style)
# Using modern JavaScript-style MDL format (v10+)
""" + pack_declaration + """
namespace "example";

function "inner" {
    say [example:inner] This is the inner function;
    tellraw @a {"text":"Running inner","color":"yellow"};
}

function "hello" {
    say [example:hello] Outer says hi;
    function example:inner;
    tellraw @a {"text":"Back in hello","color":"aqua"};
}

// Conditional example - detect different entity types with enhanced logic
function "conditional_demo" {
    if "entity @s[type=minecraft:player]" {
        say Player detected!;
        effect give @s minecraft:glowing 5 1;
        tellraw @a {"text":"A player is nearby!","color":"green"};
    } else if "entity @s[type=minecraft:zombie]" {
        say Zombie detected!;
        effect give @s minecraft:poison 5 1;
        tellraw @a {"text":"A zombie is nearby!","color":"red"};
    } else if "entity @s[type=minecraft:creeper]" {
        say Creeper detected!;
        effect give @s minecraft:resistance 5 1;
        tellraw @a {"text":"A creeper is nearby!","color":"dark_red"};
    } else {
        say Unknown entity detected;
        tellraw @a {"text":"Something unknown is nearby...","color":"gray"};
    }
}

// Advanced conditional example - weapon effects system
function "weapon_effects" {
    if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:diamond_sword'}}]" {
        say Diamond sword detected!;
        effect give @s minecraft:strength 10 1;
        effect give @s minecraft:glowing 10 0;
    } else if "entity @s[type=minecraft:player,nbt={SelectedItem:{id:'minecraft:golden_sword'}}]" {
        say Golden sword detected!;
        effect give @s minecraft:speed 10 1;
        effect give @s minecraft:night_vision 10 0;
    } else if "entity @s[type=minecraft:player]" {
        say Player without special weapon;
        effect give @s minecraft:haste 5 0;
    } else {
        say No player found;
    }
}

// Variable system example
var num global_counter = 0;
var str global_message = "Hello World";

function "variable_demo" {
    var num local_counter = 10;
    var str player_name = "Steve";
    
    local_counter = local_counter + 5;
    global_counter = global_counter + 1;
    
    player_name = "Alex";
    global_message = "Updated: " + player_name;
    
    if "score @s test:local_counter matches 15" {
        say Counter is 15!;
    }
}

// Hook the function into load and tick
on_load "example:hello";
on_tick "example:hello";
on_tick "example:conditional_demo";
on_tick "example:weapon_effects";
on_tick "example:variable_demo";

// Second namespace with a cross-namespace call
namespace "util";

function "helper" {
    say [util:helper] Helping out...;
}

function "boss" {
    say [util:boss] Calling example:hello then util:helper;
    function example:hello;
    function util:helper;
}

// Run boss every tick as well
on_tick "util:boss";

// Function tag examples
tag function "minecraft:load" {
    add "example:hello";
}

tag function "minecraft:tick" {
    add "example:hello";
    add "example:conditional_demo";
    add "example:weapon_effects";
    add "example:variable_demo";
    add "util:boss";
}

// Data tag examples across registries
tag item "example:swords" {
    add "minecraft:diamond_sword";
    add "minecraft:netherite_sword";
}

tag block "example:glassy" {
    add "minecraft:glass";
    add "minecraft:tinted_glass";
}
"""
    with open(os.path.join(root, "mypack.mdl"), "w", encoding="utf-8") as f:
        f.write(sample.strip() + os.linesep)
    print(f"Created sample at {root}")

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
    for func in ast.get('functions', []):
        if hasattr(func, 'name'):
            func_name = func.name
            # Get the namespace for this function
            namespace_name = getattr(func, 'namespace', 'minecraft')  # Default to minecraft if no namespace
            ns = pack.namespace(namespace_name)
            
            # Convert function body to commands
            commands = _ast_to_commands(func.body)
            if commands:
                # Create function directly without going through old processing pipeline
                fn = ns.functions.setdefault(func_name, Function(func_name, []))
                fn.commands.extend(commands)
    
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

def _ast_to_commands(body: List[Any]) -> List[str]:
    """Convert AST function body to list of valid Minecraft commands."""
    commands = []
    for node in body:
        if hasattr(node, '__class__'):
            class_name = node.__class__.__name__
            
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
                
                if var_type == 'num':
                    # Number variables use scoreboard
                    commands.append(f"scoreboard objectives add {var_name} dummy")
                    if node.value:
                        # Set initial value if provided
                        try:
                            initial_value = int(node.value)
                            commands.append(f"scoreboard players set @s {var_name} {initial_value}")
                        except (ValueError, TypeError):
                            # If not a simple number, set to 0
                            commands.append(f"scoreboard players set @s {var_name} 0")
                elif var_type == 'str':
                    # String variables use NBT storage
                    commands.append(f"data modify storage mdl:variables {var_name} set value \"\"")
                    if node.value:
                        # Set initial value if provided
                        initial_value = str(node.value).strip('"')
                        commands.append(f"data modify storage mdl:variables {var_name} set value \"{initial_value}\"")
                elif var_type == 'list':
                    # List variables use NBT storage with array
                    commands.append(f"data modify storage mdl:variables {var_name} set value []")
                    if node.value and hasattr(node.value, 'elements'):
                        # Add initial values if provided
                        for i, item in enumerate(node.value.elements):
                            if hasattr(item, 'value'):
                                # Handle string literals in lists
                                item_value = item.value.strip('"')
                                commands.append(f"data modify storage mdl:variables {var_name} append value \"{item_value}\"")
                            else:
                                # Handle other types - convert to string for now
                                commands.append(f"data modify storage mdl:variables {var_name} append value \"unknown\"")
                            
            elif class_name == 'VariableAssignment':
                # Convert variable assignments to appropriate Minecraft commands
                var_name = node.name
                
                if hasattr(node, 'value'):
                    # Handle different types of expressions
                    if hasattr(node.value, '__class__'):
                        expr_class = node.value.__class__.__name__
                        
                        if expr_class == 'BinaryExpression':
                            # Handle arithmetic operations
                            if node.value.operator in ['+', '-', '*', '/']:
                                # Handle different types of binary expressions
                                if node.value.operator == '+':
                                    # Addition
                                    if hasattr(node.value.left, 'name') and hasattr(node.value.right, 'value'):
                                        # Variable + literal (e.g., local_counter + 5)
                                        right_value = node.value.right.value
                                        commands.append(f"scoreboard players add @s {var_name} {right_value}")
                                    elif hasattr(node.value.left, 'value') and hasattr(node.value.right, 'name'):
                                        # Literal + variable (e.g., 5 + local_counter)
                                        left_value = node.value.left.value
                                        commands.append(f"scoreboard players add @s {var_name} {left_value}")
                                    elif hasattr(node.value.left, 'value') and hasattr(node.value.right, 'name'):
                                        # String concatenation (e.g., "Updated: " + player_name)
                                        left_value = node.value.left.value
                                        right_var = node.value.right.name
                                        commands.append(f"# String concatenation: '{left_value}' + {right_var}")
                                        commands.append(f"data modify storage mdl:variables {var_name} set value \"{left_value}\"")
                                        commands.append(f"execute store result storage mdl:temp concat string 1 run data get storage mdl:variables {right_var}")
                                        commands.append(f"data modify storage mdl:variables {var_name} append value storage mdl:temp concat")
                                    else:
                                        # Complex addition - for now, set to 0
                                        commands.append(f"scoreboard players set @s {var_name} 0")
                                elif node.value.operator == '-':
                                    # Subtraction
                                    if hasattr(node.value.right, 'value'):
                                        right_value = node.value.right.value
                                        commands.append(f"scoreboard players remove @s {var_name} {right_value}")
                                    else:
                                        commands.append(f"scoreboard players set @s {var_name} 0")
                                else:
                                    # Complex arithmetic - for now, set to 0
                                    commands.append(f"scoreboard players set @s {var_name} 0")
                            else:
                                # Unknown operator
                                commands.append(f"scoreboard players set @s {var_name} 0")
                                
                        elif expr_class == 'StringLiteral':
                            # String assignment
                            value = node.value.value.strip('"')
                            commands.append(f"data modify storage mdl:variables {var_name} set value \"{value}\"")
                            
                        elif expr_class == 'NumericLiteral':
                            # Number assignment
                            value = node.value.value
                            commands.append(f"scoreboard players set @s {var_name} {value}")
                            
                        elif expr_class == 'LiteralExpression':
                            # Handle LiteralExpression (which can be string or number)
                            if hasattr(node.value, 'type'):
                                if node.value.type == 'string':
                                    value = node.value.value.strip('"')
                                    commands.append(f"data modify storage mdl:variables {var_name} set value \"{value}\"")
                                elif node.value.type == 'number':
                                    value = node.value.value
                                    commands.append(f"scoreboard players set @s {var_name} {value}")
                                else:
                                    # Unknown type - skip
                                    continue
                            else:
                                # No type info - try to determine from value
                                try:
                                    value = int(node.value.value)
                                    commands.append(f"scoreboard players set @s {var_name} {value}")
                                except (ValueError, TypeError):
                                    # Assume string
                                    value = node.value.value.strip('"')
                                    commands.append(f"data modify storage mdl:variables {var_name} set value \"{value}\"")
                                    
                        elif expr_class == 'ListExpression':
                            # Handle list assignments
                            commands.append(f"data modify storage mdl:variables {var_name} set value []")
                            if hasattr(node.value, 'elements'):
                                for item in node.value.elements:
                                    if hasattr(item, 'value'):
                                        # Handle string literals in lists
                                        item_value = item.value.strip('"')
                                        commands.append(f"data modify storage mdl:variables {var_name} append value \"{item_value}\"")
                                    else:
                                        # Handle other types - convert to string for now
                                        commands.append(f"data modify storage mdl:variables {var_name} append value \"unknown\"")
                            
                        elif expr_class == 'Identifier':
                            # Variable reference - for now, assume it's a number variable
                            commands.append(f"scoreboard players operation @s {var_name} = @s {node.value.name}")
                            
                        elif expr_class == 'ListAccessExpression':
                            # Handle list access like local_str = local_list[0]
                            list_name = node.value.list_name
                            if hasattr(node.value.index, 'value'):
                                index = node.value.index.value
                                # For now, we'll use a simple approach - store the list element in a temporary variable
                                commands.append(f"# Access element at index {index} from {list_name}")
                                commands.append(f"data modify storage mdl:temp element set from storage mdl:variables {list_name}[{index}]")
                                # Then copy to the target variable (assuming it's a string for now)
                                commands.append(f"data modify storage mdl:variables {var_name} set from storage mdl:temp element")
                            else:
                                # Complex index expression - skip for now
                                continue
                            
                        else:
                            # Unknown expression type - skip for now
                            continue
                    else:
                        # Simple value assignment
                        if isinstance(node.value, (int, float)):
                            commands.append(f"scoreboard players set @s {var_name} {node.value}")
                        elif isinstance(node.value, str):
                            value = node.value.strip('"')
                            commands.append(f"data modify storage mdl:variables {var_name} set value \"{value}\"")
                        else:
                            # Unknown type - skip
                            continue
                        
            elif class_name == 'IfStatement':
                # Convert if statements to Minecraft conditional commands
                condition = node.condition.strip('"')
                if_body = _ast_to_commands(node.body)
                
                # Generate conditional commands for if block
                for cmd in if_body:
                    commands.append(f"execute if {condition} run {cmd}")
                
                # Handle elif branches - each elif needs to check its condition AND that previous conditions were false
                if hasattr(node, 'elif_branches') and node.elif_branches:
                    # For the first elif, we need to check its condition AND that the if condition was false
                    first_elif = node.elif_branches[0]
                    elif_condition = first_elif.condition.strip('"')
                    elif_body = _ast_to_commands(first_elif.body)
                    
                    for cmd in elif_body:
                        commands.append(f"execute if {elif_condition} unless {condition} run {cmd}")
                    
                    # For subsequent elif branches, we need to check their condition AND that all previous conditions were false
                    for i in range(1, len(node.elif_branches)):
                        elif_branch = node.elif_branches[i]
                        elif_condition = elif_branch.condition.strip('"')
                        elif_body = _ast_to_commands(elif_branch.body)
                        
                        # Build condition that checks this elif condition AND that all previous conditions were false
                        previous_conditions = [condition] + [branch.condition.strip('"') for branch in node.elif_branches[:i]]
                        unless_conditions = " ".join([f"unless {cond}" for cond in previous_conditions])
                        
                        for cmd in elif_body:
                            commands.append(f"execute if {elif_condition} {unless_conditions} run {cmd}")
                
                # Handle else branch - only execute if all previous conditions were false
                if hasattr(node, 'else_body') and node.else_body:
                    else_body = _ast_to_commands(node.else_body)
                    
                    # Build condition that checks that all previous conditions were false
                    all_conditions = [condition]
                    if hasattr(node, 'elif_branches') and node.elif_branches:
                        all_conditions.extend([branch.condition.strip('"') for branch in node.elif_branches])
                    
                    unless_conditions = " ".join([f"unless {cond}" for cond in all_conditions])
                    
                    for cmd in else_body:
                        commands.append(f"execute {unless_conditions} run {cmd}")
                        
            elif class_name == 'ForLoop':
                # Convert for loops to Minecraft iteration commands
                variable = node.variable
                selector = node.selector.strip('"')
                loop_body = _ast_to_commands(node.body)
                
                # Generate loop commands
                for cmd in loop_body:
                    # Replace @s with the loop variable selector
                    modified_cmd = cmd.replace('@s', selector)
                    commands.append(f"execute as {selector} run {modified_cmd}")
                    
            elif class_name == 'WhileLoop':
                # Convert while loops to Minecraft conditional commands
                condition = node.condition.strip('"')
                loop_body = _ast_to_commands(node.body)
                
                # Generate loop commands (simplified - in practice you'd need more complex logic)
                for cmd in loop_body:
                    commands.append(f"execute if {condition} run {cmd}")
                    
            elif class_name == 'BreakStatement':
                # Skip break statements for now
                continue
                
            elif class_name == 'ContinueStatement':
                # Skip continue statements for now
                continue
                
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
                if node.index:
                    # Pop at specific index
                    if hasattr(node.index, 'value'):
                        index = node.index.value
                        commands.append(f"# Pop element at index {index} from {list_name}")
                        commands.append(f"data remove storage mdl:variables {list_name}[{index}]")
                else:
                    # Pop last element
                    commands.append(f"# Pop last element from {list_name}")
                    commands.append(f"execute store result storage mdl:temp last_index int 1 run data get storage mdl:variables {list_name}")
                    commands.append(f"execute if data storage mdl:variables {list_name} run data remove storage mdl:variables {list_name}[storage mdl:temp last_index]")
                    
            elif class_name == 'ListClearOperation':
                # Convert list clear operations to Minecraft NBT commands
                list_name = node.list_name
                commands.append(f"# Clear all elements from {list_name}")
                commands.append(f"data modify storage mdl:variables {list_name} set value []")
                
            elif class_name == 'ReturnStatement':
                # Skip return statements for now
                continue
                
            else:
                # Unknown node type - skip for now
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
