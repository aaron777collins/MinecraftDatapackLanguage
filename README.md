# Minecraft Datapack Language (MDL)

A tiny compiler that lets you write Minecraft datapacks in a simple language (`.mdl`) **or** via a clean Python API, and then compiles to the correct 1.21+ datapack folder layout (singular directories) automatically.

- ✅ Handles the directory renames from snapshots **24w19a** (tag subfolders) and **24w21a** (core registry folders) for you.
- ✅ Easy hooks into `minecraft:tick` and `minecraft:load` via function tags.
- ✅ Creates tags for `function`, `item`, `block`, `entity_type`, `fluid`, and `game_event`.
- ✅ VS Code extension for syntax highlighting, linting, and quick compile.

## Why?

1. **Stop memorizing folder names**: write code, not scaffolding.
2. **Version-aware**: pass the `pack_format`, and MDL emits the right folders.
3. **Flexible**: use `.mdl` **or** Python to build complex packs.

> MDL uses `pack_format >= 48` (Java 1.21) by default (singular names like `function`, `advancement`, `recipe`).  
> Set `--pack-format 47` to emit the legacy plural layout for older versions.

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
```

### Build a whole folder of `.mdl` files
```bash
mdl build --mdl src/ -o dist
# Recursively parses src/**/*.mdl, merges into one pack (errors on duplicate functions).
```

### Validate a folder (JSON diagnostics)
```bash
mdl check --json src/
```

---

## `.mdl` language (minimal)

```mdl
pack "My Pack" description "Demo" pack_format 48

namespace "demo"

function "hello":
    say Hello from MDL!
    tellraw @a {"text":"tick!","color":"green"}

on_load "demo:hello"
on_tick "demo:hello"

# Tag another function to run every tick (from anywhere)
tag function "minecraft:tick":
    add "demo:hello"
```

### Python API

```python
from minecraft_datapack_language import Pack

def create_pack():
    p = Pack("My Pack", description="Example", pack_format=48)
    ns = p.namespace("demo")

    ns.function("hello",
        'say Hello from Python API',
        'tellraw @a {"text":"tick!","color":"aqua"}'
    )
    p.on_tick("demo:hello")
    p.on_load("demo:hello")

    # Item tag
    p.tag("item", "minecraft:swords", values=["minecraft:diamond_sword", "minecraft:netherite_sword"])

    return p
```

Build:
```bash
python -c "import my_pack; from minecraft_datapack_language.cli import main as M; M(['build','--py-module','my_pack','-o','dist','--pack-format','48','--wrapper','mypack'])"
```

---

## VS Code

Open `vscode-extension/`, run:

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