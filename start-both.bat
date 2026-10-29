@echo off
title AI Career Guidance Framework - Launcher
cd /d "%~dp0"
echo ========================================================
echo Starting AI Career Guidance Framework (Backend + Frontend)
echo ========================================================
echo Starting Python FastAPI backend in a new window...
start "AI Career Backend (FastAPI)" cmd /c "run-backend.bat"

timeout /t 3 /nobreak >nul

echo Starting React Frontend in a new window...
start "AI Career Frontend (Vite)" cmd /c "run-frontend.bat"

echo.
echo Both servers have been launched!
echo - Frontend: http://localhost:5173
echo - Backend API: http://127.0.0.1:8000
echo - Swagger Docs: http://127.0.0.1:8000/docs
echo ========================================================
pause
