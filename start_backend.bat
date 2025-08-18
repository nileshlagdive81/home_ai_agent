@echo off
echo Starting Real Estate Backend Server...
echo.
cd /d "%~dp0backend"
echo Current directory: %CD%
echo.
echo Starting FastAPI server on port 8000...
python main.py
pause
