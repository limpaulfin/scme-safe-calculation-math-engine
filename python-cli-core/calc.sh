#!/usr/bin/env bash
# Safe Calculation Math Engine - CLI Wrapper
# ID: 78fab127ce50
# Activates venv and runs main CLI

set -e

# Project paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${SCME_VENV:-$SCRIPT_DIR/../.venv}"
MAIN_SCRIPT="$SCRIPT_DIR/main-78fab127ce50.py"

# Activate venv when present (set SCME_VENV to use another one); otherwise use the python3 on PATH
if [ -d "$VENV" ]; then
    source "$VENV/bin/activate"
fi

# Run main script with all arguments
python3 "$MAIN_SCRIPT" "$@"
