@echo off
setlocal enabledelayedexpansion
title Bookmart - Odoo 19 Automatic Theme Installer
chcp 65001 >nul
color 0B

:: =======================================================================
:: Request Administrator Elevation
:: =======================================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo =======================================================================
    echo   [!] Administrator Privileges Required
    echo   Please click "YES" on the Windows UAC prompt window...
    echo =======================================================================
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c """"%~f0""""", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /b
)

cd /d "%~dp0"

echo =======================================================================
echo          METAMORPHOSIS - BOOKMART THEME FOR ODOO 19
echo                 AUTOMATIC INSTALLER & SYNC
echo =======================================================================
echo.

:: 1. Database Configuration
set "DBNAME=Testdata"
if not "%~1"=="" set "DBNAME=%~1"
echo [*] Target Odoo Database: [%DBNAME%]

:: 2. Detect Odoo 19 Paths
set "ODOO_DIR=C:\Program Files\Odoo 19.0.20260902"
if not exist "%ODOO_DIR%" set "ODOO_DIR=C:\Program Files\Odoo 19.0"

set "PYTHON_EXE=%ODOO_DIR%\python\python.exe"
set "ODOO_BIN=%ODOO_DIR%\server\odoo-bin"
set "ODOO_CONF=%ODOO_DIR%\server\odoo.conf"
set "SERVER_ADDONS=%ODOO_DIR%\server\odoo\addons"
set "LOCAL_ADDONS=%LOCALAPPDATA%\OpenERP S.A\Odoo\addons\19.0"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at: %PYTHON_EXE%
    echo Please verify your Odoo 19 installation directory.
    pause
    exit /b 1
)

:: 3. Source directory
set "SRC_MODULE=%~dp0bookmart"
if not exist "%SRC_MODULE%\__manifest__.py" (
    echo [ERROR] Module folder 'bookmart' not found in %~dp0
    pause
    exit /b 1
)

echo.
echo [*] Stopping Odoo 19 Windows Service...
net stop "odoo-server-19.0" >nul 2>&1

echo.
echo [*] Syncing 'bookmart' module to Odoo Addons...
if exist "%LOCAL_ADDONS%" (
    echo   - Copying to Local Addons: %LOCAL_ADDONS%\bookmart
    robocopy "%SRC_MODULE%" "%LOCAL_ADDONS%\bookmart" /E /XD __pycache__ .git /XF *.pyc *.pyo "index - Copy.html" *.bat >nul
)

if exist "%SERVER_ADDONS%" (
    echo   - Copying to Server Addons: %SERVER_ADDONS%\bookmart
    robocopy "%SRC_MODULE%" "%SERVER_ADDONS%\bookmart" /E /XD __pycache__ .git /XF *.pyc *.pyo "index - Copy.html" *.bat >nul
)

echo.
echo [*] Installing / Upgrading 'bookmart' in database '%DBNAME%'...
echo -----------------------------------------------------------------------
"%PYTHON_EXE%" "%ODOO_BIN%" -c "%ODOO_CONF%" -d "%DBNAME%" -u bookmart --stop-after-init
echo -----------------------------------------------------------------------

echo.
echo [*] Restarting Odoo 19 Windows Service...
net start "odoo-server-19.0" >nul 2>&1

echo.
echo =======================================================================
echo   [SUCCESS] Bookmart Theme has been installed and synced successfully!
echo   Opening: http://localhost:8069/?db=%DBNAME%
echo =======================================================================
echo.

start "" "http://localhost:8069/?db=%DBNAME%"
pause

