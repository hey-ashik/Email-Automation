# Email Automation Dashboard Launcher (PowerShell)
# Quick start script for Windows PowerShell

Write-Host "`n========================================"
Write-Host "  Email Automation Dashboard"
Write-Host "========================================`n"

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "[!] Virtual environment not found!" -ForegroundColor Yellow
    Write-Host "[*] Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "[✓] Virtual environment created!`n" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "[*] Checking dependencies..." -ForegroundColor Cyan
$flaskInstalled = pip show flask 2>$null
if (-Not $flaskInstalled) {
    Write-Host "[!] Dependencies not installed!" -ForegroundColor Yellow
    Write-Host "[*] Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    Write-Host "[✓] Dependencies installed!`n" -ForegroundColor Green
}

# Start the application
Write-Host "`n========================================"
Write-Host "  Starting Flask Application..."
Write-Host "========================================`n"
Write-Host "Dashboard will be available at:" -ForegroundColor Cyan
Write-Host "http://127.0.0.1:5000`n" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server"
Write-Host "========================================`n"

python app.py
