import re
from .pack import Pack

class ParseError(Exception):
    pass

def parse_mdl(src: str, default_pack_format: int = 48) -> Pack:
    # Simple line-oriented parser with blocks using ":" and indentation for functions
    lines = src.splitlines()

    current_ns = None
    mode = None  # None or "function"
    fn_ns = fn_name = None
    fn_commands = []
    fn_body_indent = None  # indentation level required for function body lines

    # Tag block state
    in_tag = False
    tag_reg = None
    tag_name = None
    tag_values = []

    def flush_function():
        nonlocal fn_ns, fn_name, fn_commands, mode, fn_body_indent
        if mode == "function":
            if fn_ns is None or fn_name is None:
                raise ParseError("Internal function state error")
            p.namespace(fn_ns).function(fn_name, *fn_commands)
            fn_ns = fn_name = None
            fn_commands = []
            mode = None
            fn_body_indent = None

    def flush_tag():
        nonlocal in_tag, tag_reg, tag_name, tag_values
        if in_tag:
            # finalize the open tag block
            p.tag(tag_reg, tag_name, values=tag_values)
            in_tag = False
            tag_reg = None
            tag_name = None
            tag_values = []

    # Preprocess: remove comments (# ...), keep indentation and hashes inside strings
    cleaned = []
    for raw in lines:
        if re.match(r'^\s*#', raw):
            continue
        cleaned.append(raw.rstrip('\n'))

    p = None
    for lineno, raw in enumerate(cleaned, start=1):
        line = raw.rstrip()
        if not line.strip():
            # blank lines are ignored everywhere (including inside blocks)
            continue

        # Count leading spaces (tabs are not supported)
        indent = len(line) - len(line.lstrip(" "))
        if indent % 4 != 0:
            raise ParseError(f"Line {lineno}: indentation must be multiples of 4 spaces")
        text = line.strip()

        # If we were inside a function and we dedented, close the function first
        if mode == "function" and indent < (fn_body_indent or 0):
            flush_function()
            # fall through to parse this line as a directive

        # Lines inside a function body: treat as raw Minecraft commands
        if mode == "function":
            # any non-empty line with indent >= body indent is part of the body
            if indent >= (fn_body_indent or 0):
                fn_commands.append(text)
                continue
            # (otherwise a dedent would have flushed above)

        # Top-level directives only from here on (indent must be 0 for directives)
        # Also ensure we flush any open tag before starting a new directive
        # Pack header
        if indent == 0 and text.startswith("pack "):
            flush_tag()
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
        if indent == 0 and text.startswith("namespace "):
            flush_tag()
            flush_function()
            m = re.match(r'namespace\s+"([a-z0-9_\-\.]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid namespace")
            current_ns = m.group(1)
            continue

        # function start: function "name":
        if indent == 0 and text.startswith("function "):
            flush_tag()
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
            fn_body_indent = indent + 4  # function body must be at least one indent level deeper
            continue

        # hooks
        if indent == 0 and text.startswith("on_tick "):
            flush_tag()
            m = re.match(r'on_tick\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_tick requires a namespaced id")
            p.on_tick(m.group(1))
            continue

        if indent == 0 and text.startswith("on_load "):
            flush_tag()
            m = re.match(r'on_load\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_load requires a namespaced id")
            p.on_load(m.group(1))
            continue

        # tag <registry> "<ns:id>" [replace]:
        if indent == 0 and text.startswith("tag "):
            flush_tag()
            flush_function()
            m = re.match(r'tag\s+(function|item|block|entity_type|fluid|game_event)\s+"([^"]+:[^"]+)"(?:\s+replace)?\s*:\s*$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid tag header")
            tag_reg = m.group(1)
            tag_name = m.group(2)
            tag_values = []
            in_tag = True
            continue  # values gathered on following 'add' lines

        # tag values lines: 'add "<ns:val>"'
        if text.startswith("add "):
            if not in_tag:
                raise ParseError(f"Line {lineno}: 'add' outside of tag block")
            m = re.match(r'add\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid add line")
            tag_values.append(m.group(1))
            continue

        # If we get here:
        # - indent == 0: unknown directive
        # - indent > 0: unexpected indentation outside any block
        if indent == 0:
            raise ParseError(f"Line {lineno}: unknown directive: {text}")
        else:
            raise ParseError(f"Line {lineno}: unexpected indentation")

    # Finalize any open scopes
    flush_function()
    flush_tag()

    return p
