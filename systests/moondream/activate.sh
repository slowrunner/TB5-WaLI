#!/bin/bash 
# Set the path to your virtual environment directory
VENV_PATH="./moondream_venv" 


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "!!! Must use:  . activate.sh"
    exit 0
fi

if [ -d "$VENV_PATH" ] && [ -f "$VENV_PATH/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
else
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi
