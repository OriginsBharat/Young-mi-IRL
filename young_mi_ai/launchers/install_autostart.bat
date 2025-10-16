@echo off
:: This script must be run as an administrator to work.

echo ==========================================================
echo  Kim Young-mi AI - Invisible Autostart Installer
echo ==========================================================
echo.
echo This script will create a new task in Windows Task Scheduler.
echo The task will automatically run the 'start_everything.bat'
echo script silently in the background whenever you log in.
echo.

:: Get the absolute path of the start_everything.bat script
set "LAUNCHER_PATH=%~dp0start_everything.bat"

echo Creating task to run the following script on logon:
echo %LAUNCHER_PATH%
echo.

:: Create the scheduled task
:: /tn: Task Name
:: /tr: Task Run (the command to execute)
:: /sc: Schedule Type (on logon)
:: /rl: Run Level (highest privileges)
:: /f: Force creation (overwrite if exists)
schtasks /create /tn "YoungMiAI" /tr "%LAUNCHER_PATH%" /sc ONLOGON /rl HIGHEST /f

:: Check if the task was created successfully
if %errorlevel% == 0 (
    echo.
    echo SUCCESS!
    echo The 'YoungMiAI' task has been created. She will now
    echo start automatically and invisibly with your computer.
) else (
    echo.
    echo ERROR!
    echo Failed to create the scheduled task.
    echo Please make sure you ran this script as an administrator.
)

echo.
pause