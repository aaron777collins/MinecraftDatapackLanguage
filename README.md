# Minecraft Datapack Language (MDL)

A tiny compiler that lets you write Minecraft datapacks in a simple language (`.mdl`) **or** via a clean Python API, and then compiles to the correct 1.21+ datapack folder layout (singular directories) automatically.

- ✅ Handles the directory renames from snapshots **24w19a** (tag subfolders) and **24w21a** (core registry folders) for you.
- ✅ Easy hooks into `minecraft:tick` and `minecraft:load` via function tags.
- ✅ Creates tags for `function`, `item`, `block`, `entity_type`, `fluid`, and `game_event`.
- ✅ VS Code extension for syntax highlighting, linting, and quick compile.

> Default **pack_format** is **48** (Java 1.21). Set `--pack-format 47` to emit the legacy plural layout for older versions.

---

## Install

### Option A — from PyPI (recommended for users)
Global, isolated CLI via **pipx**:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath    # reopen terminal
pipx install minecraft-datapack-language

mdl --help
```

Virtualenv (if you prefer):
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install minecraft-datapack-language
```

### Option B — from source (for contributors)
```bash
# inside the repo
python -m pip install -e .
```

---

## Update

- **pipx**: `pipx upgrade minecraft-datapack-language`  
- **pip (venv)**: `pip install -U minecraft-datapack-language`  
- Pin a version: `pipx install "minecraft-datapack-language==1.1.0"`

---

## CLI

```bash
mdl new my_pack --name "My Pack" --pack-format 48
mdl check my_pack/mypack.mdl
mdl build --mdl my_pack/mypack.mdl -o dist --wrapper mypack --pack-format 48
# → dist/mypack/... and dist/mypack.zip

# With verbose output to see file processing
mdl build --mdl my_pack/ -o dist --verbose
```

### Build a whole folder of `.mdl` files
```bash
mdl build --mdl src/ -o dist
# Recursively parses src/**/*.mdl, merges into one pack (errors on duplicate functions).
```

### Build multiple specific `.mdl` files
```bash
mdl build --mdl "src/core.mdl src/features.mdl src/ui.mdl" -o dist
# Parses multiple specific files and merges them into one datapack.
```

### Validate a folder (JSON diagnostics)
```bash
mdl check --json src/
```

---

## Multi-file Support

MDL supports building datapacks from multiple `.mdl` files. This is useful for organizing large projects into logical modules.

### How it works
- **Directory scanning**: When you pass a directory to `--mdl`, MDL recursively finds all `.mdl` files
- **File merging**: Each file is parsed into a `Pack` object, then merged into a single datapack
- **Conflict resolution**: Duplicate function names within the same namespace will cause an error
- **Pack metadata**: The first file's pack declaration (name, description, format) is used as the base

### Best practices
- **One pack declaration per project**: Only the first file's pack declaration is used
- **Organize by namespace**: Consider splitting files by namespace or feature
- **Use descriptive filenames**: `core.mdl`, `combat.mdl`, `ui.mdl` etc.
- **Avoid conflicts**: Ensure function names are unique within each namespace

### Example project structure
```
my_datapack/
├── core.mdl          # pack declaration, main functions
├── combat/
│   ├── weapons.mdl   # combat-related functions
│   └── armor.mdl     # armor-related functions
├── ui/
│   └── hud.mdl       # UI functions
└── data/
    └── recipes.mdl   # recipe definitions
```

Build the entire project:
```bash
mdl build --mdl my_datapack/ -o dist
```

### CLI Options for Multi-file Builds

- `--mdl <path>`: Path to `.mdl` file, directory, or space-separated file list
- `--src <path>`: Alias for `--mdl` (same functionality)
- `-o, --out <dir>`: Output directory for the built datapack
- `--wrapper <name>`: Custom wrapper folder/zip name (default: first namespace or pack name slug)
- `--pack-format <N>`: Minecraft pack format (default: 48 for 1.21+)
- `-v, --verbose`: Show detailed processing information including file merging
- `--py-module <path>`: Alternative: build from Python module with `create_pack()` function

---

## The `.mdl` language

### Grammar you can rely on (based on the parser)
- **pack header** (required once):
  ```mdl
  pack "Name" [description "Desc"] [pack_format N]
  ```
- **namespace** (selects a namespace for following blocks):
  ```mdl
  namespace "example"
  ```
- **function** (colon + indented commands, 4-space indents only):
  ```mdl
  function "hello":
      say hi
      tellraw @a {"text":"ok","color":"green"}
  ```
- **function calls** (one function invoking another with fully qualified ID):
  ```mdl
  function "outer":
      say I will call another function
      function example:hello
  ```
- **hooks** (namespaced ids required):
  ```mdl
  on_load "example:hello"
  on_tick "example:hello"
  ```
- **tags** (supported registries: `function`, `item`, `block`, `entity_type`, `fluid`, `game_event`):
  ```mdl
  tag function "minecraft:tick":
      add "example:hello"
  ```
  The parser accepts an optional `replace` flag on the header (e.g. `tag function "minecraft:tick" replace:`) but replacement behavior is controlled by the pack writer.
- **comments** start with `#`. Hashes inside **quoted strings** are preserved.
- **whitespace**: empty lines are ignored; indentation must be **multiples of four spaces** (tabs are invalid).

