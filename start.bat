@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Backend environment not found.
    echo Create it with: py -m venv .venv
    echo Then install dependencies with: .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo Frontend dependencies not found.
    echo Run: cd frontend ^&^& npm install
    pause
    exit /b 1
)

start "Agentic URL Shortener - Backend" cmd /k "cd /d "%~dp0" ^&^& .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
start "Agentic URL Shortener - Frontend" cmd /k "cd /d "%~dp0frontend" ^&^& npm run dev -- --host 127.0.0.1"

echo Backend:  http://127.0.0.1:8000
 echo Frontend: http://127.0.0.1:5173
endlocal
