@echo off
title Policy Comparison
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0compare_policies.ps1" %*
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%
