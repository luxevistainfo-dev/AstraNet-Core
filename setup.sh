#!/bin/bash

echo "=== AstraNet Core Setup ==="

# Креирај virtual environment
echo "1. Creating virtual environment..."
python3 -m venv venv 2>/dev/null || {
    echo "Installing python3-venv..."
    sudo apt install python3-venv -y
    python3 -m venv venv
}

# Активирај
echo "2. Activating virtual environment..."
source venv/bin/activate

# Инсталирај Flask
echo "3. Installing Flask..."
pip install flask==2.3.3

# Провери
echo "4. Verifying installation..."
python3 -c "import flask; print('✅ Flask installed successfully')"

echo "=== Setup complete ==="
echo "To activate: source venv/bin/activate"
echo "To run CLI: python3 node.py"
echo "To run API: python3 api.py"
