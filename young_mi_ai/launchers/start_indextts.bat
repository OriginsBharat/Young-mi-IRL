@echo off
REM --- ONE-TIME SETUP ---
REM 1. Follow the instructions in the main README to install IndexTTS One-Click.
REM 2. Find the 'index-tts-OneClick' folder you created.
REM 3. Right-click that folder and select "Copy as path".
REM 4. Replace the placeholder path in the line below with the path you copied.
REM    - Example: set INDEXTTS_DIR="C:\AI\index-tts-OneClick"

echo Starting IndexTTS API Server...

REM --- EDIT THE PATH BELOW ---
set INDEXTTS_DIR="C:\path\to\your\index-tts-OneClick"
REM --- END OF SETUP ---

if not exist "%INDEXTTS_DIR%" (
    echo.
    echo ERROR: IndexTTS directory not found at the path specified in this script.
    echo Please edit start_indextts.bat to set the correct path.
    pause
    exit /b
)

cd /d "%INDEXTTS_DIR%"

echo Launching IndexTTS API...
call run-http.bat

echo.
echo IndexTTS API has started.
timeout /t 3 >nul