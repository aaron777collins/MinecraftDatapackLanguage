
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
            fn.commands.extend([c.strip() for c in commands if c.strip()])
        return fn

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
    def __init__(self, name: str, description: str = "", pack_format: int = 48):
        self.name = name
        self.description = description or name
        self.pack_format = pack_format
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

    def _process_conditionals(self, ns_name: str, func_name: str, commands: List[str]) -> List[str]:
        """Process conditional blocks in function commands and generate appropriate Minecraft commands."""
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
                if_commands = []
                i += 1
                
                # Collect commands for this if block (until next conditional or end)
                while i < len(commands):
                    next_cmd = commands[i].strip()
                    # Stop if we hit another conditional or end of commands
                    if (re.match(r'^else\s+if\s+"', next_cmd) or 
                        next_cmd == "else:" or 
                        re.match(r'^if\s+"', next_cmd)):
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
                        re.match(r'^if\s+"', next_cmd)):
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
                        re.match(r'^if\s+"', next_cmd)):
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
            
            # Regular command
            processed_commands.append(cmd)
            i += 1
        
        return processed_commands

    def merge(self, other: "Pack"):
        """Merge content of another Pack into this one. Raises on conflicting function names within same namespace."""
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
        mcmeta = {
            "pack": {"pack_format": self.pack_format, "description": self.description}
        }
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
                processed_commands = self._process_conditionals(ns_name, path, fn.commands)
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
                    # Don't process conditionals for generated functions - they should already be clean
                    write_text(file_path, "\n".join(fn.commands))

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
