@echo off
REM Email Automation Dashboard Launcher
REM Quick start script for Windows

echo.
echo ========================================
echo   Email Automation Dashboard
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found!
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created!
    echo.
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo [*] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed!
    echo [*] Installing dependencies...
    pip install -r requirements.txt
    echo [✓] Dependencies installed!
    echo.
)

REM Start the application
echo.
echo ========================================
echo   Starting Flask Application...
echo ========================================
echo.
echo Dashboard will be available at:
echo http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
