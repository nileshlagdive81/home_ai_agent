# Real Estate Application Startup Script
# This script starts both backend and frontend servers

Write-Host "Starting Real Estate Application - All Servers" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn" 2>$null
    Write-Host "✅ FastAPI and Uvicorn are available" -ForegroundColor Green
} catch {
    Write-Host "❌ Required packages not found! Installing..." -ForegroundColor Red
    pip install -r requirements.txt
}

# Check and fix NumPy compatibility issue
Write-Host "Checking NumPy compatibility..." -ForegroundColor Yellow
try {
    $numpyVersion = python -c "import numpy; print(numpy.__version__)" 2>$null
    if ($numpyVersion -like "2.*") {
        Write-Host "⚠️  NumPy 2.x detected - downgrading for compatibility..." -ForegroundColor Yellow
        pip install "numpy<2"
        Write-Host "✅ NumPy downgraded for compatibility" -ForegroundColor Green
    } else {
        Write-Host "✅ NumPy version is compatible: $numpyVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error checking NumPy version" -ForegroundColor Red
}

Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to start both servers..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Yellow

# Start backend server in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python main.py" -WindowStyle Normal

Write-Host ""
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow

# Start frontend server in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python -m http.server 3000" -WindowStyle Normal

Write-Host ""
Write-Host "Both servers are starting..." -ForegroundColor Green
Write-Host ""

# Wait a bit for servers to start
Write-Host "Waiting for servers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test if servers are running
$backendRunning = $false
$frontendRunning = $false

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "✅ Backend server is running on http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend server not responding yet..." -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $frontendRunning = $true
        Write-Host "✅ Frontend server is running on http://localhost:3000" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend server not responding yet..." -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to open the application in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browsers
if ($frontendRunning) {
    Start-Process "http://localhost:3000"
    Write-Host "✅ Opened frontend in browser" -ForegroundColor Green
}

if ($backendRunning) {
    Start-Process "http://localhost:8000/docs"
    Write-Host "✅ Opened API docs in browser" -ForegroundColor Green
}

Write-Host ""
Write-Host "Application startup complete!" -ForegroundColor Green
Write-Host "Keep the server windows open while using the application." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit this startup script"
