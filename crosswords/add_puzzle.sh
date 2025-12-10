#!/bin/bash
# Wrapper script to add puzzles with automatic virtual environment activation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/converter/venv/bin/activate"

# Activate virtual environment if it exists
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
fi

# Run the Python script with all arguments
python3 "$SCRIPT_DIR/add_puzzle.py" "$@"



