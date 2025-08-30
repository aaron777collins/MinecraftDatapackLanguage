#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate || true

# Determine MDL command (prefer installed CLI; fallback to module execution)
if command -v mdl &>/dev/null; then
  MDL_CMD="mdl"
else
  MDL_CMD="python3 -m minecraft_datapack_language.cli"
fi

$MDL_CMD --help >/dev/null

# Smoke test: new, check, build
rm -rf tmp_mdl_test || true
mkdir -p tmp_mdl_test
$MDL_CMD new tmp_mdl_test --name "Test Pack" --pack-format 48
$MDL_CMD check tmp_mdl_test/mypack.mdl
$MDL_CMD build --mdl tmp_mdl_test/mypack.mdl -o tmp_mdl_test/dist --pack-format 48

test -f tmp_mdl_test/dist/pack.mcmeta
test -f tmp_mdl_test/dist/data/minecraft/tags/function/tick.json || true

echo "[+] CLI smoke test OK"
