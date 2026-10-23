@echo off
setlocal EnableExtensions DisableDelayedExpansion
title H1 6-Terrain Video Suite
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0h1_6terrain_video.ps1" %*
set "RC=%ERRORLEVEL%"
echo.
if "%H1_VIDEO_NO_PAUSE%"=="1" goto done
pause
:done
exit /b %RC%
