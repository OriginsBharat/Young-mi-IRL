@echo off
:: This script must be run as an administrator to work.

echo ==========================================================
echo  Kim Young-mi AI - Invisible Autostart Uninstaller
echo ==========================================================
echo.
echo This script will remove the 'YoungMiAI' task from the
echo Windows Task Scheduler, stopping her from starting
echo automatically with your computer.
echo.
echo Are you sure you want to continue?
choice /c yn /m "Press Y for Yes, N for No."

if %errorlevel% == 2 (
    echo.
    echo Operation cancelled.
    goto end
)

echo.
echo Deleting the 'YoungMiAI' scheduled task...

:: Delete the scheduled task
:: /tn: Task Name
:: /f: Force deletion without confirmation
schtasks /delete /tn "YoungMiAI" /f

:: Check if the task was deleted successfully
if %errorlevel% == 0 (
    echo.
    echo SUCCESS!
    echo The 'YoungMiAI' task has been removed.
) else (
    echo.
    echo INFO:
    echo The task was likely already removed or never existed.
)

:end
echo.
pause