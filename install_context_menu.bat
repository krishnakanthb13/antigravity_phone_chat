@echo off
title Antigravity - Context Menu Manager

:menu
cls
echo ===================================================
echo   Antigravity - Right-Click Context Menu Manager
echo ===================================================
echo.
echo This tool manages the "Open with Antigravity (Debug)" option
echo in your Windows Right-Click context menu.
echo.
echo WHAT IT DOES:
echo   - Adds/Removes a new option when you right-click a folder
echo   - Clicking it will run: agy . --remote-debugging-port=9000
echo   - This launches Antigravity with debugging enabled for Phone Connect
echo.
echo REQUIREMENTS:
echo   - Antigravity CLI must be installed and in your PATH
echo   - Administrator access (UAC prompt will appear)
echo.
echo ===================================================
echo.
echo Choose an option:
echo   [1] Install   - Add Right-Click menu
echo   [2] Remove    - Remove Right-Click menu
echo   [3] Restart   - Restart Windows Explorer (to apply changes)
echo   [4] Backup    - Export current registry keys before changes
echo   [5] Exit
echo.

set /p "choice=Enter choice (1-5): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto remove
if "%choice%"=="3" goto restart
if "%choice%"=="4" goto backup
if "%choice%"=="5" goto end
echo [ERROR] Invalid choice.
pause
goto menu

:backup
echo.
echo [BACKUP] Exporting registry keys...
:: Use PowerShell for locale-independent timestamp (works on all Windows locales)
for /f %%a in ('powershell -command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set "TIMESTAMP=%%a"

:: Create registry folder if it doesn't exist
if not exist "%~dp0registry" mkdir "%~dp0registry"

set "BACKUP_FILE=%~dp0registry\context_menu_backup_%TIMESTAMP%.reg"
reg export "HKEY_CLASSES_ROOT\Directory\Background\shell\AntigravityDebug" "%BACKUP_FILE%" /y 2>nul
reg export "HKEY_CLASSES_ROOT\Directory\shell\AntigravityDebug" "%BACKUP_FILE%" /y 2>nul
if exist "%BACKUP_FILE%" (
    echo [SUCCESS] Backup saved to: %BACKUP_FILE%
) else (
    echo [INFO] No existing Antigravity context menu found to backup.
)
echo.
pause
goto menu

:install
echo.
echo [INSTALL] Adding registry entries...

:: Add to folder background (right-click empty space in folder)
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\Background\shell\AntigravityDebug\" /ve /d \"Open with Antigravity (Debug)\" /f' -Verb RunAs -Wait" 2>nul
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\Background\shell\AntigravityDebug\" /v Icon /d \"%~dp0assets\antigravity.ico\" /f' -Verb RunAs -Wait" 2>nul
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\Background\shell\AntigravityDebug\command\" /ve /d \"cmd /c cd /d \\\"%%V\\\" ^&^& agy . --remote-debugging-port=9000\" /f' -Verb RunAs -Wait" 2>nul

:: Add to folder itself (right-click on a folder)
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\shell\AntigravityDebug\" /ve /d \"Open with Antigravity (Debug)\" /f' -Verb RunAs -Wait" 2>nul
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\shell\AntigravityDebug\" /v Icon /d \"%~dp0assets\antigravity.ico\" /f' -Verb RunAs -Wait" 2>nul
powershell -Command "Start-Process reg -ArgumentList 'add \"HKEY_CLASSES_ROOT\Directory\shell\AntigravityDebug\command\" /ve /d \"cmd /c cd /d \\\"%%1\\\" ^&^& agy . --remote-debugging-port=9000\" /f' -Verb RunAs -Wait" 2>nul

echo.
echo [SUCCESS] Context menu installed!
echo.
pause
goto menu

:restart
echo.
echo [RESTART] Restarting Windows Explorer...
taskkill /f /im explorer.exe >nul 2>nul
start explorer.exe
echo [SUCCESS] Explorer restarted.
echo.
pause
goto menu

:remove
echo.
echo [REMOVE] Deleting registry entries...

powershell -Command "Start-Process reg -ArgumentList 'delete \"HKEY_CLASSES_ROOT\Directory\Background\shell\AntigravityDebug\" /f' -Verb RunAs -Wait" 2>nul
powershell -Command "Start-Process reg -ArgumentList 'delete \"HKEY_CLASSES_ROOT\Directory\shell\AntigravityDebug\" /f' -Verb RunAs -Wait" 2>nul

echo.
echo [SUCCESS] Context menu removed!
echo.
pause
goto menu

:end
echo [EXIT] No changes made.
exit /b
