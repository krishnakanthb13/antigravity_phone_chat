@echo off
setlocal enabledelayedexpansion
title Antigravity Phone Connect

:: Navigate to the script's directory
cd /d "%~dp0"

:: Check for .env file
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] .env file not found. Creating from .env.example...
        copy .env.example .env >nul
        echo [SUCCESS] .env created from template!
        echo [ACTION] Please update .env if you wish to change defaults.
        echo.
    )
)

echo ===================================================
echo   Antigravity Phone Connect Launcher
echo ===================================================
echo.

echo [STARTING] Launching via Unified Launcher...
chcp 65001 >nul
set PYTHONUTF8=1

if not exist "venv\" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

python launcher.py --mode local

:: Keep window open if server crashes
echo.
echo [INFO] Server stopped. Press any key to exit.
pause >nul

