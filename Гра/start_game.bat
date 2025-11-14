@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
set PYTHON_PATH=C:\Users\yarik\AppData\Local\Python\pythoncore-3.14-64\python.exe
if exist "!PYTHON_PATH!" (
    "!PYTHON_PATH!" space_game.py
) else (
    python space_game.py
)
pause
