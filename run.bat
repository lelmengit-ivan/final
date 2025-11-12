@echo off
echo ========================================
echo   Pharmacy Management System
echo   AI-Powered Inventory & Sales
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Checking if database exists...
if not exist pharmacy.db (
    echo Database not found. Creating sample data...
    python seed_data.py
    echo.
)

echo Starting the application...
echo.
echo ========================================
echo   Server will start on:
echo   http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
