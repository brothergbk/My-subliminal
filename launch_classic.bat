@echo off
REM Subliminal Message App Launcher (Classic Version)
REM This batch file launches the classic version of the Subliminal Message App

echo.
echo ========================================
echo   Subliminal Message App v1.0 (Classic)
echo ========================================
echo.
echo Starting the application...
echo.

REM Launch the classic version
python subliminal_app.py

REM If there's an error, pause so user can see it
if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch the application!
    echo Make sure Python is installed and dependencies are installed.
    echo Run: pip install -r requirement.txt
    echo.
    pause
)

