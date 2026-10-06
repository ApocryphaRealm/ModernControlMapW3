@echo off
rem Modern Control Map (The Witcher 3) - puts the settings files back as they were before the first install.
rem Drag a settings folder onto this file to restore that folder instead of Documents\The Witcher 3.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Uninstall %1
pause
