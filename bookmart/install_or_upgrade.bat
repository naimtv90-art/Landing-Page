@echo off
setlocal enabledelayedexpansion
title Bookmart - Odoo 19 Installer
chcp 65001 >nul
color 0B

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c """"%~f0""""", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /b
)

set "DBNAME=Testdata"
if not "%~1"=="" set "DBNAME=%~1"

set "ODOO_DIR=C:\Program Files\Odoo 19.0.20260902"
if not exist "%ODOO_DIR%" set "ODOO_DIR=C:\Program Files\Odoo 19.0"

set "PYTHON_EXE=%ODOO_DIR%\python\python.exe"
set "ODOO_BIN=%ODOO_DIR%\server\odoo-bin"
set "ODOO_CONF=%ODOO_DIR%\server\odoo.conf"
set "LOCAL_ADDONS=%LOCALAPPDATA%\OpenERP S.A\Odoo\addons\19.0"

echo [*] Stopping Odoo 19 Service...
net stop "odoo-server-19.0" >nul 2>&1

echo [*] Syncing module to addons...
if exist "%LOCAL_ADDONS%" (
    robocopy "%~dp0\" "%LOCAL_ADDONS%\bookmart" /E /XD __pycache__ .git /XF *.pyc *.pyo "index - Copy.html" *.bat >nul
)

echo [*] Upgrading module 'bookmart' on database '%DBNAME%'...
"%PYTHON_EXE%" "%ODOO_BIN%" -c "%ODOO_CONF%" -d "%DBNAME%" -u bookmart --stop-after-init

echo [*] Starting Odoo 19 Service...
net start "odoo-server-19.0" >nul 2>&1

echo [SUCCESS] Bookmart is live at: http://localhost:8069/?db=%DBNAME%
start "" "http://localhost:8069/?db=%DBNAME%"
pause
