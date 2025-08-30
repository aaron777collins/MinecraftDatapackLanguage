#!/usr/bin/env bash
set -euo pipefail

# Syncs production MDL package non-code assets into the local source tree
# so local editable installs (mdlbeta) have parity with production goodies.
#
# Usage:
#   scripts/sync_prod_assets.sh           # sync from latest release
#   MDL_PROD_VERSION==1.2.3 scripts/sync_prod_assets.sh  # pin version

echo "[sync] Synchronizing production MDL assets into local source..."

if [ ! -d "minecraft_datapack_language" ]; then
  echo "[sync] Error: run from project root (minecraft_datapack_language/ not found)" >&2
  exit 1
fi

PROD_VERSION_SUFFIX=""
if [ "${MDL_PROD_VERSION:-}" != "" ]; then
  PROD_VERSION_SUFFIX="==${MDL_PROD_VERSION}"
fi

WORKDIR=".tmp/_mdl_prod_sync"
TARGET_SITEPKG="${WORKDIR}/sitepkgs"

rm -rf "${WORKDIR}"
mkdir -p "${TARGET_SITEPKG}"

# Choose a Python interpreter
if command -v python3 >/dev/null 2>&1; then
  PYBIN=python3
elif command -v python >/dev/null 2>&1; then
  PYBIN=python
else
  echo "[sync] Error: python3/python not found in PATH" >&2
  exit 1
fi

# Try safest approach first: download wheel without installing
UNPACK_DIR="${WORKDIR}/unpacked"
mkdir -p "${UNPACK_DIR}"
if $PYBIN -m pip download "minecraft-datapack-language${PROD_VERSION_SUFFIX}" -d "${WORKDIR}" >/dev/null 2>&1; then
  WHEEL_FILE=$(ls -1 "${WORKDIR}"/minecraft_datapack_language-*.whl 2>/dev/null | head -1 || true)
  if [ -n "${WHEEL_FILE}" ]; then
    python3 - <<PY
import zipfile, sys
zf = zipfile.ZipFile("${WHEEL_FILE}")
zf.extractall("${UNPACK_DIR}")
zf.close()
PY
    # Find package directory inside unpacked wheel
    CANDIDATE_DIR=$(ls -d "${UNPACK_DIR}"/minecraft_datapack_language*/ 2>/dev/null | head -1 || true)
    if [ -n "${CANDIDATE_DIR}" ]; then
      INSTALLED_PKG_DIR="${CANDIDATE_DIR%/}"
    fi
  fi
fi

# Fallback: install package into a temp target directory (no system install)
if [ -z "${INSTALLED_PKG_DIR:-}" ]; then
  $PYBIN -m pip install "minecraft-datapack-language${PROD_VERSION_SUFFIX}" --target "${TARGET_SITEPKG}" --break-system-packages >/dev/null 2>&1 || true
  if [ -d "${TARGET_SITEPKG}/minecraft_datapack_language" ]; then
    INSTALLED_PKG_DIR="${TARGET_SITEPKG}/minecraft_datapack_language"
  else
    INSTALLED_PKG_DIR=""
  fi
fi

if [ -z "${INSTALLED_PKG_DIR}" ] || [ ! -d "${INSTALLED_PKG_DIR}" ]; then
  echo "[sync] Error: Could not locate installed production package directory" >&2
  exit 1
fi

echo "[sync] Found production package at: ${INSTALLED_PKG_DIR}"

SRC_DIR="minecraft_datapack_language"

# Candidate non-code asset directories to copy if present upstream
ASSET_DIRS=(
  "assets"
  "resources"
  "templates"
  "completions"
  "data"
  "static"
)

COPIED_ANY=0
for d in "${ASSET_DIRS[@]}"; do
  if [ -d "${INSTALLED_PKG_DIR}/${d}" ]; then
    echo "[sync] Copying ${d}/ from production..."
    mkdir -p "${SRC_DIR}/${d}"
    rsync -a --delete \
      --exclude='*.py' --exclude='*.pyc' --exclude='__pycache__/' \
      "${INSTALLED_PKG_DIR}/${d}/" "${SRC_DIR}/${d}/"
    COPIED_ANY=1
  fi
done

if [ ${COPIED_ANY} -eq 0 ]; then
  echo "[sync] No asset directories found in production package (nothing to sync)."
else
  echo "[sync] Asset synchronization complete."
fi

if [ "${MDL_KEEP_TMP:-}" = "1" ]; then
  echo "[sync] Temporary files kept at ${WORKDIR} (MDL_KEEP_TMP=1)."
else
  echo "[sync] Cleaning up ${WORKDIR}..."
  rm -rf "${WORKDIR}"
fi
echo "[sync] Done."

