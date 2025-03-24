@echo off
echo ===================================
echo MotivaPlant - Game Runner
echo ===================================

REM Check if Python is installed
python --version > NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import pygame; import pyglet; from PIL import Image; import numpy" > NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Run the game
echo Starting MotivaPlant...
python run_game.py

pause