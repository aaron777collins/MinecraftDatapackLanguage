
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
    if os.path.isdir(path):
        return sorted([p for p in glob.glob(os.path.join(path, "**", "*.mdl"), recursive=True)])
    elif os.path.isfile(path):
        return [path]
    else:
        raise SystemExit(f"Path not found: {path}")

def _parse_many(files, default_pack_format: int):
    root_pack = None
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            src = f.read()
        try:
            p = parse_mdl(src, default_pack_format=default_pack_format)
        except Exception as e:
            # Bubble up with filename context
            raise RuntimeError(f"{fp}: {e}")
        if root_pack is None:
            root_pack = p
        else:
            # Ensure consistent pack_format; prefer explicit default
            if p.pack_format != root_pack.pack_format and default_pack_format is not None:
                p.pack_format = default_pack_format
            root_pack.merge(p)
    if root_pack is None:
        raise SystemExit("No .mdl files found")
    return root_pack

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
        f.write(sample.strip() + "\\n")
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
        pack = _parse_many(files, default_pack_format=args.pack_format)
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
            files = _gather_mdl_files(path)
            for fp in files:
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        src = f.read()
                    parse_mdl(src, default_pack_format=args.pack_format)
                except Exception as e:
                    # Try to extract 'Line N:'
                    m = re.search(r'Line (\\d+):\\s*(.*)', str(e))
                    if m:
                        errors.append({"file": fp, "line": int(m.group(1)), "message": m.group(2)})
                    else:
                        errors.append({"file": fp, "line": None, "message": str(e)})
        else:
            with open(path, "r", encoding="utf-8") as f:
                src = f.read()
            parse_mdl(src, default_pack_format=args.pack_format)
    except Exception as e:
        # For top-level failures
        m = re.search(r'Line (\\d+):\\s*(.*)', str(e))
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
