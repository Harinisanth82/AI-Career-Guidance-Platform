@echo off
title AI Career Guidance - Python FastAPI Backend
cd /d "%~dp0"
echo ========================================================
echo Starting AI Career Guidance Framework - Python Backend
echo URL: http://127.0.0.1:8000
echo Docs: http://127.0.0.1:8000/docs
echo ========================================================
.\backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause
