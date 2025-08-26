
import argparse, os, sys, json, traceback
from .pack import Pack
from .dir_map import get_dir_map
from .utils import ensure_dir
from .mdl_parser import parse_mdl

def cmd_new(args):
    # Create a sample project
    root = os.path.abspath(args.path)
    ensure_dir(root)
    sample = f"""
# mypack.mdl - minimal example for Minecraft Datapack Language
pack "{args.name}" description "Example datapack" pack_format {args.pack_format}

namespace "example"

function "hello":
    say Hello from MDL!
    tellraw @a {{"text":"MDL works","color":"green"}}

on_load "example:hello"
on_tick "example:hello"
"""
    with open(os.path.join(root, "mypack.mdl"), "w", encoding="utf-8") as f:
        f.write(sample.strip() + "\n")
    print(f"Created sample at {root}")

def cmd_build(args):
    # Build from .mdl or Python file (exec-invocation is risky: we only support .mdl here for safety)
    out = os.path.abspath(args.out)
    ensure_dir(out)

    pack = None
    if args.mdl:
        with open(args.mdl, "r", encoding="utf-8") as f:
            src = f.read()
        pack = parse_mdl(src, default_pack_format=args.pack_format)
    else:
        # from python module path containing a function create_pack()
        sys.path.insert(0, os.path.abspath("."))
        mod = __import__(args.py_module)
        if not hasattr(mod, "create_pack"):
            raise SystemExit("Python module must expose create_pack() -> Pack")
        pack = mod.create_pack()

    pack.build(out)
    print(f"Built datapack at {out}")

def cmd_check(args):
    try:
        with open(args.mdl, "r", encoding="utf-8") as f:
            src = f.read()
        parse_mdl(src, default_pack_format=args.pack_format)
        print("OK")
        return 0
    except Exception as e:
        print("ERROR:", e)
        if args.verbose:
            traceback.print_exc()
        return 1

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
    g.add_argument("--mdl", help="Path to .mdl source")
    g.add_argument("--py-module", help="Python module path exposing create_pack() -> Pack")
    p_build.add_argument("-o", "--out", required=True, help="Output folder")
    p_build.add_argument("--pack-format", type=int, default=48)
    p_build.set_defaults(func=cmd_build)

    p_check = sub.add_parser("check", help="Validate .mdl source")
    p_check.add_argument("mdl")
    p_check.add_argument("--pack-format", type=int, default=48)
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.set_defaults(func=cmd_check)

    args = p.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
