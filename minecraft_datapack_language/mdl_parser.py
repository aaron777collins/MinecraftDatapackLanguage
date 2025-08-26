
import re
from .pack import Pack

class ParseError(Exception):
    pass

def parse_mdl(src: str, default_pack_format: int = 48) -> Pack:
    # Simple line-oriented parser with blocks using ":" and indentation for functions
    lines = src.splitlines()
    i = 0
    pack = None
    current_ns = None
    indent_stack = [0]
    mode = None  # None or "function"
    fn_ns = fn_name = None
    fn_commands = []

    def flush_function():
        nonlocal fn_ns, fn_name, fn_commands, mode
        if mode == "function":
            if fn_ns is None or fn_name is None:
                raise ParseError("Internal function state error")
            p.namespace(fn_ns).function(fn_name, *fn_commands)
            fn_ns = fn_name = None
            fn_commands = []
            mode = None

    # Preprocess: remove comments (# ...), keep indentation
    cleaned = []
    for raw in lines:
        # allow comments after commands
        if "#" in raw:
            idx = raw.find("#")
            # permit JSON braces within tellraw etc (ignore hash inside quotes)
            parts = re.split(r'(".*?")', raw)
            rebuilt = ""
            seen = False
            for part in parts:
                if part.startswith('"') and part.endswith('"'):
                    rebuilt += part
                else:
                    if "#" in part and not seen:
                        part = part.split("#",1)[0]
                        seen = True
                    rebuilt += part
            raw = rebuilt
        cleaned.append(raw.rstrip("\n"))

    p = None
    for lineno, raw in enumerate(cleaned, start=1):
        line = raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent % 4 != 0:
            raise ParseError(f"Line {lineno}: indentation must be multiples of 4 spaces")
        text = line.strip()

        # Pack header
        if text.startswith("pack "):
            if p is not None:
                raise ParseError(f"Line {lineno}: duplicate pack declaration")
            m = re.match(r'pack\s+"([^"]+)"(?:\s+description\s+"([^"]*)")?(?:\s+pack_format\s+(\d+))?$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid pack declaration")
            name, desc, pf = m.groups()
            p = Pack(name=name, description=desc or name, pack_format=int(pf) if pf else default_pack_format)
            continue

        if p is None:
            raise ParseError(f"Line {lineno}: missing pack declaration")

        # namespace
        if text.startswith("namespace "):
            flush_function()
            m = re.match(r'namespace\s+"([a-z0-9_\-\.]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid namespace")
            current_ns = m.group(1)
            continue

        # function start: function "name":
        if text.startswith("function "):
            flush_function()
            m = re.match(r'function\s+"([^"]+)"\s*:\s*$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid function declaration")
            if not current_ns:
                raise ParseError(f"Line {lineno}: function requires a current namespace")
            fn_ns = current_ns
            fn_name = m.group(1)
            fn_commands = []
            mode = "function"
            continue

        if text.startswith("on_tick "):
            m = re.match(r'on_tick\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_tick requires a namespaced id")
            p.on_tick(m.group(1))
            continue

        if text.startswith("on_load "):
            m = re.match(r'on_load\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_load requires a namespaced id")
            p.on_load(m.group(1))
            continue

        # tag <registry> "<ns:id>" [replace]:
        if text.startswith("tag "):
            flush_function()
            m = re.match(r'tag\s+(function|item|block|entity_type|fluid|game_event)\s+"([^"]+:[^"]+)"(?:\s+replace)?\s*:\s*$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid tag header")
            reg = m.group(1)
            name = m.group(2)
            # consume subsequent indented "add" lines until next block
            values = []
            continue  # header; values gathered in following lines

        # Inside function block: any other non-empty line is a command
        if mode == "function":
            # commands are raw, no further parsing
            fn_commands.append(text)
            continue

        # tag values lines: 'add "<ns:val>"' or '# comment already removed'
        if text.startswith("add "):
            m = re.match(r'add\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid add line")
            try:
                reg  # noqa: F821
            except NameError:
                raise ParseError(f"Line {lineno}: 'add' outside of tag block")
            values.append(m.group(1))
            # Lookahead to see if next line starts a new block; we handle finalization when we hit new tag/namespace/pack or EOF
            continue

        # finalize a tag if a new construct starts
        if any(text.startswith(kw) for kw in ("namespace ", "function ", "pack ", "tag ", "on_tick", "on_load")):
            # will be handled at next iteration
            pass

        # unknown directive
        raise ParseError(f"Line {lineno}: unknown directive: {text}")

    # Finalize any open scopes
    flush_function()
    # finalize last tag if any
    try:
        reg  # noqa: F821
        # If 'reg' exists in locals, we have an open tag
        if values:
            p.tag(reg, name, values=values)
    except NameError:
        pass

    return p
