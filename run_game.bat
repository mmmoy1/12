@echo off
echo 🎮 Cyberpunk Adventure Launcher
echo ================================
echo.
echo Starting Cyberpunk Adventure...
echo.

python run_game.py

if errorlevel 1 (
    echo.
    echo ❌ Error: Failed to start the game
    echo    Make sure Python is installed and accessible
    echo.
    pause
)