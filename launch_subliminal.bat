@echo off
REM Subliminal Message App Launcher
REM This batch file launches the modern version of the Subliminal Message App

echo.
echo ========================================
echo   Subliminal Message App v2.0
echo ========================================
echo.
echo Starting the application...
echo.

REM Launch the modern version
python subliminal_app_modern.py

REM If there's an error, pause so user can see it
if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch the application!
    echo Make sure Python is installed and dependencies are installed.
    echo Run: pip install -r requirement.txt
    echo.
    pause
)

