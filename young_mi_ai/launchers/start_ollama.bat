@echo off
REM --- ONE-TIME SETUP ---
REM 1. Find your ollama.exe file.
REM 2. Right-click it and select "Copy as path".
REM 3. Replace the line below with "start 'Ollama' /d [path] ollama.exe serve"
REM    - Replace [path] with the directory of your ollama.exe.
REM    - Example: start "Ollama" /d "C:\Users\YourName\AppData\Local\Programs\Ollama" ollama.exe serve

echo Starting Ollama...
REM --- PASTE YOUR OLLAMA PATH BELOW ---
start "Ollama" ollama serve
REM --- END OF SETUP ---

echo.
echo Ollama is starting in a new window.
timeout /t 3 >nul