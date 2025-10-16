@echo off
REM --- ONE-TIME SETUP ---
REM 1. Follow the instructions in the main README to install StyleTTS 2.
REM 2. Find the 'StyleTTS2-Sillytavern-api' folder you created.
REM 3. Right-click that folder and select "Copy as path".
REM 4. Replace the placeholder path in the line below with the path you copied.
REM    - Example: set STYLETTS_DIR="C:\AI\StyleTTS2-Sillytavern-api"

echo Starting StyleTTS 2 API Server...

REM --- EDIT THE PATH BELOW ---
set STYLETTS_DIR="C:\path\to\your\StyleTTS2-Sillytavern-api"
REM --- END OF SETUP ---

if not exist "%STYLETTS_DIR%" (
    echo.
    echo ERROR: StyleTTS 2 directory not found at the path specified in this script.
    echo Please edit start_styletts.bat to set the correct path.
    pause
    exit /b
)

cd /d "%STYLETTS_DIR%"

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Launching StyleTTS 2 API...
python api.py

echo.
echo StyleTTS 2 API has started.
timeout /t 3 >nul