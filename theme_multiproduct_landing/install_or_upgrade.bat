@echo off
setlocal enabledelayedexpansion
title Single Page Multi-Product Landing - Odoo 19 Installer
chcp 65001 >nul
color 0A

echo =======================================================================
echo     ODOO 19 SINGLE PAGE MULTI-PRODUCT LANDING THEME & STORE
echo                 INSTALLER & UPGRADE SCRIPT
echo =======================================================================
echo.

set "DBNAME=Testdata"
echo Target Odoo Database: %DBNAME%
echo.

echo Upgrading module 'theme_multiproduct_landing'...
"C:\Program Files\Odoo 19.0.20260902\python\python.exe" "C:\Program Files\Odoo 19.0.20260902\server\odoo-bin" -c "C:\Program Files\Odoo 19.0.20260902\server\odoo.conf" -d "%DBNAME%" -u theme_multiproduct_landing --stop-after-init

echo.
echo Syncing landing page views...
"C:\Program Files\Odoo 19.0.20260902\python\python.exe" "%~dp0..\convert_views.py"

echo.
echo =======================================================================
echo  SUCCESS: Single Page Multi-Product Store is Live!
echo  Visit: http://localhost:8069/?db=%DBNAME%
echo =======================================================================
pause

