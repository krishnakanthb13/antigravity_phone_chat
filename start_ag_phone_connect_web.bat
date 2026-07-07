@echo off
setlocal enabledelayedexpansion
title Antigravity Phone Connect - WEB MODE

:: Navigate to script directory
cd /d "%~dp0"

echo ===================================================
echo   Antigravity Phone Connect - WEB ACCESS MODE
echo ===================================================
echo.

:: 0. Aggressive Cleanup (Clear any stuck processes from previous runs)
echo [0/2] Cleaning up orphans...
taskkill /f /im node.exe /fi "WINDOWTITLE eq AG_SERVER_PROC*" >nul 2>&1
taskkill /f /im ngrok.exe >nul 2>&1
taskkill /f /im cloudflared.exe >nul 2>&1
taskkill /f /im pinggy.exe >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

:: 1. Ensure dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    call npm install
)

:: 2. Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js missing.
    pause
    exit /b
)

:: 3. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python missing. Required for the web tunnel.
    pause
    exit /b
)

:: 4. Check for .env file
if exist ".env" goto ENV_FOUND
if exist "%~dp0.env" goto ENV_FOUND

echo [WARNING] .env file not found. This is required for Web Access.
echo.

if exist ".env.example" (
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env >nul
    echo [SUCCESS] .env created from template!
    echo [ACTION] Please open .env and update it with your configuration (e.g., NGROK_AUTHTOKEN).
    pause
    exit /b
) else (
    echo [ERROR] .env.example not found. Cannot create .env template.
    pause
    exit /b
)

:ENV_FOUND
echo [INFO] .env configuration found.

:: 5. Launch everything via Python
echo [1/1] Launching Antigravity Phone Connect...
echo (This will start both the server and the web tunnel)

if not exist "venv\" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

chcp 65001 >nul
set PYTHONUTF8=1

python launcher.py --mode web
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Launcher failed with exit code %errorlevel%.
    echo Check for any error messages above.
    pause
    exit /b %errorlevel%
)

:: 6. Successful exit
exit /b 0
