@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed or not on PATH.
  pause
  exit /b 1
)
REM Port 8000 is used by INBODY - use 8077 instead
if "%INBODY_PORT%"=="" set INBODY_PORT=8078
start "INBODY" /min python "%~dp0server.py"
echo INBODY: http://localhost:%INBODY_PORT%/inbody-manger.html
echo Stop: close the minimized INBODY window.
endlocal
