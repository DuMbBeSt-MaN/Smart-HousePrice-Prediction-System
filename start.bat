@echo off
echo Starting Housing Prices App...

start "Backend" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\activate && set PYTHONPATH=. && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

start "Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo Both servers started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
