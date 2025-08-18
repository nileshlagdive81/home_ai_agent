@echo off
echo Starting Real Estate Application - All Servers
echo =============================================
echo.
echo This will start both backend and frontend servers
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to start both servers...
pause >nul

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0backend" && python main.py"

echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "python -m http.server 3000"

echo.
echo Both servers are starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:3000
start http://localhost:8000/docs

echo.
echo Application started successfully!
echo Close this window when you're done.
pause
