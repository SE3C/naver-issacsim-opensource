@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Go2 6-Terrain Video Suite
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0go2_6terrain_video.ps1" %*
set "RC=%ERRORLEVEL%"
echo.
if "%GO2_VIDEO_NO_PAUSE%"=="1" goto done
pause
:done
exit /b %RC%
