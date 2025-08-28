#!/usr/bin/env bash
# Git Bash: build sdist + wheel
set -euo pipefail

# Activate venv if present
if [ -f ".venv/Scripts/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

python -m pip install --upgrade pip
python -m pip install build
python -m build

echo "[+] Built distributions in ./dist"
ls -1 dist
