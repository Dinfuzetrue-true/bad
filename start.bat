@echo off
:loop
REM Change to the TEMP directory
cd %TEMP%

REM Launch truc.py using PowerShell and Start-Process
powershell -WindowStyle Hidden -Command "Start-Process -FilePath 'python' -ArgumentList 'truc.py' -NoNewWindow"

REM Wait for 60 seconds before restarting
timeout /t 60 > nul

REM Go back to the start of the script
goto loop
