#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate || true

mdl --help >/dev/null

# Smoke test: new, check, build
rm -rf tmp_mdl_test || true
mkdir -p tmp_mdl_test
mdl new tmp_mdl_test --name "Test Pack" --pack-format 48
mdl check tmp_mdl_test/mypack.mdl
mdl build --mdl tmp_mdl_test/mypack.mdl -o tmp_mdl_test/dist --pack-format 48

test -f tmp_mdl_test/dist/pack.mcmeta
test -f tmp_mdl_test/dist/data/minecraft/tags/function/tick.json || true

echo "[+] CLI smoke test OK"
