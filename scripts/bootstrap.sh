#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/bootstrap.sh  [PYTHON=python3]
PYTHON_BIN="${PYTHON:-python3}"

$PYTHON_BIN -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e .

echo "[+] Virtualenv ready. Activate with: source .venv/bin/activate"
echo "[+] Try: mdl --help"
