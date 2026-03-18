@echo off
:loop
REM Change to the TEMP directory
cd %TEMP%

REM Launch truc.py with Python
python truc.py

REM Wait for 60 seconds before restarting
timeout /t 60 > nul

REM Go back to the start of the script
goto loop