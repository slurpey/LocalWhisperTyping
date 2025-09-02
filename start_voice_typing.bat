@echo off
REM LocalWhisperTyping Startup Script
REM This batch file provides an easy way to start the voice typing application

echo Starting LocalWhisperTyping...
echo.
echo This will:
echo - Load the Whisper model (may take a moment on first run)
echo - Start the voice typing service
echo - Create a system tray icon
echo.
echo Usage: Hold Ctrl+Shift to record, release to type
echo Exit: Press Ctrl+Shift+Esc or right-click tray icon
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the voice typing application
python lloydswhisper.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to close...
    pause >nul
)
