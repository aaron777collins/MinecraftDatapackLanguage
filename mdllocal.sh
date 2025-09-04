#!/bin/bash
# Local MDL compiler shim - runs the local version instead of installed version

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the local MDL compiler
python -m minecraft_datapack_language.cli "$@"
