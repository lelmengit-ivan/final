#!/bin/bash

echo "========================================"
echo "  Pharmacy Management System"
echo "  AI-Powered Inventory & Sales"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
python3 --version
echo ""

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "Checking if database exists..."
if [ ! -f pharmacy.db ]; then
    echo "Database not found. Creating sample data..."
    python3 seed_data.py
    echo ""
fi

echo "Starting the application..."
echo ""
echo "========================================"
echo "  Server will start on:"
echo "  http://localhost:5000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
