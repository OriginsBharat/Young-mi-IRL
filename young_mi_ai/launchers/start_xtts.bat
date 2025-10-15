@echo off
REM --- ONE-TIME SETUP ---
REM 1. Navigate to your XTTS web UI folder (e.g., xtts-webui).
REM 2. Find the startup script (e.g., `start.bat`, `run.bat`).
REM 3. Right-click it and select "Copy as path".
REM 4. Replace the line below with the full path you copied.
REM    - Example: "C:\AI\xtts-webui\start.bat"

echo Starting XTTSv2 Server...
REM --- PASTE YOUR XTTS PATH BELOW ---
call C:\path\to\your\xtts-webui\start.bat
REM --- END OF SETUP ---

echo.
echo XTTS is starting in a new window.
timeout /t 3 >nul