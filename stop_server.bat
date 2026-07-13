@echo off
title Stop Mathematics Mastery Roadmap Server
echo ========================================================
echo  Stopping Mathematics Mastery Roadmap Server...
echo ========================================================
echo.

set "found="
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8090 ^| findstr LISTENING') do (
    echo Found process %%a running on port 8090.
    echo Terminating server process...
    taskkill /f /pid %%a
    set "found=1"
)

if not defined found (
    echo No server instance found running on port 8090.
) else (
    echo Server stopped successfully.
)

echo.
echo ========================================================
pause
