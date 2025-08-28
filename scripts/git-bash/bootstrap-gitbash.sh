#!/usr/bin/env bash
# Git Bash bootstrap: create venv + editable install
# Works on Windows Git Bash or MSYS2/MinGW environments.
set -euo pipefail

# Prefer 'py -3' on Windows; fall back to python3/python
if command -v py >/dev/null 2>&1; then
  PYTHON_BIN="${PYTHON:-py -3}"
else
  PYTHON_BIN="${PYTHON:-python3}"
fi

# Create venv
eval "$PYTHON_BIN -m venv .venv"

# Activate (Git Bash path)
# shellcheck source=/dev/null
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e .

echo "[+] Virtualenv ready."
echo "   To activate later: source .venv/Scripts/activate (Windows Git Bash) or .venv/bin/activate (POSIX)"
echo "[+] Try: mdl --help"
