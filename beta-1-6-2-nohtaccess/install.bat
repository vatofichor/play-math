@echo off
title play-math Environment Setup and Installer
echo ========================================================
echo  Checking Environment Dependencies for play-math...
echo ========================================================
echo.

set "PHP_SYS_OK="

:: 1. Check system PHP on PATH and verify version >= 5.3
where php >nul 2>nul
if %errorlevel% equ 0 (
    php -r "if(version_compare(PHP_VERSION,'5.3.0','<')) exit(1);" >nul 2>nul
    if not errorlevel 1 (
        set "PHP_SYS_OK=1"
        echo [OK] System PHP is installed and version requirement PHP 5.3+ is met.
    ) else (
        echo [INFO] System PHP found, but version is lower than 5.3.
    )
) else (
    echo [INFO] System PHP is not found on PATH.
)

:: 2. If system PHP is missing or outdated, unpack local portable PHP if needed
if not defined PHP_SYS_OK (
    if exist "%~dp0assets\lib\php\php\php.exe" (
        echo [OK] Local portable PHP environment is already installed in assets\lib\php\php\
    ) else (
        if exist "%~dp0assets\lib\php\php.zip" (
            echo.
            echo [INSTALLING] Unpacking local portable PHP runtime...
            powershell -NoProfile -Command "Expand-Archive -Path '%~dp0assets\lib\php\php.zip' -DestinationPath '%~dp0assets\lib\php\php' -Force"
            if exist "%~dp0assets\lib\php\php\php.exe" (
                echo [OK] Local portable PHP runtime successfully installed to assets\lib\php\php\
            ) else (
                echo [ERROR] Failed to unpack portable PHP archive.
                pause
                exit /b 1
            )
        ) else (
            echo [ERROR] Portable PHP archive assets\lib\php\php.zip was not found!
            pause
            exit /b 1
        )
    )
)

:: 3. Copy ONLY Windows launcher script and uninstaller from assets\lib\installer\ into root
echo.
echo [INSTALLING] Deploying Windows launcher script and uninstaller...
if exist "%~dp0assets\lib\installer\run_server.bat" copy /y "%~dp0assets\lib\installer\run_server.bat" "%~dp0run_server.bat" >nul
if exist "%~dp0assets\lib\installer\uninstall.bat" copy /y "%~dp0assets\lib\installer\uninstall.bat" "%~dp0uninstall.bat" >nul

echo [OK] Windows server launcher (run_server.bat) and uninstaller deployed to project root.

echo.
echo ========================================================
echo  Environment setup complete! Run run_server.bat to start.
echo ========================================================
