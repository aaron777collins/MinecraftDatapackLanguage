
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import os, json
from .dir_map import get_dir_map, DirMap
from .utils import ensure_dir, write_json, write_text, ns_path

@dataclass
class Function:
    name: str  # name within namespace e.g. "tick" or "folder/thing"
    commands: List[str] = field(default_factory=list)

@dataclass
class TagFile:
    path: str  # e.g. "minecraft:tick" or "my_ns:foo"
    values: List[str] = field(default_factory=list)
    replace: bool = False

@dataclass
class Recipe:
    name: str
    data: dict

@dataclass
class Advancement:
    name: str
    data: dict

@dataclass
class LootTable:
    name: str
    data: dict

@dataclass
class Predicate:
    name: str
    data: dict

@dataclass
class ItemModifier:
    name: str
    data: dict

@dataclass
class Structure:
    name: str
    data: dict  # we treat this as JSON until external tools produce .nbt

@dataclass
class Namespace:
    name: str
    functions: Dict[str, Function] = field(default_factory=dict)
    recipes: Dict[str, Recipe] = field(default_factory=dict)
    advancements: Dict[str, Advancement] = field(default_factory=dict)
    loot_tables: Dict[str, LootTable] = field(default_factory=dict)
    predicates: Dict[str, Predicate] = field(default_factory=dict)
    item_modifiers: Dict[str, ItemModifier] = field(default_factory=dict)
    structures: Dict[str, Structure] = field(default_factory=dict)

    def function(self, name: str, *commands: str) -> Function:
        fn = self.functions.setdefault(name, Function(name, []))
        if commands:
            # Process control flow immediately when commands are added
            processed_commands = self._process_control_flow(name, commands)
            fn.commands.extend(processed_commands)
        return fn
    
    def _process_control_flow(self, func_name: str, commands: List[str]) -> List[str]:
        """Process conditional blocks and loops in function commands and generate appropriate Minecraft commands."""
        import re
        
        processed_commands = []
        i = 0
        
        while i < len(commands):
            cmd = commands[i].strip()
            
            # Check for if statement
            if_match = re.match(r'^if\s+"([^"]+)"\s*:\s*$', cmd)
            if if_match:
                condition = if_match.group(1)
                if_commands = []
                i += 1
                
                # Collect commands for this if block (until next conditional or end)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another conditional or end of commands
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        next_cmd == "else:" or 
                        re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        if_commands.append(next_cmd)
                    i += 1
                
                # Generate conditional function
                conditional_func_name = f"{func_name}_if_{len(processed_commands)}"
                self.function(conditional_func_name, *if_commands)
                
                # Add conditional execution command
                processed_commands.append(f"execute if {condition} run function {self.name}:{conditional_func_name}")
                continue
            
            # Check for else if statement
            elif_match = re.match(r'^else\s+if\s+"([^"]+)"\s*:\s*$', cmd)
            if elif_match:
                condition = elif_match.group(1)
                elif_commands = []
                i += 1
                
                # Collect commands for this else if block
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        next_cmd == "else:" or 
                        re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:
                        elif_commands.append(next_cmd)
                    i += 1
                
                # Generate else if function
                elif_func_name = f"{func_name}_elif_{len(processed_commands)}"
                self.function(elif_func_name, *elif_commands)
                
                # Add else if execution command
                processed_commands.append(f"execute if {condition} run function {self.name}:{elif_func_name}")
                continue
            
            # Check for else statement
            elif cmd == "else:":
                else_commands = []
                i += 1
                
                # Collect commands for this else block
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    if (re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:
                        else_commands.append(next_cmd)
                    i += 1
                
                # Generate else function
                else_func_name = f"{func_name}_else_{len(processed_commands)}"
                self.function(else_func_name, *else_commands)
                
                # Add else execution command
                processed_commands.append(f"execute run function {self.name}:{else_func_name}")
                continue
            
            # Check for while loop
            while_match = re.match(r'^while\s+"([^"]+)"\s*:\s*$', cmd)
            if while_match:
                condition = while_match.group(1)
                loop_commands = []
                i += 1
                
                # Collect commands for this while block
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    if (re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:
                        loop_commands.append(next_cmd)
                    i += 1
                
                # Generate while loop function
                loop_func_name = f"{func_name}_while_{len(processed_commands)}"
                self.function(loop_func_name, *loop_commands)
                
                # Generate while loop control function
                loop_control_func_name = f"{func_name}_while_control_{len(processed_commands)}"
                loop_control_commands = [
                    f"execute if {condition} run function {self.name}:{loop_func_name}",
                    f"execute if {condition} run function {self.name}:{loop_control_func_name}"
                ]
                self.function(loop_control_func_name, *loop_control_commands)
                
                # Add initial while loop call
                processed_commands.append(f"execute if {condition} run function {self.name}:{loop_control_func_name}")
                continue
            
            # Check for for loop
            for_match = re.match(r'^for\s+(\w+)\s+in\s+(.+?)\s*:\s*$', cmd)
            if for_match:
                var_name = for_match.group(1)
                collection_name = for_match.group(2)
                loop_commands = []
                i += 1
                
                # Collect ALL commands for this for block (including nested control structures)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another top-level control structure
                    if (re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^else\s+if\s+"', next_cmd) or
                        next_cmd == "else:" or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        loop_commands.append(next_cmd)
                    i += 1
                
                # Generate for loop function with processed conditionals
                for_func_name = f"{func_name}_for_{len(processed_commands)}"
                # Process the loop body commands to handle conditionals
                processed_loop_commands = self._process_control_flow(for_func_name, loop_commands)
                self.function(for_func_name, *processed_loop_commands)
                
                # Generate for loop control function that iterates through collection
                for_control_func_name = f"{func_name}_for_control_{len(processed_commands)}"
                for_control_commands = [
                    f"execute as {collection_name} run function {self.name}:{for_func_name}"
                ]
                self.function(for_control_func_name, *for_control_commands)
                
                # Add initial for loop call
                processed_commands.append(f"execute if entity {collection_name} run function {self.name}:{for_control_func_name}")
                continue
            
            # Regular command
            processed_commands.append(cmd)
            i += 1
        
        return processed_commands

    def recipe(self, name: str, data: dict) -> Recipe:
        r = Recipe(name, data)
        self.recipes[name] = r
        return r

    def advancement(self, name: str, data: dict) -> Advancement:
        a = Advancement(name, data)
        self.advancements[name] = a
        return a

    def loot_table(self, name: str, data: dict) -> LootTable:
        lt = LootTable(name, data)
        self.loot_tables[name] = lt
        return lt

    def predicate(self, name: str, data: dict) -> Predicate:
        p = Predicate(name, data)
        self.predicates[name] = p
        return p

    def item_modifier(self, name: str, data: dict) -> ItemModifier:
        im = ItemModifier(name, data)
        self.item_modifiers[name] = im
        return im

    def structure(self, name: str, data: dict) -> Structure:
        s = Structure(name, data)
        self.structures[name] = s
        return s

@dataclass
class Tag:
    registry: str  # "function", "item", "block", "entity_type", "fluid", "game_event"
    name: str      # namespaced id e.g. "minecraft:tick" or "myns:my_tag"
    values: List[str] = field(default_factory=list)
    replace: bool = False

class Pack:
    def __init__(self, name: str, description: str = "", pack_format: int = 48, min_format: Optional[Union[int, List[int]]] = None, max_format: Optional[Union[int, List[int]]] = None, min_engine_version: Optional[str] = None):
        self.name = name
        self.description = description or name
        self.pack_format = pack_format
        self.min_format = min_format
        self.max_format = max_format
        self.min_engine_version = min_engine_version
        self.namespaces: Dict[str, Namespace] = {}
        self.tags: List[Tag] = []
        # helpful shortcuts
        self._tick_functions: List[str] = []
        self._load_functions: List[str] = []

    # Namespace management
    def namespace(self, name: str) -> Namespace:
        ns = self.namespaces.get(name)
        if ns is None:
            ns = Namespace(name=name)
            self.namespaces[name] = ns
        return ns

    # Function shortcuts
    def fn(self, ns: str, path: str, *commands: str) -> Function:
        return self.namespace(ns).function(path, *commands)

    def on_tick(self, full_id: str):
        """Add a function id to minecraft:tick tag for running every tick."""
        self._tick_functions.append(full_id)

    def on_load(self, full_id: str):
        """Add a function id to minecraft:load tag for running on world load."""
        self._load_functions.append(full_id)

    # Tag builder
    def tag(self, registry: str, name: str, values: Optional[List[str]] = None, replace: bool = False) -> Tag:
        t = Tag(registry=registry, name=name, values=list(values or []), replace=replace)
        self.tags.append(t)
        return t

    def _process_list_access_in_condition(self, condition: str, ns_name: str, func_name: str, cmd_index: int) -> str:
        """Process list access expressions in conditions and convert them to valid Minecraft syntax."""
        import re
        
        # Pattern to match list access expressions like list_name[index]
        list_access_pattern = r'(\w+)\[(\w+)\]'
        
        def replace_list_access(match):
            list_name = match.group(1)
            index_var = match.group(2)
            
            # For now, just return the list name since we can't easily process this in conditions
            # The actual list access will need to be handled in the CLI when processing variable assignments
            return list_name
        
        # Replace list access expressions in the condition
        processed_condition = re.sub(list_access_pattern, replace_list_access, condition)
        
        return processed_condition

    def _process_control_flow(self, ns_name: str, func_name: str, commands: List[str]) -> List[str]:
        """Process conditional blocks and loops in function commands and generate appropriate Minecraft commands."""
        import re
        
        processed_commands = []
        i = 0
        previous_conditions = []  # Track conditions for proper else if logic
        
        while i < len(commands):
            cmd = commands[i].strip()
            
            # Check for if statement
            if_match = re.match(r'^if\s+"([^"]+)"\s*:\s*$', cmd)
            if if_match:
                condition = if_match.group(1)
                
                # Process list access expressions in conditions
                condition = self._process_list_access_in_condition(condition, ns_name, func_name, len(processed_commands))
                
                if_commands = []
                i += 1
                
                # Collect commands for this if block (until next conditional or end)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another conditional or end of commands
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        next_cmd == "else:" or 
                        re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        if_commands.append(next_cmd)
                    i += 1
                
                # Generate conditional function
                conditional_func_name = f"{func_name}_if_{len(processed_commands)}"
                self.namespace(ns_name).function(conditional_func_name, *if_commands)
                
                # Add execute command
                processed_commands.append(f"execute if {condition} run function {ns_name}:{conditional_func_name}")
                previous_conditions = [condition]  # Reset for new if chain
                continue
            
            # Check for else if statement
            elif_match = re.match(r'^else\s+if\s+"([^"]+)"\s*:\s*$', cmd)
            if elif_match:
                condition = elif_match.group(1)
                elif_commands = []
                i += 1
                
                # Collect commands for this else if block (until next conditional or end)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another conditional or end of commands
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        next_cmd == "else:" or 
                        re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        elif_commands.append(next_cmd)
                    i += 1
                
                # Generate conditional function
                conditional_func_name = f"{func_name}_elif_{len(processed_commands)}"
                self.namespace(ns_name).function(conditional_func_name, *elif_commands)
                
                # Build execute command with all previous conditions negated
                execute_parts = []
                for prev_condition in previous_conditions:
                    execute_parts.append(f"unless {prev_condition}")
                execute_parts.append(f"if {condition}")
                execute_parts.append(f"run function {ns_name}:{conditional_func_name}")
                
                processed_commands.append("execute " + " ".join(execute_parts))
                previous_conditions.append(condition)
                continue
            
            # Check for else statement
            elif cmd == "else:":
                else_commands = []
                i += 1
                
                # Collect commands for this else block (until end)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another conditional or end of commands
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        else_commands.append(next_cmd)
                    i += 1
                
                # Generate conditional function
                conditional_func_name = f"{func_name}_else"
                self.namespace(ns_name).function(conditional_func_name, *else_commands)
                
                # Build execute command with all previous conditions negated
                execute_parts = []
                for prev_condition in previous_conditions:
                    execute_parts.append(f"unless {prev_condition}")
                execute_parts.append(f"run function {ns_name}:{conditional_func_name}")
                
                processed_commands.append("execute " + " ".join(execute_parts))
                previous_conditions = []  # Reset for next if chain
                continue
            
            # Check for while loop
            while_match = re.match(r'^while\s+"([^"]+)"\s*:\s*$', cmd)
            if while_match:
                condition = while_match.group(1)
                loop_commands = []
                i += 1
                
                # Collect commands for this while block (until end or next control structure)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another control structure
                    if (re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^else\s+if\s+"', next_cmd) or
                        next_cmd == "else:" or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)):
                        break
                    if next_cmd:  # Skip empty lines
                        loop_commands.append(next_cmd)
                    i += 1
                
                # Generate loop function
                loop_func_name = f"{func_name}_while_{len(processed_commands)}"
                self.namespace(ns_name).function(loop_func_name, *loop_commands)
                
                # Generate loop control function that calls itself if condition is still true
                loop_control_func_name = f"{func_name}_while_control_{len(processed_commands)}"
                loop_control_commands = [
                    f"execute if {condition} run function {ns_name}:{loop_func_name}",
                    f"execute if {condition} run function {ns_name}:{loop_control_func_name}"
                ]
                self.namespace(ns_name).function(loop_control_func_name, *loop_control_commands)
                
                # Add initial loop call
                processed_commands.append(f"execute if {condition} run function {ns_name}:{loop_control_func_name}")
                continue
            
            # Check for for loop
            for_match = re.match(r'^for\s+(\w+)\s+in\s+(.+?)\s*:\s*$', cmd)
            if for_match:
                var_name = for_match.group(1)
                collection_name = for_match.group(2)
                loop_commands = []
                i += 1
                
                # Collect commands for this for block (including nested control structures)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another top-level control structure (same indentation level)
                    if (re.match(r'^if\s+"', next_cmd) or
                        re.match(r'^else\s+if\s+"', next_cmd) or
                        next_cmd == "else:" or
                        re.match(r'^while\s+"', next_cmd) or
                        re.match(r'^for\s+', next_cmd)) and not next_cmd.startswith('    '):
                        break
                    if next_cmd:  # Skip empty lines
                        loop_commands.append(next_cmd)
                    i += 1
                
                # Generate for loop function with processed conditionals
                for_func_name = f"{func_name}_for_{len(processed_commands)}"
                # Process the loop body commands to handle conditionals
                processed_loop_commands = self._process_conditionals(loop_commands, for_func_name, ns_name)
                self.namespace(ns_name).function(for_func_name, *processed_loop_commands)
                
                # Generate for loop control function that iterates through collection
                for_control_func_name = f"{func_name}_for_control_{len(processed_commands)}"
                for_control_commands = [
                    f"execute as {collection_name} run function {ns_name}:{for_func_name}"
                ]
                self.namespace(ns_name).function(for_control_func_name, *for_control_commands)
                
                # Add initial for loop call
                processed_commands.append(f"execute if entity {collection_name} run function {ns_name}:{for_control_func_name}")
                continue
            
            # Regular command
            processed_commands.append(cmd)
            i += 1
        
        return processed_commands

    def merge(self, other: "Pack"):
        """Merge content of another Pack into this one. Raises on conflicting function names within same namespace."""
        # Preserve metadata from the root pack (self) - don't override with other pack's metadata
        # This ensures that the first pack's metadata (min_format, max_format, min_engine_version) is preserved
        
        # Namespaces
        for ns_name, ns_other in other.namespaces.items():
            ns_self = self.namespaces.get(ns_name)
            if ns_self is None:
                self.namespaces[ns_name] = ns_other
                continue
            # functions
            for fname, fobj in ns_other.functions.items():
                if fname in ns_self.functions:
                    raise ValueError(f"Duplicate function '{ns_name}:{fname}' while merging")
                ns_self.functions[fname] = fobj
            # simple maps
            ns_self.recipes.update(ns_other.recipes)
            ns_self.advancements.update(ns_other.advancements)
            ns_self.loot_tables.update(ns_other.loot_tables)
            ns_self.predicates.update(ns_other.predicates)
            ns_self.item_modifiers.update(ns_other.item_modifiers)
            ns_self.structures.update(ns_other.structures)

        # Tags and hooks
        self.tags.extend(other.tags)
        self._tick_functions.extend(other._tick_functions)
        self._load_functions.extend(other._load_functions)

    # Compilation
    def build(self, out_dir: str):
        dm: DirMap = get_dir_map(self.pack_format)

        # pack.mcmeta
        pack_meta = {"description": self.description}
        
        # Handle pack format metadata based on version
        if self.pack_format < 82:
            # For older formats, use pack_format and supported_formats
            pack_meta["pack_format"] = self.pack_format
            if hasattr(self, 'supported_formats') and self.supported_formats:
                pack_meta["supported_formats"] = self.supported_formats
        else:
            # For format 82+, use min_format and max_format
            if self.min_format is not None:
                pack_meta["min_format"] = self.min_format
            if self.max_format is not None:
                pack_meta["max_format"] = self.max_format
            # pack_format is optional for 82+
            if self.pack_format:
                pack_meta["pack_format"] = self.pack_format
                
        # Add engine version if specified
        if self.min_engine_version:
            pack_meta["min_engine_version"] = self.min_engine_version
            
        mcmeta = {"pack": pack_meta}
        write_json(os.path.join(out_dir, "pack.mcmeta"), mcmeta)

        data_root = os.path.join(out_dir, "data")
        ensure_dir(data_root)

        # Namespaces
        for ns_name, ns in self.namespaces.items():
            ns_root = os.path.join(data_root, ns_name)
            # Functions
            functions_to_process = list(ns.functions.items())
            processed_functions = set()
            generated_functions = set()  # Track functions created during conditional processing
            
            for path, fn in functions_to_process:
                fn_dir = os.path.join(ns_root, dm.function, os.path.dirname(path))
                file_path = os.path.join(ns_root, dm.function, f"{path}.mcfunction")
                ensure_dir(fn_dir)
                
                # Process conditionals in function commands
                print(f"Processing function: {ns_name}:{path}")
                # Check if commands are already in new format (no semicolons, no old-style control flow)
                if any(cmd.endswith(';') for cmd in fn.commands):
                    # Old format - process with control flow
                    processed_commands = self._process_control_flow(ns_name, path, fn.commands)
                else:
                    # New format - commands are already processed
                    processed_commands = fn.commands
                write_text(file_path, "\n".join(processed_commands))
                processed_functions.add(path)
                
                # Track any new functions that were created during conditional processing
                for new_path in ns.functions.keys():
                    if new_path not in [f[0] for f in functions_to_process]:
                        generated_functions.add(new_path)
            
            # Write any additional functions created during conditional processing
            for path, fn in ns.functions.items():
                if path not in processed_functions and path in generated_functions:  # Only write generated functions
                    fn_dir = os.path.join(ns_root, dm.function, os.path.dirname(path))
                    file_path = os.path.join(ns_root, dm.function, f"{path}.mcfunction")
                    ensure_dir(fn_dir)
                    # Process loops in generated functions (conditionals are already processed)
                    if any(cmd.endswith(';') for cmd in fn.commands):
                        # Old format - process with control flow
                        processed_commands = self._process_control_flow(ns_name, path, fn.commands)
                    else:
                        # New format - commands are already processed
                        processed_commands = fn.commands
                    write_text(file_path, "\n".join(processed_commands))

            # Recipes, Advancements, etc.
            for name, r in ns.recipes.items():
                write_json(os.path.join(ns_root, dm.recipe, f"{name}.json"), r.data)
            for name, a in ns.advancements.items():
                write_json(os.path.join(ns_root, dm.advancement, f"{name}.json"), a.data)
            for name, lt in ns.loot_tables.items():
                write_json(os.path.join(ns_root, dm.loot_table, f"{name}.json"), lt.data)
            for name, p in ns.predicates.items():
                write_json(os.path.join(ns_root, dm.predicate, f"{name}.json"), p.data)
            for name, im in ns.item_modifiers.items():
                write_json(os.path.join(ns_root, dm.item_modifier, f"{name}.json"), im.data)
            for name, s in ns.structures.items():
                # Structure typically NBT; here we store JSON placeholder
                write_json(os.path.join(ns_root, dm.structure, f"{name}.json"), s.data)

        # Autowire special function tags
        if self._tick_functions:
            self.tags.append(Tag("function", "minecraft:tick", values=self._tick_functions))
        if self._load_functions:
            self.tags.append(Tag("function", "minecraft:load", values=self._load_functions))

        # Tags
        for t in self.tags:
            if ":" not in t.name:
                raise ValueError(f"Tag name must be namespaced (e.g., 'minecraft:tick'), got {t.name}")
            ns, path = t.name.split(":", 1)

            if t.registry == "function":
                tag_path = dm.tags_function
            elif t.registry == "item":
                tag_path = dm.tags_item
            elif t.registry == "block":
                tag_path = dm.tags_block
            elif t.registry == "entity_type":
                tag_path = dm.tags_entity_type
            elif t.registry == "fluid":
                tag_path = dm.tags_fluid
            elif t.registry == "game_event":
                tag_path = dm.tags_game_event
            else:
                raise ValueError(f"Unknown tag registry: {t.registry}")

            tag_obj = {"replace": t.replace, "values": t.values}
            write_json(os.path.join(data_root, ns, tag_path, f"{path}.json"), tag_obj)
