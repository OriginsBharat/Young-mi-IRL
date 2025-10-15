@echo off
title Kim Young-mi AI Launcher

echo =================================
echo  Starting All Services...
echo =================================
echo.

REM This script will start all necessary components for the Kim Young-mi AI.
REM Make sure you have configured the individual .bat files in this folder first.

echo [1/4] Starting Ollama...
start "Ollama" cmd /c start_ollama.bat
timeout /t 5 >nul

echo [2/4] Starting ComfyUI...
start "ComfyUI" cmd /c start_comfyui.bat
timeout /t 10 >nul

echo [3/4] Starting XTTS Server...
start "XTTS" cmd /c start_xtts.bat
timeout /t 10 >nul

echo [4/4] Starting Kim Young-mi Bot...
echo.
REM This assumes your python executable is in your PATH.
REM If not, you may need to provide the full path to python.exe
cd ..
python src/main.py

echo.
echo =================================
echo  All services are running.
echo =================================
pause