> Inside a function block, **every non-empty line** is emitted almost verbatim as a Minecraft command. Comments are stripped out and multi-line commands are automatically wrapped. See below for details.

### Comments

MDL supports comments in a way that matches how Minecraft actually interprets them:

- **Full-line comments** (a line starting with `#`) are ignored by the parser.
- **Inline `#` characters** are preserved inside function bodies, so you can still use them the way `mcfunction` normally allows.

Example:

```mdl
pack "Comment Demo" description "Testing comments"

namespace "demo"

function "comments":
    # This whole line is ignored by MDL
    say Hello # This inline comment is preserved
    tellraw @a {"text":"World","color":"blue"} # Inline too!
```

When compiled, the resulting function looks like:

```mcfunction
say Hello # This inline comment is preserved
tellraw @a {"text":"World","color":"blue"} # Inline too!
```

Notice how the full-line `#` never makes it into the `.mcfunction`, but the inline ones do.

---

### Multi-line Commands

Long JSON commands can be split across multiple lines with a trailing backslash `\`.  
MDL will join them back together before writing the final `.mcfunction`.

Example:

```mdl
pack "Multi-line Demo"

namespace "demo"

function "multiline":
    tellraw @a \
        {"text":"This text is really, really long so we split it",\
         "color":"gold"}
```

When compiled, the function is a single line:

```mcfunction
tellraw @a {"text":"This text is really, really long so we split it","color":"gold"}
```

---

## FULL example (nested calls + multi-namespace)

```mdl
# mypack.mdl - minimal example for Minecraft Datapack Language
pack "Minecraft Datapack Language" description "Example datapack" pack_format 48

namespace "example"

function "inner":
    say [example:inner] This is the inner function
    tellraw @a {"text":"Running inner","color":"yellow"}

function "hello":
    say [example:hello] Outer says hi
    function example:inner
    tellraw @a {"text":"Back in hello","color":"aqua"}

# Hook the function into load and tick
on_load "example:hello"
on_tick "example:hello"

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
    add "util:boss"

# Data tag examples across registries
tag item "example:swords":
    add "minecraft:diamond_sword"
    add "minecraft:netherite_sword"

tag block "example:glassy":
    add "minecraft:glass"
    add "minecraft:tinted_glass"
```

### What this demonstrates
- **Nested-like function composition** (`function example:inner` inside `function "hello"`).
- **Multiple namespaces** (`example`, `util`) calling each other with fully-qualified IDs.
- **Lifecycle hooks** (`on_load`, `on_tick`) on both `example:hello` and `util:boss`.
- **Function tags** to participate in vanilla tags (`minecraft:load`, `minecraft:tick`).
- **Data tags** (`item`, `block`) in addition to function tags.

---

## Python API equivalent

```python
from minecraft_datapack_language import Pack

def build_pack():
    p = Pack(name="Minecraft Datapack Language",
             description="Example datapack",
             pack_format=48)

    ex = p.namespace("example")
    ex.function("inner",
        'say [example:inner] This is the inner function',
        'tellraw @a {"text":"Running inner","color":"yellow"}'
    )
    ex.function("hello",
        'say [example:hello] Outer says hi',
        'function example:inner',
        'tellraw @a {"text":"Back in hello","color":"aqua"}'
    )

    # Hooks for example namespace
    p.on_load("example:hello")
    p.on_tick("example:hello")

    util = p.namespace("util")
    util.function("helper",
        'say [util:helper] Helping out...'
    )
    util.function("boss",
        'say [util:boss] Calling example:hello then util:helper',
        'function example:hello',
        'function util:helper'
    )

    # Tick hook for util namespace
    p.on_tick("util:boss")

    # Function tags
    p.tag("function", "minecraft:load", values=["example:hello"])
    p.tag("function", "minecraft:tick", values=["example:hello", "util:boss"])

    # Data tags
    p.tag("item",  "example:swords", values=["minecraft:diamond_sword", "minecraft:netherite_sword"])
    p.tag("block", "example:glassy", values=["minecraft:glass", "minecraft:tinted_glass"])

    return p
```

Build it:
```bash
python - <<'PY'
from my_pack_module import build_pack
from minecraft_datapack_language.cli import main as M
# write to dist/ with a wrapper folder name 'mypack'
p = build_pack()
M(['build', '--py-object', 'my_pack_module:build_pack', '-o', 'dist', '--wrapper', 'mypack', '--pack-format', '48'])
PY
```

---

## VS Code

Open `vscode-extension/`, then:

```bash
npm i
# Press F5 to launch the Extension Dev Host
```

- Highlights `.mdl`
- Runs `mdl check` on save and shows inline diagnostics
- **MDL: Build current file** prompts for output folder and optional wrapper
- **MDL: Check Workspace** validates the whole workspace

---

## CI & Releases

- **CI** runs on push/PR across Linux/macOS/Windows and uploads artifacts.
- **Release** is triggered by pushing a tag like `v1.0.0` or via the Release workflow manually.
- Versions are derived from git tags via **setuptools-scm**; tag `vX.Y.Z` → package version `X.Y.Z`.

### Local release helper
```bash
# requires GitHub CLI: gh auth login
./scripts/release.sh patch  "Fixes"
./scripts/release.sh minor  "Features"
./scripts/release.sh major  "Breaking"
./scripts/release.sh v1.2.3 "Exact version"
```
