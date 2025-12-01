#!/bin/bash
# Setup script for Python virtual environment

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements (if any)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment created and activated!"
echo "To activate manually, run: source venv/bin/activate"
echo "To deactivate, run: deactivate"

