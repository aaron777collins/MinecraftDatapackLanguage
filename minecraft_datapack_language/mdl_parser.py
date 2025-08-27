import re
from .pack import Pack

class ParseError(Exception):
    pass

def parse_mdl(src: str, default_pack_format: int = 48, require_pack: bool = True) -> Pack:
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

    # Recipe block state
    in_recipe = False
    recipe_name = None
    recipe_data = {}
    recipe_indent = None

    # === Multi-line command joiner state (for function bodies) ===
    current_cmd = ""     # buffered logical command
    brace = 0            # '{' ... '}'
    bracket = 0          # '[' ... ']'
    in_str = False       # double-quoted JSON strings only (mcfunction uses "...")
    # Keep a rough pointer to where the current command started for nicer errors
    current_cmd_start_line = None

    def update_nesting(segment: str):
        """Update quote/brace/bracket state for a line segment."""
        nonlocal brace, bracket, in_str
        i = 0
        while i < len(segment):
            c = segment[i]
            if c == '"' and (i == 0 or segment[i - 1] != '\\'):
                in_str = not in_str
            elif not in_str:
                if c == '{':
                    brace += 1
                elif c == '}':
                    brace -= 1
                elif c == '[':
                    bracket += 1
                elif c == ']':
                    bracket -= 1
            i += 1

    def push_cmd_if_complete(force: bool = False):
        """If the buffered command is complete (balanced and not in a string) or force=True, append it."""
        nonlocal current_cmd, brace, bracket, in_str, fn_commands, current_cmd_start_line
        if not current_cmd:
            return
        if force:
            # On force, ensure we're not mid-quote or unbalanced; else raise a clear error.
            if in_str or brace != 0 or bracket != 0:
                start = current_cmd_start_line if current_cmd_start_line is not None else "?"
                raise ParseError(f"Unterminated multi-line command starting at line {start}")
            fn_commands.append(current_cmd.strip())
            current_cmd = ""
            current_cmd_start_line = None
            return
        if not in_str and brace == 0 and bracket == 0:
            fn_commands.append(current_cmd.strip())
            current_cmd = ""
            current_cmd_start_line = None

    def buffer_segment(seg: str, lineno: int):
        """Append a segment of a function-body line to current_cmd, tracking nesting and continuations."""
        nonlocal current_cmd, current_cmd_start_line
        s = seg.rstrip()
        # Support explicit line continuation with backslash at end of the physical line
        forced_continuation = s.endswith("\\")
        if forced_continuation:
            s = s[:-1].rstrip()

        if current_cmd:
            current_cmd += " " + s
        else:
            current_cmd = s
            current_cmd_start_line = lineno

        update_nesting(s)
        # Only push when balanced and not inside quotes and not forced continuation
        if not forced_continuation:
            push_cmd_if_complete(force=False)

    def flush_function():
        nonlocal fn_ns, fn_name, fn_commands, mode, fn_body_indent
        # Before closing, finalize any buffered multi-line command
        push_cmd_if_complete(force=True)
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

    def flush_recipe():
        nonlocal in_recipe, recipe_name, recipe_data
        if in_recipe:
            # finalize the open recipe block
            try:
                import json
                recipe_json = json.loads(recipe_data)
                p.namespace(current_ns).recipe(recipe_name, recipe_json)
            except json.JSONDecodeError as e:
                raise ParseError(f"Invalid JSON in recipe {recipe_name}: {e}")
            in_recipe = False
            recipe_name = None
            recipe_data = {}

    # Preprocess: keep only full-line '#' comments; do not strip inline '#'
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

        # Lines inside a function body: join multi-line commands safely
        if mode == "function":
            # any non-empty line with indent >= body indent is part of the body
            if indent >= (fn_body_indent or 0):
                buffer_segment(text, lineno)
                continue
            # (otherwise a dedent would have flushed above)

        # Top-level directives only from here on (indent must be 0 for directives)
        # Also ensure we flush any open tag before starting a new directive
        # Pack header
        if indent == 0 and text.startswith("pack "):
            flush_tag()
            flush_recipe()
            if p is not None:
                raise ParseError(f"Line {lineno}: duplicate pack declaration")
            m = re.match(r'pack\s+"([^"]+)"(?:\s+description\s+"([^"]*)")?(?:\s+pack_format\s+(\d+))?(?:\s+min_format\s+\[([^\]]+)\])?(?:\s+max_format\s+\[([^\]]+)\])?(?:\s+min_engine_version\s+"([^"]*)")?$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid pack declaration")
            name, desc, pf, minf, maxf, mev = m.groups()
            
            # Parse min_format if provided
            min_format = None
            if minf:
                try:
                    parts = [int(x.strip()) for x in minf.split(',')]
                    min_format = parts[0] if len(parts) == 1 else parts
                except ValueError:
                    raise ParseError(f"Line {lineno}: invalid min_format format")
            
            # Parse max_format if provided
            max_format = None
            if maxf:
                try:
                    parts = [int(x.strip()) for x in maxf.split(',')]
                    max_format = parts[0] if len(parts) == 1 else parts
                except ValueError:
                    raise ParseError(f"Line {lineno}: invalid max_format format")
            
            p = Pack(
                name=name, 
                description=desc or name, 
                pack_format=int(pf) if pf else default_pack_format,
                min_format=min_format,
                max_format=max_format,
                min_engine_version=mev
            )
            continue

        if p is None:
            if require_pack:
                raise ParseError(f"Line {lineno}: missing pack declaration")
            else:
                # In module mode, create a minimal pack for merging
                p = Pack(name="module", description="Module", pack_format=default_pack_format)

        # namespace
        if indent == 0 and text.startswith("namespace "):
            flush_tag()
            flush_recipe()
            flush_function()
            m = re.match(r'namespace\s+"([a-z0-9_\-\.]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid namespace")
            current_ns = m.group(1)
            continue

        # function start: function "name":
        if indent == 0 and text.startswith("function "):
            flush_tag()
            flush_recipe()
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
            # reset joiner state for the new function
            current_cmd = ""
            brace = bracket = 0
            in_str = False
            current_cmd_start_line = None
            continue

        # hooks
        if indent == 0 and text.startswith("on_tick "):
            flush_tag()
            flush_recipe()
            m = re.match(r'on_tick\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_tick requires a namespaced id")
            p.on_tick(m.group(1))
            continue

        if indent == 0 and text.startswith("on_load "):
            flush_tag()
            flush_recipe()
            m = re.match(r'on_load\s+"([^"]+:[^"]+)"$', text)
            if not m:
                raise ParseError(f"Line {lineno}: on_load requires a namespaced id")
            p.on_load(m.group(1))
            continue

        # recipe "name":
        if indent == 0 and text.startswith("recipe "):
            flush_tag()
            flush_function()
            m = re.match(r'recipe\s+"([^"]+)"\s*:\s*$', text)
            if not m:
                raise ParseError(f"Line {lineno}: invalid recipe declaration")
            if not current_ns:
                raise ParseError(f"Line {lineno}: recipe requires a current namespace")
            recipe_name = m.group(1)
            recipe_data = {}
            in_recipe = True
            recipe_indent = indent + 4
            continue

        # tag <registry> "<ns:id>" [replace]:
        if indent == 0 and text.startswith("tag "):
            flush_tag()
            flush_recipe()
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

        # Recipe data lines (JSON)
        if in_recipe and indent >= recipe_indent:
            # Accumulate JSON data
            if recipe_data == {}:
                recipe_data = text
            else:
                recipe_data += "\n" + text
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
    flush_recipe()

    return p
