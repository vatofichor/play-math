@echo off
title play-math Server Launcher
echo ========================================================
echo  Starting play-math Server...
echo ========================================================
echo.

set "PY_CMD="

:: 1. Check system Python and verify version is 3+
where python >nul 2>nul
if %errorlevel% equ 0 (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 0) else 1)" >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=python"
    )
)

:: 2. If system Python is missing or too old, check for local portable Python
if not defined PY_CMD (
    if exist "%~dp0assets\lib\python\python.exe" (
        set "PY_CMD=%~dp0assets\lib\python\python.exe"
    )
)

:: 3. If still not found, show error and guide
if not defined PY_CMD (
    echo [ERROR] Python is not installed on this computer!
    echo.
    echo To run this math playground, you need to install Python:
    echo 1. Go to the official Python website:
    echo    https://www.python.org/downloads/
    echo 2. Download and run the installer for Windows.
    echo 3. IMPORTANT: Check the box that says "Add Python.exe to PATH" 
    echo    at the bottom of the installer window before clicking Install.
    echo 4. Once finished, double-click "run_server.bat" again.
    echo.
    echo ========================================================
    pause
    exit /b 1
)

echo Using Python from: %PY_CMD%
%PY_CMD% "%~dp0app.py"
if %errorlevel% neq 0 (
    echo.
    echo Server stopped with error code %errorlevel%
    pause
)
