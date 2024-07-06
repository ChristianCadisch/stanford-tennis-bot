#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$0")

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source .env/bin/activate

# Run the Python script
python3 reserve.py