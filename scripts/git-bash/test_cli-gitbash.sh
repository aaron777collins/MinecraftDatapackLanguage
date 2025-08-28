#!/usr/bin/env bash
# Git Bash: CLI smoke test
set -euo pipefail

# Activate venv if present
if [ -f ".venv/Scripts/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

mdl --help >/dev/null

rm -rf tmp_mdl_test || true
mkdir -p tmp_mdl_test
mdl new tmp_mdl_test --name "Test Pack" --pack-format 48
mdl check tmp_mdl_test/mypack.mdl
mdl build --mdl tmp_mdl_test/mypack.mdl -o tmp_mdl_test/dist --pack-format 48

test -f tmp_mdl_test/dist/pack.mcmeta
echo "[+] CLI smoke test OK"
