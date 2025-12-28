@echo off
echo ========================================
echo  Government Finance Portal Launcher
echo ========================================
echo.

echo [1/2] Starting Backend Server (Port 8000)...
start "Backend Server" cmd /k "cd /d c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\gok_backend && C:\Users\nyaga\OneDrive\Desktop\NASA\.venv\Scripts\python.exe main.py"

echo [2/2] Starting Frontend Server (Port 5500)...
timeout /t 3 /nobreak > nul
start "Frontend Server" cmd /k "cd /d c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\NASA && python -m http.server 5500"

echo.
echo ========================================
echo  SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5500/login.html
echo.
echo Opening browser...
timeout /t 3 /nobreak > nul
start http://localhost:5500/login.html

echo.
echo Press any key to exit this window...
echo (Keep the server windows open!)
pause > nul
