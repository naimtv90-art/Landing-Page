@echo off
title Restart Odoo 19 Service
color 0A

:: Check for administrative permissions
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ====================================================
    echo   Requesting Administrator Privileges...
    echo   Please click "YES" on the popup window!
    echo ====================================================
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c """"%~f0""""", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /b
)

:: If we reach here, we have full Administrator privileges!
echo ====================================================
echo             RESTARTING ODOO 19 SERVICE
echo ====================================================
echo.

echo [*] Stopping Odoo service (odoo-server-19.0)...
net stop "odoo-server-19.0"
echo.

echo [*] Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo [*] Starting Odoo service (odoo-server-19.0)...
net start "odoo-server-19.0"
echo.

echo ====================================================
echo     ODOO 19 SERVICE RESTARTED SUCCESSFULLY!
echo ====================================================
echo.
echo Now open your browser and press Ctrl + F5!
echo.
pause
