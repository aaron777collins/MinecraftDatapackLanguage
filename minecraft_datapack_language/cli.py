
import argparse, os, sys, json, traceback, re, zipfile, shutil, glob
from .pack import Pack
from .utils import ensure_dir
from .mdl_parser import parse_mdl

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
            # First file requires pack declaration, subsequent files don't
            require_pack = (root_pack is None)
            p = parse_mdl(src, default_pack_format=default_pack_format, require_pack=require_pack)
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
    sample = f"""
# mypack.mdl - minimal example for Minecraft Datapack Language
pack "{args.name}" description "Example datapack" pack_format {args.pack_format}

namespace "example"

function "inner":
    say [example:inner] This is the inner function
    tellraw @a {{"text":"Running inner","color":"yellow"}}

function "hello":
    say [example:hello] Outer says hi
    function example:inner
    tellraw @a {{"text":"Back in hello","color":"aqua"}}

# Conditional example - detect different entity types with enhanced logic
function "conditional_demo":
    if "entity @s[type=minecraft:player]":
        say Player detected!
        effect give @s minecraft:glowing 5 1
        tellraw @a {{"text":"A player is nearby!","color":"green"}}
    else if "entity @s[type=minecraft:zombie]":
        say Zombie detected!
        effect give @s minecraft:poison 5 1
        tellraw @a {{"text":"A zombie is nearby!","color":"red"}}
    else if "entity @s[type=minecraft:creeper]":
        say Creeper detected!
        effect give @s minecraft:resistance 5 1
        tellraw @a {{"text":"A creeper is nearby!","color":"dark_red"}}
    else:
        say Unknown entity detected
        tellraw @a {{"text":"Something unknown is nearby...","color":"gray"}}

# Advanced conditional example - weapon effects system
function "weapon_effects":
    if "entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"minecraft:diamond_sword\"}}}}]":
        say Diamond sword detected!
        effect give @s minecraft:strength 10 1
        effect give @s minecraft:glowing 10 0
    else if "entity @s[type=minecraft:player,nbt={{SelectedItem:{{id:\"minecraft:golden_sword\"}}}}]":
        say Golden sword detected!
        effect give @s minecraft:speed 10 1
        effect give @s minecraft:night_vision 10 0
    else if "entity @s[type=minecraft:player]":
        say Player without special weapon
        effect give @s minecraft:haste 5 0
    else:
        say No player found

# Hook the function into load and tick
on_load "example:hello"
on_tick "example:hello"
on_tick "example:conditional_demo"
on_tick "example:weapon_effects"

# Second namespace with a cross-namespace call
namespace "util"

function "helper":
    say [util:helper] Helping out...

function "boss":
    say [util:boss] Calling example:hello then util:helper
    function example:hello
    function util:helper

# Run boss every tick as well
on_tick "util:boss"

# Function tag examples
tag function "minecraft:load":
    add "example:hello"

tag function "minecraft:tick":
    add "example:hello"
    add "example:conditional_demo"
    add "example:weapon_effects"
    add "util:boss"

# Data tag examples across registries
tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"

"""
    with open(os.path.join(root, "mypack.mdl"), "w", encoding="utf-8") as f:
        f.write(sample.strip() + os.linesep)
    print(f"Created sample at {root}")

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
            parse_mdl(src, default_pack_format=args.pack_format)
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
    sub = p.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="Create a sample .mdl project")
    p_new.add_argument("path")
    p_new.add_argument("--name", default="Minecraft Datapack Language")
    p_new.add_argument("--pack-format", type=int, default=48)
    p_new.set_defaults(func=cmd_new)

    p_build = sub.add_parser("build", help="Build a datapack")
    g = p_build.add_mutually_exclusive_group(required=True)
    g.add_argument("--mdl", help="Path to .mdl source (file or directory)")
    g.add_argument("--src", help="Path to .mdl source (file or directory)")
    g.add_argument("--py-module", help="Python module path exposing create_pack() -> Pack")
    p_build.add_argument("-o", "--out", required=True, help="Output folder (MDL creates <out>/<wrapper>/ and <out>/<wrapper>.zip)")
    p_build.add_argument("--pack-format", type=int, default=48)
    p_build.add_argument("--wrapper", help="Wrapper folder/zip name (default: first namespace or slug of pack name)")
    p_build.add_argument("-v", "--verbose", action="store_true", help="Show detailed processing information")
    p_build.set_defaults(func=cmd_build)

    p_check = sub.add_parser("check", help="Validate .mdl (file or directory)")
    p_check.add_argument("path", help="Path to .mdl file or directory")
    p_check.add_argument("--pack-format", type=int, default=48)
    p_check.add_argument("--json", action="store_true", help="Emit JSON diagnostics")
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.set_defaults(func=cmd_check)

    args = p.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
