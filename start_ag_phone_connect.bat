@echo off
setlocal enabledelayedexpansion
title Antigravity Phone Connect

:: Navigate to the script's directory
cd /d "%~dp0"

echo ===================================================
echo   Antigravity Phone Connect Launcher
echo ===================================================
echo.

:: Check for Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed.
    echo Please install it from https://nodejs.org/
    pause
    exit /b
)

:: Install deps if missing
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed.
        pause
        exit /b
    )
)

:: Get Local IP
set "MYIP="
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address" /c:"IP Address"') do (
    set "tmpip=%%a"
    set "tmpip=!tmpip: =!"
    if not "!tmpip!"=="" set "MYIP=!tmpip!"
)

:: Check for SSL certificates
set "PROTOCOL=http"
if exist "certs\server.key" if exist "certs\server.cert" (
    set "PROTOCOL=https"
    echo [SSL] HTTPS enabled - secure connection available
)

echo.
echo [READY] Server will be available at:
echo       !PROTOCOL!://!MYIP!:3000
echo.
echo [TIP] To add Right-Click context menu, run: install_context_menu.bat
if "!PROTOCOL!"=="http" (
    echo [TIP] To enable HTTPS, run: node generate_ssl.js
)
echo [SECURITY] Default Password: antigravity
echo            (Change it by setting the APP_PASSWORD env variable)
echo.

echo [STARTING] Launching monitor server...
echo.
node server.js

:: Keep window open if server crashes
echo.
echo [INFO] Server stopped. Press any key to exit.
pause >nul

