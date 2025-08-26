#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate || true

python -m pip install --upgrade pip
python -m pip install build

python -m build

echo "✅ Built distributions in ./dist"
ls -1 dist
