@echo off
REM --- ONE-TIME SETUP ---
REM 1. Navigate to your ComfyUI installation folder.
REM 2. Find the `run_nvidia_gpu.bat` (or your preferred run file).
REM 3. Right-click it and select "Copy as path".
REM 4. Replace the line below with the full path you copied.
REM    - Example: "C:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat" --windows-standalone-build

echo Starting ComfyUI...
REM --- PASTE YOUR COMFYUI PATH BELOW ---
call C:\path\to\your\ComfyUI\run_nvidia_gpu.bat
REM --- END OF SETUP ---

echo.
echo ComfyUI is starting in a new window.
timeout /t 3 >nul