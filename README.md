
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

> MDL uses `pack_format >= 48` (Java 1.21) by default, which uses singular names like `function`, `advancement`, and `recipe`.
> Set `--pack-format 47` to emit the legacy plural layout for older versions.

## Install (editable)

```bash
# inside the unzipped folder:
pip install -e .
```

## CLI

```bash
mdl new my_pack --name "My Pack" --pack-format 48
mdl check my_pack/mypack.mdl
mdl build --mdl my_pack/mypack.mdl -o dist/my_pack --pack-format 48
```

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
python -c "import my_pack; from minecraft_datapack_language.cli import main as M; M(['build','--py-module','my_pack','-o','dist/my_pack','--pack-format','48'])"
```

## VS Code

Open `vscode-extension/` in VS Code, run `npm i` then `F5` to launch Extension Dev Host.

- Highlights `.mdl`
- Runs `mdl check` on save and shows inline diagnostics

## References

- Snapshot **24w19a**: tag subdirectory renames (`tags/items→tags/item`, etc.).
- Snapshot **24w21a**: registry folder renames (`functions→function`, `advancements→advancement`, etc.).
- Data pack `pack_format` for 1.21 is **48**, 1.21.4 is **61**.



## CI & Releases

- **CI** runs on push/PR across Linux/macOS/Windows and uploads artifacts.
- **Release** is triggered by pushing a tag like `v0.1.0` or via the **Release** workflow manually.

### Manual release from your machine

```bash
# Make sure you're logged in to GitHub CLI (gh auth login)
./scripts/release.sh v0.1.0 "Initial release"
```

