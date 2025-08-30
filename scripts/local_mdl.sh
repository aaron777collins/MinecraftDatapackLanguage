#!/usr/bin/env bash
set -euo pipefail

# One-shot helper to build local mdl (mdlbeta) mirroring production goodies
# - Syncs prod assets into source
# - Installs editable package as mdlbeta
# - Optional: runs quick smoke tests
#
# Usage:
#   scripts/local_mdl.sh           # sync + install
#   scripts/local_mdl.sh --test    # also run quick tests

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

if [ ! -f "pyproject.toml" ]; then
  echo "[local] Error: run from project root" >&2
  exit 1
fi

echo "[local] Syncing production assets..."
bash scripts/sync_prod_assets.sh

echo "[local] Installing editable package as mdlbeta..."
# Choose a Python interpreter
if command -v python3 >/dev/null 2>&1; then
  PYBIN=python3
elif command -v python >/dev/null 2>&1; then
  PYBIN=python
else
  echo "[local] Error: python3/python not found in PATH" >&2
  exit 1
fi

$PYBIN -m pip install --upgrade pip >/dev/null || true
# Prefer user install to avoid system package manager conflicts
$PYBIN -m pip install --user -e . --force-reinstall >/dev/null

# Ensure the user-base bin directory is on PATH for this session
USER_BASE=$($PYBIN -m site --user-base)
USER_BIN="${USER_BASE}/bin"
export PATH="${USER_BIN}:$PATH"

echo "[local] Using PATH: $PATH"
echo "[local] mdlbeta version:" && mdlbeta --version || echo "[local] Hint: add ${USER_BIN} to your PATH"

if [ "${1:-}" = "--test" ]; then
  echo "[local] Running development smoke tests..."
  bash scripts/test_dev.sh
fi

echo "[local] Done. Try: mdlbeta --help"

